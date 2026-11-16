# ADR 009: DataHub as the first business catalog adapter

- Status: Accepted
- Date: 2026-11-10

## Context

meshlane must either create a catalog or register into an existing one. An open-source default supports the project's positioning; AWS-native adopters want SageMaker Catalog.

## Decision

The catalog is an adapter with four operations (register product, publish port, sync owners and glossary, record subscriptions). DataHub is the first adapter and the default for `create` mode. SageMaker Catalog is the second adapter.

## Consequences

Self-hosting DataHub adds cost and operational weight (open question 2). Adopters with another catalog implement the adapter interface.
