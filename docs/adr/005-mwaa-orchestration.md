# ADR 005: MWAA (managed Apache Airflow) for orchestration

- Status: Accepted
- Date: 2026-11-10

## Context

Each data product needs scheduled ingestion, transformation, quality checks and table maintenance. Options were Step Functions, MWAA and Dagster.

## Decision

meshlane uses Amazon MWAA. One DAG per product is generated from the descriptor. In v1 a single MWAA environment in the shared platform account runs all DAGs, which assume per-product roles in domain accounts.

## Consequences

Open-source DAG model with a large talent pool. MWAA has a fixed hourly cost per environment; shared versus per-domain environments is an open question.
