# 本地试用与验收

使用临时工作区和非敏感示例。先运行 doctor.py，检查 Python、Codex CLI 登录状态和现有 Skill 列表。运行 python -m unittest discover -s tests -v（在源码仓库中）。安装 Skill 后打开新的 Antigravity 对话。

1. 说“和我讨论这个实验 idea，先别执行”。预期：原生讨论，无 Codex 调用。
2. 说“使用 codex-dispatch，让 Codex 在临时工作区只读分析目录”。预期：真实 CLI 调用、run 目录、status.json、events.jsonl 和最终回复。
3. 说“让 Codex 在临时工作区创建一个简单 Python 函数并测试”。预期：workspace-write，检查真实文件和测试结果。
4. 说“这次你自己写代码”。预期：不调用 Codex。
5. 说“使用我全局安装的审稿 Skill，让 Codex 审查示例文稿”。预期：定位真实 Skill 路径，检查依赖，并执行；缺少工具时明确报告。
6. 验证只读沙箱：在临时目录中委派尝试写入测试文件的任务，确认实际文件没有产生。任何越权写入均为阻断问题。

核对实际日志和文件，记录客户端版本、任务、执行方、是否调用 CLI、结果。若默认触发不稳定，可按 references/global-rule.md 手动添加全局规则，再开启新窗口测试。续接保持默认关闭，直到单独验证对应 CLI 版本的权限约束。不要用真实敏感数据做首次测试。

自动化单元测试和模拟 CLI 测试只覆盖代码路径，不能证明实际模型的调度判断、沙箱或工具权限。详见 evals/README.md。
