# .github/workflows

Reusable workflows called by product repos (validate, build, test, plan, deploy, publish). Pinned by tag, e.g. `@v1`. Workflows for this repo's own CI also live here.

- **Phase:** 1
- **Decisions:** [ADR 002](../../docs/adr/002-repo-per-data-product.md)

## This repository's CI

[`repo-ci.yml`](repo-ci.yml) runs on every pull request and on pushes to `main`. It is not a reusable workflow.

| Job | Checks |
| --- | --- |
| `docs` | Relative links resolve; the architecture YAML examples match the validated example files |
| `schemas` | Vendored schema checksums; extension schemas are valid JSON Schema; example descriptor and all example contracts validate ([`validate.py`](../../docs/spikes/oq-03-odps-odcs-validation/validate.py)); `datacontract lint` |

Contracts are gated by schema validation, because `datacontract lint` accepts some invalid files. Actions are pinned to commit SHAs, Python dependencies are locked in `uv.lock`, and the job token is read-only.

> Reusable workflows for product repos: not started. See [architecture proposal](../../docs/architecture.md).
