# ADR 005: MWAA (managed Apache Airflow) for orchestration

- Status: Accepted (amended 2026-11-25 by [ADR 014](014-separate-dev-prod-accounts.md))
- Date: 2026-11-10

## Context

Each data product needs scheduled ingestion, transformation, quality checks and table maintenance. Options were Step Functions, MWAA and Dagster.

## Decision

meshlane uses Amazon MWAA. One DAG per product is generated from the descriptor. In v1 dev and prod each have a single MWAA environment in their shared platform account, running all of that side's DAGs, which assume per-product roles in its domain accounts.

## Consequences

Open-source DAG model with a large talent pool. MWAA has a fixed hourly cost per environment; shared versus per-domain environments is an open question.
