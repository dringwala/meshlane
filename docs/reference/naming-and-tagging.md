# Naming and tagging

> Status: **accepted** in [ADR 016](../adr/016-naming-and-tagging.md). The extension schema checks the cost center and `x-platform` port keys; policies that check the rest in product CI are not written yet.

## Slugs

| Slug | Pattern | Max | Source | Example |
| --- | --- | --- | --- | --- |
| `org` | `^[a-z][a-z0-9]{1,5}$` | 6 | Deployment configuration | `acme` |
| `domain` | `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` | 20 | Descriptor `domain` | `warehouse-ops` |
| `product` | same as `domain` | 20 | Second part of descriptor `id` | `wms-shipments` |
| `port` | same as `domain` | 20 | Input or output port `name` | `shipment-events` |
| `major` | integer from 1 | 2 digits | Major part of the port `version` | `1` |

- No underscores or doubled hyphens in slugs. This keeps the `-` to `_` mapping below reversible.
- Reserved: domain names `governance` and `platform`; product name `shared`.
- `domain` is unique in the mesh. `product` is unique within its domain. `port` is unique within its product, per major version.

## Identifiers

| Thing | Form | Example |
| --- | --- | --- |
| Product id (ODPS `id`) | `<domain>.<product>` | `warehouse-ops.wms-shipments` |
| Contract id (ODCS `id`) | `<domain>.<product>.<port>` | `warehouse-ops.wms-shipments.shipments` |
| Product repository | `<product>`, or `<domain>-<product>` if two domains share a product slug | `wms-shipments` |
| Column | `^[a-z][a-z0-9_]*$` | `ship_from_gln` |

An input port fed by a vendor source has its own contract id under this product (`warehouse-ops.wms-shipments.wms-daily-extract`). An input port fed by another product uses that product's contract id.

## Resource names

`_x` below means the slug with `-` replaced by `_`. None of these names contains the environment: dev and prod are separate accounts. The exception is account names.

### Data catalog

| Resource | Form | Example |
| --- | --- | --- |
| Published database | `<domain_x>__<product_x>` | `warehouse_ops__wms_shipments` |
| Staged database | `<domain_x>__<product_x>__staged` | `warehouse_ops__wms_shipments__staged` |
| Raw database (if tables are registered) | `<domain_x>__<product_x>__raw` | `warehouse_ops__wms_shipments__raw` |
| Published table (batch port) | `<object>_v<major>` | `shipments_v1` |
| Staged and raw tables | `^[a-z][a-z0-9_]*$`, no version | `wms_shipment_lines` |

The double underscore separates the parts, so `warehouse_ops__wms_shipments` reads only one way. The domain is part of the database name because consumers see databases from many domains side by side.

A batch port can publish several tables. Each is one schema object in the port's contract:

- `<object>` is the object's ODCS `name`, matching `^[a-z][a-z0-9_]*$`. A port with a single table names the object after the port (`shipments`).
- `<major>` is the port's major version, so all tables of a port move to a new major version together.
- Object names are unique across all of a product's batch ports, because the tables share one database.
- The contract records the table name in `physicalName` (`physicalName: shipments_v1`); `name` stays `shipments`.

Stream and API resources are named per port, as below.

### Storage

| Resource | Form |
| --- | --- |
| Raw bucket (source-aligned products) | `<org>-<product>-raw-<account-id>-<region>-an` |
| Data bucket (staged and published) | `<org>-<product>-data-<account-id>-<region>-an` |
| Other shared buckets | `<org>-<purpose>-<account-id>-<region>-an`, purpose at most 20 characters (`tfstate`, `mwaa`) |

Example: `acme-wms-shipments-data-111122223333-ap-southeast-4-an`.

