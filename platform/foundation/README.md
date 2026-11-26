# platform/foundation

Governance, shared-platform and domain account baselines: KMS keys, Lake Formation settings, LF-tag ontology, GitHub OIDC deploy roles, cost-allocation tags. Assumes an existing AWS Organization. Dev and prod each have a complete, separate set of these accounts, and the whole mesh runs in one region.

- **Phase:** 0
- **Decisions:** [ADR 001](../../docs/adr/001-existing-aws-organization.md), [013](../../docs/adr/013-glue-lake-formation-technical-layer.md), [014](../../docs/adr/014-separate-dev-prod-accounts.md), [015](../../docs/adr/015-single-region.md)

> Status: not started. See [architecture proposal](../../docs/architecture.md).
