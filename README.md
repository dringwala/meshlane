# meshlane

**Data mesh blueprints for logistics.**

meshlane is an open-source reference implementation and template set for standing up a data mesh on AWS. It gives domain teams in logistics (order management, warehouse operations, transportation, customer analytics) a golden path for building data products from vendor systems such as ERP, WMS and TMS, or from their own pipelines.

> Status: **design phase.** The architecture proposal and decision records are in [`docs/`](docs/). No platform code has been released yet.

## What it will provide

- **Platform modules** (Terraform): account baselines, Lake Formation and LF-tags, output ports (Iceberg tables, Kinesis streams, APIs), ingestion (SFTP file drops, API pulls), MWAA orchestration, and catalog adapters.
- **Data product templates** (Copier): source-aligned, internal and consumer-aligned products that novice teams fill in with YAML and SQL.
- **Governance as code**: OPA policies run in GitHub Actions, classification tiers enforced by Lake Formation.
- **Open standards**: products described with [Bitol ODPS](https://github.com/bitol-io/open-data-product-standard), contracts with [Bitol ODCS](https://github.com/bitol-io/open-data-contract-standard).
- **A deployable example**: a fictional third-party logistics provider with synthetic data across four domains.

## Stack (v1)

AWS (S3, Glue, Lake Formation, Athena, Kinesis, API Gateway, MWAA) · Apache Iceberg · dbt · Terraform · GitHub Actions · DataHub · OpenLineage · OPA

## Repository layout

| Path | Contents | Phase |
| --- | --- | --- |
| [`platform/`](platform/) | Terraform modules: foundation, ports, ingestion, orchestration, catalog | 0–3 |
| [`schemas/`](schemas/) | JSON Schemas for the `x-platform` ODPS/ODCS extensions | 0 |
| [`policies/`](policies/) | OPA/Rego governance policies and tests | 1 |
| [`vocabulary/`](vocabulary/) | Logistics glossary and shared identifiers | 1–2 |
| [`.github/workflows/`](.github/workflows/) | Reusable CI workflows for product repos | 1 |
| [`cli/`](cli/) | The `meshlane` CLI | 1–4 |
| [`examples/logistics-3pl/`](examples/logistics-3pl/) | Fictional 3PL with synthetic data | 1–3 |
| [`templates/`](templates/) | Copier templates for products | 4 |
| [`docs/`](docs/) | Architecture, ADRs, open questions, spikes, Diátaxis docs | all |

## Documentation

| Document | Contents |
| --- | --- |
| [Architecture proposal](docs/architecture.md) | Scope, accounts, ports, descriptors, ingestion, governance, developer experience, roadmap |
| [Architecture decision records](docs/adr/) | ADR 001–016 |
| [Open questions](docs/open-questions.md) | Unresolved items and the phase each must close by |

## License

[Apache License 2.0](LICENSE)
