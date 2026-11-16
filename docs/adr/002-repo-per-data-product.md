# ADR 002: One repository per data product

- Status: Accepted
- Date: 2026-11-10

## Context

Data products need clear ownership, independent release cycles and a limited blast radius. Some organizations prefer a domain monorepo.

## Decision

Each data product lives in its own repository generated from a meshlane template. A monorepo layout (one folder per product) is supported as an option, using the same reusable workflows with path filters.

## Consequences

Ownership maps cleanly to CODEOWNERS and repo permissions. Cross-product refactors need multiple PRs; template updates are applied per repo with `copier update`.
