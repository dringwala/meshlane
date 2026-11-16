# ADR 003: Self-managed Apache Iceberg on S3 general-purpose buckets

- Status: Accepted
- Date: 2026-11-10

## Context

Batch output ports need an open table format with schema evolution and ACID writes. Amazon S3 Tables manages compaction and snapshot expiry, but practitioners report that cross-account sharing through Lake Formation has undocumented sharp edges.

## Decision

v1 stores batch ports as Apache Iceberg tables on S3 general-purpose buckets, registered in the Glue Data Catalog. An S3 Tables port module is an opt-in addition once cross-account sharing is validated.

## Consequences

meshlane must schedule compaction and snapshot expiry itself (MWAA tasks). Cross-account sharing uses the well-documented Glue + Lake Formation path.
