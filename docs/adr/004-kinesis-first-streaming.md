# ADR 004: Kinesis Data Streams first for streaming ports

- Status: Accepted
- Date: 2026-11-10

## Context

Streaming output ports are needed for shipment and tracking events. Kinesis is simpler to operate; Kafka (MSK) is more portable and familiar to some adopters.

## Decision

The first streaming port module uses Kinesis Data Streams with the Glue Schema Registry. An MSK Serverless module follows behind the same `x-platform.port.type` key.

## Consequences

Lower operating burden for novice teams. Kafka-native consumers wait for the second module.
