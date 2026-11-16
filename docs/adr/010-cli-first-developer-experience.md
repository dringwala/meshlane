# ADR 010: CLI-first developer experience

- Status: Accepted
- Date: 2026-11-10

## Context

Novice domain teams need guided scaffolding and local validation. A developer portal is valuable but heavy to build and run.

## Decision

v1 ships the `meshlane` CLI (new, validate, dev, render, subscribe, backfill, scorecard, update). Backstage scaffolder templates are added later from the same Copier templates.

## Consequences

Lower entry cost. Teams without a terminal-friendly workflow wait for the portal.
