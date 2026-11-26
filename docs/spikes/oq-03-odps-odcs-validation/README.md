# Spike: ODPS and ODCS validation

Settles [open questions 3 and 4](../../open-questions.md). Run 2026-11-17 against datacontract-cli 1.2.11 and the upstream schemas as of that date.

## Result

The example in the architecture proposal did **not** validate. Corrected files now do, and a validator proves it (including seven negative cases, so the checks can fail).

```bash
python -m venv .venv && .venv/bin/pip install -r docs/spikes/oq-03-odps-odcs-validation/requirements.txt
.venv/bin/python docs/spikes/oq-03-odps-odcs-validation/validate.py
```

| Files | Contents |
| --- | --- |
| [`data-product.yaml`](data-product.yaml), [`contracts/shipments.odcs.yaml`](contracts/shipments.odcs.yaml) | Corrected WMS Shipments example |
| [`validate.py`](validate.py) | Validates against the vendored schemas plus the extension schema; negative tests |
| [`../../../schemas/upstream/`](../../../schemas/upstream/) | Pinned official schemas with checksums |
| [`../../../schemas/x-platform/product.v0.schema.json`](../../../schemas/x-platform/product.v0.schema.json) | First cut of the `x-platform` extension schema |

## Question 3: what was wrong with the example

| # | Problem | Fix |
| --- | --- | --- |
| 1 | `team` was a list; ODPS defines it as an object with `members` | `team: {name, members: [...]}` |
| 2 | Quality checks used `rule: rowCount` and `rule: duplicateCount` with a `column` key. ODCS 3.1.0+ rejects `rule` (deprecated for `metric`), `duplicateCount` is not a metric, and `column` does not exist. The check only passed on ODCS 3.0.2 because that version was lenient; datacontract-cli warns it becomes an error in January 2027 | `metric: rowCount` at table level; `metric: duplicateValues` on the `shipment_id` property |
| 3 | Only one column carried a classification, so the example failed the `classification-required` policy it was meant to illustrate | Every property classified |
| 4 | Versions were stale: ODPS 1.0.0 (now 1.1.0) and ODCS 3.0.2 (now 3.2.0) | Corrected files use ODPS v1.1.0 and ODCS v3.2.0 |

Valid ODCS library metrics are `nullValues`, `missingValues`, `invalidValues`, `duplicateValues` and `rowCount`. Extensions must live in `customProperties` because both schemas set `additionalProperties: false` at the top level.

## Question 4: what datacontract-cli does

| Capability | Finding |
| --- | --- |
| Read ODPS descriptors | **No.** `datacontract lint data-product.yaml` fails with `Cannot parse ODPS product`, and `catalog` skips ODPS files by name. meshlane validates the descriptor itself (JSON Schema plus OPA) |
| Lint ODCS contracts | Yes, v3.1.0 and v3.2.0 both pass |
| Detect breaking changes | Use **`datacontract breaking`**, not `changelog`. `changelog` lists differences and always exits 0. `breaking` exits 1 on a removed column or a type change and 0 on an added optional column, and has `--perspective consumer\|producer` |
| Check the version bump | **No.** `breaking` does not compare version numbers. The `semver-breaking` policy needs a small wrapper: if `breaking` exits 1, the major version must have increased |

## Other findings

1. **Upstream schema versions are not immutable.** The file for ODCS v3.1.0 has been modified 43 times, most recently on the day of this spike. The schemas are therefore vendored and pinned by checksum (see [`schemas/upstream/README.md`](../../../schemas/upstream/README.md)).
2. **`x-platform.classification` is unnecessary.** ODCS has a native property-level `classification` field. The corrected contract uses it with the four tier values; `validate.py` enforces the enum.
3. **ODPS v1.1.0 has native `type` fields** that overlap with our extensions. Product-level `type` takes `sourceAligned`, `aggregate`, `consumerAligned` (our three templates), and output ports have a free-text `type` that could carry `iceberg-table`, `kinesis-stream` or `api`. The corrected example keeps `x-platform.ports.<name>.type` as ADR 004 specifies and sets product `type: sourceAligned`.
4. `x-platform` cannot check cross-references (for example, that `ingestion` keys match input port names, or that each output port has a contract). Those belong in OPA policies.

## Changes made as a result

| Change | Where |
| --- | --- |
| Pin ODPS **v1.1.0** and ODCS **v3.2.0**, vendored with checksums; use native `classification`; use `datacontract breaking` plus a version check | [ADR 012](../../adr/012-bitol-odps-odcs.md) (amended) |
| Replace the example YAML, drop `x-platform.classification`, correct the contract-versioning command | [architecture proposal](../../architecture.md) |
| Mark questions 3 and 4 settled | [open questions](../../open-questions.md) |
| Output port type stays at `x-platform.ports.<name>.type` for now; whether to move to the native field is a new open question (13) | [open questions](../../open-questions.md) |

## Not covered

- `datacontract test` against real data (needs a server and sample data; Phase 1).
- The `shipment-events` and `wms-raw-shipments` contracts the descriptor references; only `shipments` was written.
- The `$id` in the extension schema is a placeholder (`raw.githubusercontent.com/dringwala/meshlane/...`); hosting for versioned `$id` URLs is undecided.
- The extension schema covers the product only. `file-drop` and `api-pull` settings beyond the example fields are not yet specified.
