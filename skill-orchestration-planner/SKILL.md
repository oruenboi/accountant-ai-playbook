---
name: skill-orchestration-planner
description: Create or update skills-catalog.md files and plan orchestration of multiple skills across a workflow using AGENTS.md, SKILL.md files, and optional catalog notes; use when coordinating skills, defining end-to-end pipelines, documenting skill inventories, or designing skill interactions and handoffs.
---

# Skill Orchestration Planner

## Purpose
Create or update a `skills-catalog.md`, then design an end-to-end orchestration plan that coordinates multiple skills, their triggers, inputs/outputs, dependencies, validation gates, and handoffs. Ground the output in local `AGENTS.md`, existing skill folders, each skill's official `SKILL.md`, and any existing catalog notes.

`skills-catalog.md` is a human-maintained planning artifact. It is not an official agent runtime file and should not be treated as a replacement for each skill's `SKILL.md`.

## Inputs to Locate
- `AGENTS.md` (local instructions; treat as authoritative for constraints).
- Skill folders containing `SKILL.md` files.
- `skills-catalog.md` (optional inventory, dependencies, and expected outputs). If missing, create one when requested or draft a minimal inferred inventory inside the plan and flag gaps.
- Existing orchestration notes, plans, or examples provided by the user.

## Outputs
- `skills-catalog.md` when the user asks to create, update, standardize, or audit a skill inventory.
- `orchestration_plan.md` when the user asks to plan a multi-skill workflow, pipeline, or handoff model.

## skills-catalog.md Requirements
Use `assets/skills_catalog_template.md` as the base structure. For each skill, include:
- Description
- Trigger phrases
- Inputs
- Outputs
- Upstream dependencies
- Downstream consumers
- Key files
- Notes

Fill global conventions and orchestration constraints. If a value is unknown, write `not specified`; do not leave placeholders such as TBD.

## orchestration_plan.md Requirements
Create `orchestration_plan.md` in the current working directory containing:
- Goal and scope
- Assumptions and constraints (from AGENTS.md)
- Skill inventory (from `SKILL.md` files and `skills-catalog.md`, when present)
- Orchestration graph (text or mermaid)
- Step-by-step execution plan with inputs/outputs
- Artifact handoffs (files, schemas, formats)
- Failure modes + fallback paths
- Next steps

## Workflow
1. **Read constraints**: Open `AGENTS.md` and extract relevant rules (skills, tools, approvals, file paths).
2. **Discover skills**: Scan skill folders or a provided skill list. Read each `SKILL.md` frontmatter and any orchestration notes.
3. **Load or create catalog**: Open `skills-catalog.md` if present. If the user requested a skill inventory, update or create it before planning.
4. **Build the inventory**: Record triggers, inputs, outputs, upstream dependencies, downstream consumers, key files, and notes.
5. **Validate relationships**: Dependencies must reference known skills, and upstream outputs should plausibly feed downstream inputs. Use `references/skills_catalog_checklist.md`.
6. **Map orchestration**: Choose the appropriate sequencing pattern from `references/orchestration-patterns.md`, including parallel steps and validation checkpoints.
7. **Draft plan**: Produce `orchestration_plan.md` when requested, using the plan template below.
8. **Call out unknowns**: Explicitly list missing inputs, unclear dependencies, or required decisions.

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
- Preserve existing `skills-catalog.md` ordering and tone when updating a file.
- Use 2-4 user-facing trigger phrases per skill.
- Avoid inventing dependencies; if unknown, mark them as `not specified` in Notes.
- For common graphs and sequencing patterns, see `references/orchestration-patterns.md`.
