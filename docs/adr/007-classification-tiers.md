# ADR 007: Classification tiers with column masking for PII

- Status: Accepted
- Date: 2026-11-10

## Context

Logistics data includes driver identity, consignee names and addresses, and GPS traces. Regulations differ by adopter and region.

## Decision

Every contract property carries one of four tiers: public, internal, confidential, restricted. Tiers map to Lake Formation LF-tags; restricted columns are masked or excluded with data cell filters. No specific regulation (GDPR, CCPA) is encoded in v1.

## Consequences

Adopters map their regulatory requirements onto the tiers. Streams and APIs need separate protection because Lake Formation does not govern them (open question 5).
