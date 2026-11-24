# Discovery — `ai-agent-py`

Status: Draft · 2026-11-24

This folder is the discovery phase of the project specification for `ai-agent-py`, a Python
customer-support agent being built as a staged LLM engineering project. It defines the problem,
stakeholders, requirements, constraints, and success measures before solution and delivery
specifications are written.

## Evidence base

| Source | Use |
| --- | --- |
| `README.md`, `LOG.md` | Stated purpose, lesson history, current status, known gaps |
| `src/ai_agent/**` | Observed implementation and architecture |
| `tests/**` | Observed verification coverage and current failures |
| `pyproject.toml`, `.env.example` | Dependencies, commands, configuration |
| `experiments/**` | Manual proof-of-concept behavior |
| `docs/SUMMARY.md` | Lesson-level design rationale; treat status sections as point-in-time snapshots |

No stakeholder interviews, production telemetry, live-model evaluations, or user research were
available at the time of writing. Statements derived from those activities are marked as
hypotheses or open questions rather than facts.

## Ground rules

1. Separate **observed** current behavior, **target** behavior, and **assumed** behavior.
2. Every requirement carries an evidence reference and a validation status.
3. Targets in this pack are proposed until measured on a representative dataset.
4. Business state comes from tools, databases, or application code; model output is never the
   authority for order status, permissions, or workflow state.
5. Secrets, owner IDs, and retrieved memory are treated as sensitive or untrusted inputs.

## Documents

| File | Purpose |
| --- | --- |
| `discovery-brief.md` | Problem, vision, scope, findings, decision gates |
| `stakeholder-interviews.md` | Stakeholder map, interview guide, evidence and hypotheses |
| `business-requirements.md` | Why the project exists and what outcomes it must deliver |
| `functional-requirements.md` | Observable behaviors and acceptance criteria |
| `non-functional-requirements.md` | Quality, security, performance, cost, and operability targets |
| `assumptions-and-constraints.md` | What we assume, what limits us, and what must be validated |
| `success-metrics.md` | Metrics, baselines, targets, measurement methods, and exit gates |

## Traceability

Requirements use stable IDs:

- `BR-xx` — business requirement
- `FR-xx` — functional requirement
- `NFR-xx` — non-functional requirement
- `A-xx` — assumption
- `Q-xx` — open question

Later design, architecture, test, and release documents should reference these IDs.

## Change process

Update the affected document and its status when evidence changes. Record the source of new
evidence (interview, experiment, production data, or code review) and the date. Do not silently
promote a target or hypothesis into a confirmed fact.