Buckets use the [S3 account regional namespace](https://docs.aws.amazon.com/AmazonS3/latest/userguide/gpbucketnamespaces.html): only the owning account can create names with its suffix. The suffix counts toward the 63-character limit, and this is what sets the slug lengths: at 6-character `org`, 20-character `product` and a 14-character region code, a data bucket name is exactly 63.

- **Unsupported regions.** `me-south-1` and `me-central-1` do not offer the namespace. There, use `<org>-<product>-<layer>-<account-id>` in the global namespace.
- **Terraform.** `aws_s3_bucket` takes `bucket_namespace = "account-regional"`. A [reported problem](https://github.com/hashicorp/terraform-provider-aws/issues/47077) with it means the first port module must prove it works and pin a provider version.

Prefixes inside the buckets:

| Bucket | Prefix |
| --- | --- |
| Raw | `landing/<input-port>/`, `quarantine/<input-port>/` |
| Data | `staged/<table>/`, `published/<table>/` |

Athena query result locations are left to the foundation module.

### Compute, streaming, serving and security

| Resource | Form | Limit |
| --- | --- | --- |
| Airflow `dag_id` | `<domain>.<product>` | 250 |
| MWAA environment | `<org>-mwaa` | 80 |
| Athena workgroup (one per product) | `<org>-<product>` | 128 |
| Product runtime role (assumed by DAGs) | `<org>-<product>-runtime` | 64 |
| Product deploy role | `<org>-<domain>-<product>-deploy` | 64 |
| Stream consumer role | `<org>-<product>-<port>-v<major>-read-<consumer-domain>` | 64, see below |
| Lambda function | `<org>-<product>-<function>`, function at most 20 | 64 |
| EventBridge rule | `<org>-<product>-<event>`, event at most 20 | 64 |
| Kinesis stream | `<org>-<product>-<port>-v<major>` | 128 |
| DynamoDB table (API port) | `<org>-<product>-<port>-v<major>` | 255 |
| KMS alias | `alias/<org>/<product>` | 256 |
| Secret | `<org>/<product>/<name>` | 256 |
| Schema registry (platform account) | `<domain>` | 255 |
| Schema | `<product>.<port>-v<major>` | 255 |
| Terraform state key | `<domain>/<product>/terraform.tfstate` | — |

Deploy roles carry the domain because they are held in the shared platform account, where product slugs from different domains meet. Naming the stream consumer role after the consumer's domain assumes one role per consuming domain; how consumers are identified is still [open question 7](../open-questions.md).

**Over-length names.** If a composed name exceeds its limit, keep the first *limit − 7* characters, drop any trailing separator, and append `-` plus the first 6 hex characters of the SHA-256 of the full name. With maximum-length slugs, only the stream consumer role needs this.

### Accounts

Account names belong to the adopter's organization ([ADR 001](../adr/001-existing-aws-organization.md)). Suggested: `<org>-<env>-governance`, `<org>-<env>-platform`, `<org>-<env>-<domain>`, with `env` one of `dev`, `prod`.

### Lake Formation tags

| Key | Values |
| --- | --- |
| `classification` | `public`, `internal`, `confidential`, `restricted` |

Lake Formation stores tag keys and values in lower case. AWS documentation disagrees on the length limit (50 characters on one page, more in the API reference), so keep both within 50. Other LF-tags are not defined yet. An adopter who already has a `classification` LF-tag with different values has a conflict that v1 does not handle.

## Resource tags

### Required on every taggable resource

| Tag | Value | Source |
| --- | --- | --- |
| `meshlane:domain` | Domain slug, or `governance` / `platform` for central resources | Descriptor `domain` |
| `meshlane:product` | Product slug, or `shared` for resources not owned by one product | Descriptor `id` |
| `meshlane:cost-center` | `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$` | `x-platform.costCenter`, or deployment configuration for shared resources |
| `meshlane:environment` | `dev` or `prod` | Deployment configuration |

### Recommended

| Tag | Value |
| --- | --- |
| `meshlane:managed-by` | `terraform` |
| `meshlane:repository` | `<owner>/<repo>` |

The `meshlane:` prefix is fixed, not derived from `org`, so policies and cost reports work the same for every adopter. Tag keys and values are case sensitive.

### How tags are applied and checked

- Modules set the tags through the AWS provider's `default_tags`.
- Policy checks read `tags_all` in the Terraform plan JSON, which includes the defaults; checking `tags` alone would report false failures.
- Do not repeat a default tag with the same value on a resource.

### Cost attribution limits

- Tags appear in billing only after they are activated as [cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html) in the management account, which can take up to a day to show and another to activate.
- S3 cost tags work at [bucket level only](https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html), which is why buckets are per product.
- Some things cannot be tagged, including Glue tables (databases can) and Lake Formation grants.
- Shared services (MWAA, the business catalog) are reported as `shared`; splitting their cost between products is not covered.

## Worked example

WMS Shipments, `org` = `acme`, region `ap-southeast-4`:

| Resource | Name |
| --- | --- |
| Data bucket | `acme-wms-shipments-data-111122223333-ap-southeast-4-an` |
| Published table | `warehouse_ops__wms_shipments.shipments_v1` |
| Stream | `acme-wms-shipments-shipment-events-v1` |
| Runtime role | `acme-wms-shipments-runtime` |
| DAG | `warehouse-ops.wms-shipments` |
