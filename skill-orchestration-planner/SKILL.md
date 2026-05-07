---
name: skill-orchestration-planner
description: Plan orchestration of multiple skills across a workflow using AGENTS.md and skillset.md; use when coordinating skills, defining end-to-end pipelines, or designing skill interactions and handoffs.
---

# Skill Orchestration Planner

## Purpose
Design an end-to-end orchestration plan that coordinates multiple skills, their triggers, inputs/outputs, and handoffs, grounded in the local AGENTS.md and any skillset.md.

## Inputs to Locate
- `AGENTS.md` (local instructions; treat as authoritative for constraints).
- `skillset.md` (skill inventory, dependencies, and expected outputs). If missing, draft a minimal skillset from context and flag gaps.

## Output (Default)
Create `orchestration_plan.md` in the current working directory containing:
- Goal and scope
- Assumptions and constraints (from AGENTS.md)
- Skill inventory (from skillset.md)
- Orchestration graph (text or mermaid)
- Step-by-step execution plan with inputs/outputs
- Artifact handoffs (files, schemas, formats)
- Failure modes + fallback paths
- Next steps

## Workflow
1. **Read constraints**: Open `AGENTS.md` and extract relevant rules (skills, tools, approvals, file paths).
2. **Load skillset**: Open `skillset.md`. If absent, compile an inferred skill list from the user request and current repo context.
3. **Map dependencies**: For each skill, note triggers, required inputs, outputs, and downstream consumers.
4. **Sequence the flow**: Order the skills and identify parallelizable steps. Include checkpoints for validation.
5. **Draft plan**: Produce `orchestration_plan.md` using the default output structure.
6. **Call out unknowns**: Explicitly list missing inputs, unclear dependencies, or required decisions.

## Orchestration Plan Template
Use this structure inside `orchestration_plan.md`:

- **Goal**
- **Scope**
- **Assumptions/Constraints**
- **Skill Inventory** (name, trigger, inputs, outputs)
- **Orchestration Graph** (text or mermaid)
- **Execution Plan** (step-by-step)
- **Artifacts & Handoffs**
- **Risks & Fallbacks**
- **Open Questions / Decisions**

## Notes
- Keep the plan concise and actionable; avoid duplicating skill definitions.
- Prefer absolute paths for artifacts when AGENTS.md requires it.
- If a skill requires additional resources (scripts, references, assets), flag that in Open Questions.
- For common graphs and sequencing patterns, see `references/orchestration-patterns.md`.
