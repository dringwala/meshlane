# ADR 012: Bitol ODPS and ODCS for descriptors and contracts

- Status: Accepted (amended 2026-11-17 after the [ODPS/ODCS validation spike](../spikes/oq-03-odps-odcs-validation/README.md))
- Date: 2026-11-10

## Context

Each data product needs a machine-readable descriptor and per-port contracts. A custom schema would isolate the project from other tooling.

## Decision

Products are described with Bitol Open Data Product Standard (ODPS) **v1.1.0**; contracts use Open Data Contract Standard (ODCS) **v3.2.0**. meshlane-specific bindings live under `customProperties` with an `x-platform` key, validated by meshlane's extension JSON Schemas.

The official JSON Schemas are vendored in `schemas/upstream/` and pinned by checksum, because upstream rewrites released schema files in place. Upgrading a pin is a reviewed change that re-runs validation.

Where the standards already define a field, meshlane uses it instead of an extension. In particular, a column's tier is the native ODCS `classification` property, set to `public`, `internal`, `confidential` or `restricted` ([ADR 007](007-classification-tiers.md)).

Descriptors are validated by meshlane (JSON Schema plus OPA policies), because datacontract-cli reads ODCS contracts but not ODPS descriptors. Contract compatibility is checked with `datacontract breaking`, wrapped so that a breaking change requires a major version bump.

## Consequences

Interoperable with tools that read ODCS (for example datacontract-cli). meshlane must track upstream spec versions and review each schema update before adopting it.

Whether output port types move from `x-platform.ports.<name>.type` to the native ODPS `outputPorts[].type` is left open (open question 13).
