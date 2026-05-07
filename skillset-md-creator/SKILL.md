---
name: skillset-md-creator
description: Create or update skillset.md files that define a skills inventory, trigger phrases, inputs/outputs, dependencies, global conventions, and orchestration constraints for workflow planning. Use when asked to build, standardize, or revise a skillset.md for a project or skill collection.
---

# Skillset.md Creator

## Overview
Create a clear, consistent `skillset.md` that describes available skills and how they connect for orchestration planning.

## Workflow
1. Discover context
- Locate the target `skillset.md` path if provided; if updating, read it first and preserve ordering and tone.
- Identify skills in scope by scanning skill folders or a provided list. Read each skill's `SKILL.md` frontmatter and any orchestration notes (for example `skills_end_to_end_plan.md`).
- If the user provides an example `skillset.md`, treat it as the house style.

2. Build the Skills Inventory
- Start from `assets/skillset_template.md` and fill one block per skill.
- For each skill, include all required fields: description, trigger phrases, inputs, outputs, upstream dependencies, downstream consumers, key files, notes.
- Use concrete file names and paths (Windows backslashes if the repo uses them).
- Keep skill names lowercase and consistent with folder names.
- Use 2-4 trigger phrases per skill that match how a user would ask for the capability.

3. Fill Global Conventions
- Specify output directory, shared config files, naming conventions, and versioning rules.
- If unknown, write `none` or `not specified` (do not leave placeholders like TBD).

4. Define Orchestration Constraints
- State parallelizable steps, required sequencing, validation checkpoints, and failure handling.
- If only partial knowledge is available, infer the minimum safe sequencing from dependencies and mark the rest as `not specified`.

5. Validate before finalizing
- Every dependency referenced must exist in the inventory.
- Upstream and downstream relationships should be consistent.
- Outputs from one skill should plausibly feed inputs of downstream skills.
- Use consistent heading levels and bullet formatting.

## Update guidance
- Preserve existing order (alphabetical or pipeline order).
- When adding a skill, update any downstream/upstream references impacted by the change.
- Avoid inventing dependencies; if unknown, mark as `not specified` in Notes.

## Resources
- `assets/skillset_template.md` for the base structure.
- `references/skillset_checklist.md` for final QA checks.
