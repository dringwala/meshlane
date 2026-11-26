"""Spike for open question 3: validate the WMS example against the vendored
Bitol schemas and the meshlane x-platform extension schema.

Run from the repository root:
    python docs/spikes/oq-03-odps-odcs-validation/validate.py
Exits non-zero if any positive check fails or any negative check passes.
"""
import copy
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft201909Validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
UP = ROOT / "schemas" / "upstream"
TIERS = {"public", "internal", "confidential", "restricted"}


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
    xp = xplatform(product)
    if xp is None:
        errs.append("customProperties: no x-platform entry")
    else:
        errs += ["x-platform/" + e for e in errors(XPLAT, xp)]
    return errs


def check_contract(contract):
    errs = errors(ODCS, contract)
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

sys.exit(1 if failed else 0)
