# CodexDispatch

Antigravity-first global skill for deciding when to delegate work to Codex CLI. Research and general complex-task guidance are loaded on demand. Native agent planning remains in charge.

## Installation
Requires Python 3.10+ and an authenticated Codex CLI. Copy the repository to your actual Antigravity global skills directory as `codex-dispatch`. Confirm SKILL.md is discovered and Python and Codex are available in the terminal. Client-specific installation paths are intentionally not assumed. If automatic discovery is unreliable, explicitly invoke the skill or add a short global rule to consult it before delegation.

## Example
Save a task manifest with actual absolute paths:
```json
{
  "objective": "Implement and test the agreed ablation experiment",
  "workspace": "/absolute/path/to/research-project",
  "context": "Read experiment_design.md and preserve the protocol",
  "skills": [],
  "sandbox": "workspace-write",
  "deliverables": ["experiment script", "test report"],
  "acceptance_criteria": ["Tests pass", "Raw data unchanged"],
  "timeout_seconds": 1800
}
```
Run `python scripts/dispatch.py task.json --dry-run` to preview and `python scripts/dispatch.py task.json` to execute. Enable workspace-write only for authorized edits. Logs and task manifests are stored under ~/.codex-dispatch/runs/ and may contain sensitive context. Do not publish them. Existing global skills are referenced by absolute directory path, not reinstalled.

## Usage examples
- 和我讨论这个科研 idea。
- 实验设计确定了，让 Codex 实现并测试。
- 使用我全局安装的审稿 Skill，让 Codex 审稿。
- 这次代码你自己写。

## Scope
v0.2.0 development prototype: prompt-guided routing, two workflow modules, manifest validation, CLI invocation, status/log capture. No daemon, independent planner, automatic skill discovery, session resume or concurrency locking. CLI flags and live invocation need local verification. Timeout terminates the direct subprocess; child-process cleanup is not guaranteed. Use serial execution and inspect partial changes before retrying. A successful CLI exit is not scientific validation.

## Tests
`python -m unittest discover -s tests -v`


## Routing and evaluation
The main skill loads references/routing-policy.md and scenario workflows on demand. Professional skills remain in the Antigravity global library. See evals/README.md for 20 behavioral test cases and the proposed release gate. The cases are specified, not yet measured against a live host. Global skill discovery remains agent-driven; there is no separate registry or automatic resolver script.
