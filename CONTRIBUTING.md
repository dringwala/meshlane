# Contributing to meshlane

meshlane is in the design phase. The most useful contributions right now are review comments on the [architecture proposal](docs/architecture.md), the [ADRs](docs/adr/) and the [open questions](docs/open-questions.md).

## Making a decision

Significant decisions are recorded as ADRs in [`docs/adr/`](docs/adr/). To propose one, copy the format of an existing ADR (Context, Decision, Consequences), use the next free number and open a pull request. Add it to the decision log in `docs/architecture.md` and the ADR index when it is accepted.

## Repository layout

The layout is described in the [architecture proposal](docs/architecture.md#repository-layout). Each top-level directory has a README stating its purpose, phase and governing ADRs.

## Licensing

Contributions are accepted under the [Apache License 2.0](LICENSE) (inbound = outbound, per [ADR 011](docs/adr/011-apache-2-license.md)). The maintainer model and any contributor sign-off requirement are still open ([open question 11](docs/open-questions.md)).
