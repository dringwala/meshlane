# Contributing to meshlane

meshlane is in the design phase. The most useful contributions right now are review comments on the [architecture proposal](docs/architecture.md), the [ADRs](docs/adr/) and the [open questions](docs/open-questions.md).

## Making a decision

Significant decisions are recorded as ADRs in [`docs/adr/`](docs/adr/). To propose one, copy the format of an existing ADR (Context, Decision, Consequences), use the next free number and open a pull request. Add it to the decision log in `docs/architecture.md` and the ADR index when it is accepted.

## Repository layout

The layout is described in the [architecture proposal](docs/architecture.md#repository-layout). Each top-level directory has a README stating its purpose, phase and governing ADRs.

## Checks

CI runs these on every pull request. To run them locally, install [uv](https://docs.astral.sh/uv/), then from the repository root:

```bash
uv sync --locked
python3 .github/scripts/check_docs.py
uv run --locked python docs/spikes/oq-03-odps-odcs-validation/validate.py
uv run --locked datacontract lint docs/spikes/oq-03-odps-odcs-validation/contracts/shipments.odcs.yaml
(cd schemas/upstream && shasum -a 256 -c SHA256SUMS)
```

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`. After editing the dependencies, run `uv lock` and commit both files; CI fails if the lock is out of date. To pick up newer versions of locked packages, run `uv lock --upgrade`.

If you change an example file, change the matching YAML block in `docs/architecture.md` too; CI fails if they differ.

## Licensing

Contributions are accepted under the [Apache License 2.0](LICENSE) (inbound = outbound, per [ADR 011](docs/adr/011-apache-2-license.md)). The maintainer model and any contributor sign-off requirement are still open ([open question 11](docs/open-questions.md)).
