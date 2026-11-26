# ADR 014: Separate dev and prod accounts

- Status: Accepted
- Date: 2026-11-25

## Context

Domain and platform teams need somewhere to try changes without touching production data or consumers. The alternatives were one account per role with environment-prefixed resources, or separate dev and prod accounts. Prefixed resources keep the account count low but leave IAM permissions, service quotas and mistakes shared between environments. Splitting only the domain accounts would still leave LF-tag and grant changes with nowhere separate to be tested, and one MWAA environment running dev DAGs beside prod ones.

## Decision

Dev and prod each have a complete set of accounts: one governance account, one shared platform account and one account per domain. No account serves both. Grants, deploy roles and data do not cross between dev and prod.

## Consequences

Account boundaries separate dev from prod for IAM, quotas and blast radius, and governance changes can be tried in dev first. The account count doubles: the four-domain example needs twelve, and the AWS Organization prerequisite ([ADR 001](001-existing-aws-organization.md)) grows to match.

Shared services are paid for in both environments, including a second MWAA environment ([ADR 005](005-mwaa-orchestration.md)). Their cost is not yet measured. A dev environment can set the catalog provider to `none` to avoid a second DataHub, at the price of not testing catalog changes there.

All modules must deploy the same code to either environment, taking the target environment as input, with Terraform state kept in that environment's platform account. CI applies to dev first, then to prod behind an approval.
