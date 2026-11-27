"""Validate the WMS example against the vendored Bitol schemas, the meshlane
x-platform extension schema (spike for open question 3) and the naming rules
of ADR 016.

Run from the repository root:
    python docs/spikes/oq-03-odps-odcs-validation/validate.py
Exits non-zero if any positive check fails or any negative check passes.
"""
import copy
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft201909Validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
UP = ROOT / "schemas" / "upstream"
TIERS = {"public", "internal", "confidential", "restricted"}
SLUG = re.compile(r"[a-z][a-z0-9]*(-[a-z0-9]+)*")
COLUMN = re.compile(r"[a-z][a-z0-9_]*")


def is_slug(value):
    return len(value) <= 20 and SLUG.fullmatch(value) is not None


def is_contract_id(value):
    parts = value.split(".")
    return len(parts) == 3 and all(map(is_slug, parts))


def check_product_names(product):
    errs = []
    domain, _, name = product["id"].partition(".")
    if domain != product["domain"] or not is_slug(domain) or not is_slug(name):
        errs.append(f"id {product['id']!r} is not <domain>.<product> with valid slugs")
    if domain in {"governance", "platform"} or name == "shared":
        errs.append(f"id {product['id']!r} uses a reserved name")
    for kind in ("inputPorts", "outputPorts"):
        for port in product.get(kind, []):
            if not is_slug(port["name"]):
                errs.append(f"{kind}: {port['name']!r} is not a valid slug")
            if not is_contract_id(port.get("contractId", "")):
                errs.append(f"{kind}: contractId {port.get('contractId')!r} is not <domain>.<product>.<port>")
            elif kind == "outputPorts" and port["contractId"] != f"{product['id']}.{port['name']}":
                errs.append(f"{kind}: contractId {port['contractId']!r} does not match the port")
    return errs


def check_contract_names(contract):
    if not is_contract_id(contract["id"]):
        return [f"id {contract['id']!r} is not <domain>.<product>.<port>"]
    errs = []
    domain, name, _ = contract["id"].split(".")
    if (contract.get("domain"), contract.get("dataProduct")) != (domain, name):
        errs.append("domain and dataProduct do not match the id")
    major = contract["version"].split(".")[0]
    names = [obj["name"] for obj in contract.get("schema", [])]
    errs += [f"duplicate schema object {n!r}" for n in sorted(set(names)) if names.count(n) > 1]
    for obj in contract.get("schema", []):
        if not COLUMN.fullmatch(obj["name"]):
            errs.append(f"{obj['name']}: object name is not snake_case")
        expected = f"{obj['name']}_v{major}"
        if obj.get("physicalName") != expected:
            errs.append(f"{obj['name']}: physicalName {obj.get('physicalName')!r}, expected {expected!r}")
        for prop in obj.get("properties", []):
            if not COLUMN.fullmatch(prop["name"]):
                errs.append(f"{obj['name']}.{prop['name']}: column name is not snake_case")
    return errs


def load_schema(path):
    return Draft201909Validator(json.loads(path.read_text()))


ODPS = load_schema(UP / "odps-json-schema-v1.1.0.json")
ODCS = load_schema(UP / "odcs-json-schema-v3.2.0.json")
XPLAT = load_schema(ROOT / "schemas" / "x-platform" / "product.v0.schema.json")


def errors(validator, doc):
    return [
        f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message[:120]}"
        for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    ]


def xplatform(product):
    for cp in product.get("customProperties", []):
        if cp["property"] == "x-platform":
            return cp["value"]
    return None


def check_product(product):
    errs = errors(ODPS, product)
    if not errs:
        errs += check_product_names(product)
    xp = xplatform(product)
    if xp is None:
        errs.append("customProperties: no x-platform entry")
    else:
        errs += ["x-platform/" + e for e in errors(XPLAT, xp)]
    return errs


def check_contract(contract):
    errs = errors(ODCS, contract)
    if not errs:
        errs += check_contract_names(contract)
    for obj in contract.get("schema", []):
        for prop in obj.get("properties", []):
            tier = prop.get("classification")
            if tier not in TIERS:
                errs.append(f"{obj['name']}.{prop['name']}: classification {tier!r} not one of {sorted(TIERS)}")
    return errs


product = yaml.safe_load((HERE / "data-product.yaml").read_text())
contract = yaml.safe_load((HERE / "contracts" / "shipments.odcs.yaml").read_text())

failed = False


def positive(name, errs):
    global failed
    print(f"{'PASS' if not errs else 'FAIL'}  {name}")
    for e in errs:
        print("        ", e)
    failed |= bool(errs)


def negative(name, errs):
    global failed
    print(f"{'PASS' if errs else 'FAIL'}  {name} (rejected: {errs[0] if errs else 'NOT REJECTED'})")
    failed |= not errs


positive("data-product.yaml (ODPS v1.1.0 + x-platform)", check_product(product))
positive("contracts/shipments.odcs.yaml (ODCS v3.2.0 + classification)", check_contract(contract))

# Negative cases: the checks must be able to fail.
p = copy.deepcopy(product); p["team"] = [{"username": "a@example.com", "role": "owner"}]
negative("team as a list (the original example's mistake)", check_product(p))

p = copy.deepcopy(product); xplatform(p)["tier"] = 4
negative("unknown golden-path tier", check_product(p))

p = copy.deepcopy(product); xplatform(p)["ports"]["shipments"]["type"] = "parquet-folder"
negative("unknown port module", check_product(p))

p = copy.deepcopy(product); xplatform(p)["ingestion"]["wms-daily-extract"].pop("pattern")
negative("file-drop without a file pattern", check_product(p))

c = copy.deepcopy(contract); c["schema"][0]["quality"] = [{"rule": "rowCount", "mustBeGreaterThan": 0}]
negative("quality check using `rule:` instead of `metric:`", check_contract(c))

c = copy.deepcopy(contract); c["schema"][0]["properties"][0]["quality"] = [{"metric": "duplicateCount", "mustBe": 0}]
negative("non-existent metric duplicateCount", check_contract(c))

c = copy.deepcopy(contract); c["schema"][0]["properties"][1].pop("classification")
negative("property without classification", check_contract(c))

p = copy.deepcopy(product); p["outputPorts"][0]["name"] = "shipment_lines"
negative("port name with an underscore", check_product(p))

p = copy.deepcopy(product); p["id"] = "warehouse-ops.wms-shipments-and-returns"
negative("product slug over 20 characters", check_product(p))

p = copy.deepcopy(product); xplatform(p)["costCenter"] = "WH OPS"
negative("cost center with a space", check_product(p))

c = copy.deepcopy(contract); c["id"] = "warehouse-ops.shipments"
negative("two-part contract id", check_contract(c))

c = copy.deepcopy(contract); c["schema"][0].pop("physicalName")
negative("table without a versioned physicalName", check_contract(c))

c = copy.deepcopy(contract)
lines = copy.deepcopy(c["schema"][0])
lines.update(name="shipment_lines", physicalName="shipment_lines_v1")
c["schema"].append(lines)
positive("contract with two tables", check_contract(c))

c["schema"][1]["physicalName"] = "shipments_v1"
negative("second table not named after its object", check_contract(c))

c = copy.deepcopy(contract); c["schema"].append(copy.deepcopy(c["schema"][0]))
negative("two schema objects with the same name", check_contract(c))

sys.exit(1 if failed else 0)
