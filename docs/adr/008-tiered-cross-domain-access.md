# ADR 008: Tiered cross-domain access

- Status: Accepted
- Date: 2026-11-10

## Context

Self-serve access drives mesh adoption, but sensitive data needs owner consent.

## Decision

Public and internal ports are granted to all domains automatically. Confidential and restricted ports require owner approval through a pull request in the governance repo; restricted grants also need a stated purpose and are time-boxed. All grants are Terraform.

## Consequences

Most access is instant. Every grant is auditable and revocable by revert.
