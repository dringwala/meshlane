# ADR 013: Glue Data Catalog and Lake Formation as the technical layer

- Status: Accepted
- Date: 2026-11-10

## Context

Whichever business catalog is chosen, query engines need a technical catalog and an enforcement point.

## Decision

The Glue Data Catalog and Lake Formation are always deployed and are the source of truth for table metadata and access enforcement. Business catalogs sit on top through adapters.

## Consequences

Athena, Glue and EMR enforce grants natively. Non-AWS engines need Lake Formation-aware connectors.
