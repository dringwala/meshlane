# docs/spikes

Time-boxed Phase 0 investigations. Each spike produces one write-up named after the open question it settles (for example `oq-03-odps-odcs-validation.md`); throwaway code stays beside it. A spike ends with a recommendation and, where it changes a decision, a new or amended ADR.

| Spike | Open question | Question to answer | Output |
| --- | --- | --- | --- |
| ODPS/ODCS validation | [3](../open-questions.md), [4](../open-questions.md) | Do the example descriptor and contract validate against the official JSON Schemas? Where do `x-platform` extensions live? Does datacontract-cli read ODPS or only ODCS? | Corrected example YAML, `schemas/` skeleton |
| DataHub footprint | [2](../open-questions.md) | What does DataHub on Fargate with managed MSK, OpenSearch and RDS cost and take to run? Is `create` mode realistic for small adopters? | Cost and ops estimate, go/no-go on `create` mode |
| Environment layout | [6](../open-questions.md) | Separate dev and prod accounts per domain, or one account with prefixed resources? | Default proposal and Terraform layout |
| Region scope | [8](../open-questions.md) | Is single region enough for v1? | One-paragraph decision |

Phase 0 exit gate: WMS example files validate; foundation applies cleanly to three sandbox accounts.
