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
v0.3 开发版。自动发现支持常规单层全局 Skill 目录和简单 name 元数据，不是完整 YAML 解析器。路径发现不代表 Codex 能读取或运行 Skill。doctor 只检查版本与登录状态，不调用模型。客户端自动触发、真实委派、网络权限和专属工具仍需本地验证。暂不支持会话续接和并发控制。详见英文 README 和 evals/README.md。
