# Open questions

These items are unresolved by design; each names what decides it and the phase it must close by.

| # | Question | Why it matters | Settled by | Close by |
| --- | --- | --- | --- | --- |
| 1 | One shared MWAA environment, or one per domain? | Shared is cheaper; per-domain isolates failures and upgrades | Measured cost and DAG count in the example | Phase 2 |
| 2 | How heavy is DataHub to self-host? It depends on Kafka, a search index and a database | Drives example cost and whether `create` mode is realistic for small adopters | Spike deploying DataHub on Fargate with managed MSK, OpenSearch and RDS | Phase 0 |
| 3 | Exact ODPS and ODCS field names and where extensions live | The example YAML is unvalidated | Validate against the official JSON Schemas | Phase 0 |
| 4 | Does datacontract-cli read ODPS descriptors, or only ODCS contracts? | Decides whether the CLI parses ODPS itself | Check current tool support | Phase 0 |
| 5 | How are restricted fields protected on stream and API ports? Lake Formation does not govern Kinesis or API Gateway | Masking must hold outside the lake | Options: publish a redacted stream beside the full one; field filtering in the API Lambda | Phase 3 |
| 6 | Environments: separate dev and prod accounts per domain, or one account per domain with prefixed resources? | Doubles account count, changes Terraform layout | Adopter feedback; default proposal in Phase 0 | Phase 0 |
| 7 | How are human consumers identified for grants: IAM Identity Center users, or roles only? | Lake Formation grants and catalog subscriptions need a principal | Spike with Athena + Identity Center propagation | Phase 1 |
| 8 | Single region in v1? | Cross-region sharing adds catalog and Lake Formation complexity | Default single region unless adopters need more | Phase 0 |
| 9 | Generate AsyncAPI and OpenAPI from ODCS with existing tools, or build a generator? | Scope of the CLI | Survey available converters | Phase 3 |
| 10 | dbt-athena merge performance on large Iceberg tables | Hourly WMS loads may hit limits | Load test with synthetic data at 10× example volume | Phase 2 |
| 11 | Maintainer model, and whether to seek a foundation home later | Contributor trust and adoption | Project owner decision | Before public launch |
| 12 | Will Copier templates map cleanly to Backstage scaffolder templates later? | Avoids rework when the portal arrives | Prototype one template both ways | Phase 4 |
