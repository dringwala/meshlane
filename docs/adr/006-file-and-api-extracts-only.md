# ADR 006: Vendor sources arrive as file and API extracts only

- Status: Accepted
- Date: 2026-11-10

## Context

Vendor systems (ERP, WMS, TMS) are often on-premises. A reference implementation must deploy without VPN or Direct Connect to those systems.

## Decision

v1 ingestion supports SFTP or S3 file drops (including EDI X12) and scheduled API pulls. Database CDC (AWS DMS) is deferred to a later module behind the same `x-platform.ingestion` key.

## Consequences

The reference runs anywhere with synthetic data. Near-real-time sources must use API pulls or wait for the CDC module.
