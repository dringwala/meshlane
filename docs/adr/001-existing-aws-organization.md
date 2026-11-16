# ADR 001: Assume an existing AWS Organization

- Status: Accepted
- Date: 2026-11-10

## Context

Adopters need a multi-account AWS setup before a mesh can run. Building a landing zone would double the project's scope and duplicate Control Tower, Landing Zone Accelerator and similar tools that adopters already use.

## Decision

meshlane assumes an AWS Organization with the needed accounts already exists. The docs list prerequisites (accounts, SCP allowances, Lake Formation settings) and the foundation module baselines the accounts it is given.

## Consequences

Scope stays on the mesh. Adopters without an organization must set one up first; the getting-started guide links to AWS options.
