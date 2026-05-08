# Assessment Submission Coach Plugin

Codex plugin package for coaching Agentic AI Foundations learners through a competency-based assessment submission.

## Contents

- `.codex-plugin/plugin.json`: plugin manifest
- `skills/assessment-submission-coach/`: coaching skill, assessment blueprint, learner template, and completeness checker
- `templates/`: Appendix A Word templates from `AppendixA_Templates_Agentic_AI_Foundations_v1.1.zip`

## Install In Codex App

Install the plugin folder itself, not the repository root.

1. Download or clone the `accountant-ai-playbook` repository.
2. In Codex App, choose the option to add or install a local plugin.
3. Select this folder:

```text
accountant-ai-playbook/plugins/assessment-submission-coach-plugin
```

4. Confirm this manifest exists inside the selected folder:

```text
.codex-plugin/plugin.json
```

5. Restart or refresh Codex App if the plugin does not appear immediately.

Do not select the repo root:

```text
accountant-ai-playbook
```

That folder does not contain the plugin manifest at its top level.

## Prompt Codex To Install

If a learner wants Codex to help install the local plugin, they can paste:

```text
Install the local Codex plugin from this folder:
<full-path-to-accountant-ai-playbook>/plugins/assessment-submission-coach-plugin

Check that .codex-plugin/plugin.json exists, then help me enable the Assessment Submission Coach plugin in Codex App.
```

On Windows, the path may look like:

```text
C:\Users\<your-name>\Downloads\accountant-ai-playbook\plugins\assessment-submission-coach-plugin
```

## Common Install Issues

- The wrong folder was selected. Select `plugins/assessment-submission-coach-plugin`, not `accountant-ai-playbook`.
- The `.codex-plugin` folder is missing because files were copied manually. Download the GitHub ZIP or use `git clone`.
- The repository ZIP was not extracted before installation.
- Codex App needs to be refreshed or restarted after adding the plugin.

## Use Case

Use this plugin when a learner needs help preparing, reviewing, improving, or packaging the final Agentic AI Foundations assessment portfolio.

The final learner submission should be a single PDF and must use only dummy or anonymized data.

## Safety Boundary

Do not include real personal data, confidential client information, API keys, passwords, private URLs, or screenshots containing secrets in learner submissions or reusable examples.
