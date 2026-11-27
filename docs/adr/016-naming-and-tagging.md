# ADR 016: Naming and tagging conventions

- Status: Accepted
- Date: 2026-11-26

## Context

Modules, policies and templates all derive resource names and cost tags from the descriptor. Most names cannot be changed later without recreating the resource, so the rules have to exist before the first module. The full rules, with limits and examples, are in the [naming and tagging reference](../reference/naming-and-tagging.md).

## Decision

1. **Short slugs.** The organization prefix is at most 6 characters; domain, product and port slugs at most 20.
2. **Environment is not in resource names.** Dev and prod are separate accounts ([ADR 014](014-separate-dev-prod-accounts.md)), so Glue databases, tables, roles and streams have the same names in both, and SQL and contracts move between them unchanged.
3. **One raw and one data bucket per product**, in the S3 account regional namespace, which supplies global uniqueness through the account ID and region.
4. **Published names carry the major version** from v1 onwards (`shipments_v1`), so a new major version can sit beside the old one. A batch port can publish several tables, each named after its schema object in the contract.
5. **Contract ids are `<domain>.<product>.<port>`**, unique by construction.
6. **Four required tags** under a fixed `meshlane:` prefix: `domain`, `product`, `cost-center`, `environment`.

## Consequences

Names are predictable from the descriptor, so no one chooses them by hand and policies can check them. Related tables can share one port and contract; their names must then be unique across the product, and settings such as partitioning can no longer be assumed to be per port (open question 15). Per-product buckets let S3 cost be attributed to a product, which bucket-level cost tags cannot do for a shared bucket; the price is more buckets to manage.

The account regional namespace is not offered in `me-south-1` or `me-central-1`, so those regions need the fallback in the reference. Terraform support must be proven in Phase 1.

Adopters must activate the four tags as cost allocation tags in their management account.

The example files, the extension schema and the example validator follow these rules. Checks that run in product CI arrive with the OPA policies in Phase 1; until then nothing enforces them on a real product.
