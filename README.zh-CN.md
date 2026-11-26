# CodexDispatch
Antigravity 全局调度 Skill。主控使用原生规划能力，在合适的执行节点委派 Codex CLI。科研和通用复杂任务是两个按需加载的工作流。

## 安装
准备 Python 3.10+、已登录的 Codex CLI。克隆本仓库，确认 Antigravity 实际使用的全局 Skill 目录，再运行：
```bash
python scripts/install.py "<全局 Skill 目录>"
```
安装器只复制新目录，已有安装请人工检查后更新。进入安装后的 codex-dispatch 文件夹：
```bash
python scripts/doctor.py
python scripts/skill_resolver.py
python scripts/skill_resolver.py peer-review
```
自动发现默认扫描与本 Skill 同级的目录。额外全局目录可使用 --root 或环境变量 CODEX_DISPATCH_SKILL_ROOTS（系统路径分隔符分隔）。名称冲突时明确选择实际目录。不会安装或修改其他 Skill。

## 日常使用
- 和我讨论这个科研 Idea。
- 实验设计确定了，交给 Codex 实现和测试。
- 使用我全局安装的审稿 Skill，让 Codex 审稿。
- 这次代码你自己写。

主控选择任务边界、传递上下文和 Skill 路径，Codex 自主执行。论文写作与审稿动态选择。权限和工具兼容性需要检查。

## 当前限制
v0.5 试用候选版。自动发现支持常规单层全局 Skill 目录和简单 name 元数据，不是完整 YAML 解析器。路径发现不代表 Codex 能读取或运行 Skill。doctor 只检查版本与登录状态，不调用模型。客户端自动触发、真实委派、网络权限和专属工具仍需本地验证。会话续接为实验功能，默认关闭。暂不支持并发控制。详见英文 README 和 evals/README.md。

## 会话与恢复
每次调用记录任务、状态、JSONL 事件、错误日志和最终回复（如生成）。在本地验证当前 CLI 的沙箱约束后，设置环境变量 CODEX_DISPATCH_ENABLE_RESUME=1，使用 `python scripts/dispatch.py next-task.json --resume-run run-实际ID` 续接已完成的任务。必须保持工作目录和沙箱权限一致。默认新建会话。失败或超时后先检查文件变化及残留子进程，再决定是否重试。详见 references/session-policy.md。

## 本地联调
参考 [本地试用与验收](docs/local-smoke-test.zh-CN.md)。可选的 [全局调度规则](references/global-rule.md) 由用户自行添加。GitHub Actions 执行跨平台单元测试；实际模型行为和沙箱仍需本地验证。安装器只复制运行文件，测试和完整文档请在源码仓库查看。
