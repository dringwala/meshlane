# schemas/upstream

Pinned copies of the official Bitol JSON Schemas ([ADR 012](../../docs/adr/012-bitol-odps-odcs.md)). Both upstream projects are Apache-2.0.

| File | Source | Fetched |
| --- | --- | --- |
| `odps-json-schema-v1.1.0.json` | [open-data-product-standard](https://github.com/bitol-io/open-data-product-standard/tree/main/schema) | 2026-11-17 |
| `odcs-json-schema-v3.2.0.json` | [open-data-contract-standard](https://github.com/bitol-io/open-data-contract-standard/tree/main/schema) | 2026-11-17 |

**Why vendored.** Upstream rewrites released schema files in place: the file for ODCS v3.1.0 has been modified 43 times, most recently on 2026-11-17. Validating against a live URL would make CI results change without any change in this repo. `SHA256SUMS` records what we pinned; check it with `shasum -a 256 -c SHA256SUMS`.

**Updating.** Fetch the new file, re-run the validation tests, update the table and checksums in the same pull request.
