# Session and recovery policy

Start a fresh Codex session by default. A related follow-up can use the previous local run only when the user or coordinator has selected it unambiguously, the previous turn completed, the workspace and sandbox are unchanged, and the user has enabled experimental resume after validating their installed CLI version.

The executor records thread.started and turn.completed/turn.failed from JSONL. It requires a successful exit, completion event and final response file to mark a run completed. This is transport completion, not artifact acceptance. The status records a session ID only when the event stream identifies exactly one valid UUID.

To opt in after testing the local version, set CODEX_DISPATCH_ENABLE_RESUME=1 and pass --resume-run run-... along with a new manifest. Resume uses an explicit sandbox_mode config; CLI versions differ in support and enforcement. Test read-only refusal and workspace-write boundaries in a disposable workspace before enabling. Disable again after CLI upgrades until retested. Never use --last or widen permissions to make resume work. Start a fresh session if permissions must change or the correct session cannot be established; include necessary context in the manifest. Inform the user of material fallback.

On timeout, interruption or failure, inspect logs and actual workspace modifications, and check for surviving child processes. Do not retry automatically or assume rollback. The dispatcher terminates the direct subprocess on timeout; descendant cleanup is not guaranteed. Avoid simultaneous runs in the same workspace. A completed session may have newer turns outside this dispatcher; verify the session is still appropriate before reuse.

Run data under ~/.codex-dispatch/runs is private local research material; do not publish it. CLI output and session history can contain sensitive content.
