# ADR 015: Single AWS region in v1

- Status: Accepted
- Date: 2026-11-25

## Context

Sharing data across regions adds work to both the Glue Data Catalog and Lake Formation. Nothing in the v1 scope needs more than one region.

## Decision

In v1 a mesh runs in one AWS region. All of its accounts, dev and prod, use that region. The adopter chooses which one.

## Consequences

No cross-region sharing, replication or failover is built or tested. Adopters whose data residency or recovery requirements call for more than one region are not served by v1. Modules take the region as an input rather than hard-coding it, so that adding regions later does not start with removing assumptions.
