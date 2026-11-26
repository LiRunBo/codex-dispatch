---
name: codex-dispatch
description: Select when to delegate substantial executable work to local Codex CLI from Antigravity. Use when the user names Codex, assigns an executor, or an authorized research or complex task reaches an implementation handoff. Preserve native planning and ordinary professional skill usage.
---
# Codex Dispatch

Antigravity is the coordinator. Use native planning, reasoning and tools. This skill supplies delegation guidance and transport.

## Decide
- Read [routing policy](references/routing-policy.md) when considering delegation or an executor override.
- For research, read [research workflow](workflows/research.md). For other complex work, read [complex task workflow](workflows/complex-task.md). Load only relevant guidance.
- Separate discussion, planning and authorized execution. Honor explicit executor choice within its stated scope. Keep simple native tasks native unless explicitly delegated. Select cohesive handoff boundaries and avoid duplicate planning.
- If a professional skill is involved in a handoff, read [skill bridge](references/skill-bridge.md). Resolve existing global skill paths and dependencies. Preserve ordinary native skill use. Use `python <this-skill-directory>/scripts/skill_resolver.py <exact-skill-name>` for automatic sibling discovery; use `--root <actual-global-root>` when needed. Use doctor.py for preflight when setup is uncertain.

## Delegate
- Check feasibility, authorization, inputs and acceptance criteria. Briefly announce substantial handoffs. Never silently replace an explicitly selected executor.
- Create the JSON manifest described in [README](README.md) with actual absolute paths, relevant context, permitted changes, outputs and acceptance criteria. Use read-only by default; workspace-write only for authorized edits.
- Run `python <this-skill-directory>/scripts/dispatch.py <manifest-path>`. Preview with `--dry-run`. Preserve Codex native planning; prohibit recursive use of this dispatcher. Never bypass sandbox or approval controls.

## Return
Inspect status, logs, actual files and tests. Check acceptance criteria and scientific evidence before reporting success. Reassess the native plan when results change assumptions. Inspect partial writes before retrying. Report real blockers. Do not claim a handoff or completed work without execution evidence.
