# ADR 012: Bitol ODPS and ODCS for descriptors and contracts

- Status: Accepted
- Date: 2026-11-10

## Context

Each data product needs a machine-readable descriptor and per-port contracts. A custom schema would isolate the project from other tooling.

## Decision

Products are described with Bitol Open Data Product Standard v1.0; contracts use Open Data Contract Standard v3. meshlane-specific bindings live under `customProperties` with an `x-platform` key, validated by meshlane's extension JSON Schemas.

## Consequences

Interoperable with tools that read ODCS (for example datacontract-cli). meshlane must track upstream spec versions.
