# Agent Skills 官方规范与最佳实践（沉淀）

> 本文件是 2026-07-22 系统学习 Anthropic / 学术界 Agent Skills 文献后的蒸馏笔记。
> 用途：未来搭建任何 Skill 时，先对标本文件 + 本地成熟 Skill（见 `skill-building-playbook` 的 Benchmark 清单）。
> 这不是给用户看的前台内容，是给「搭 Skill 的 AI」自己用的内部规范。

## 已研读来源
1. Anthropic 官方 32 页白皮书《The Complete Guide to Building Skills for Claude》
2. agentskills.io 开放规范（open standard）
3. Claude 官方博客《Building Agents with Skills: Equipping Agents for Specialized Work》
4. Anthropic 工程博客《Equipping agents for the real world with Agent Skills》
5. platform.claude.com 文档（frontmatter 硬约束 / 三级 Token 预算）
6. arXiv 2602.12430 综述《Agent Skills for LLMs: Architecture, Acquisition, Security, and the Path Forward》
7. arXiv 2602.20867 SoK《Agentic Skills -- Beyond Tool Use in LLM Agents》

---

## 1. 一句话定义
Skill = 一个文件夹，核心是 `SKILL.md`（YAML frontmatter + Markdown 指令），可选 `scripts/ references/ assets/`。
类比：**给新入职同事的入职指南**——把领域专长 / 工作流 / 经验封装成可复用、按需加载的包。
"Building a skill is like putting together an onboarding guide for a new hire."

## 2. 渐进式披露（核心原则，三级）
- **L1 元数据**（YAML frontmatter 的 `name`+`description`）：常驻系统提示，~50–100 token/skill，只告诉模型「何时用」。
- **L2 SKILL.md 正文**：命中触发时才读入，~500 token；**建议 <5000 token、<500 行、<5000 词**。
- **L3 references/ scripts/ assets/**：按需读 / 执行，2k+ token 只在需要时，未使用 = 零 token。
准则：上下文里只留「相关的」，没用到的文件不占任何 token。

## 3. 目录结构（白皮书硬规则）
```
skill-name/               # kebab-case，与 name 一致
├── SKILL.md              # 必须，精确拼写，大小写敏感
├── scripts/              # 可选：Python/Bash 确定性工具
├── references/           # 可选：按需加载的文档
└── assets/               # 可选：模板/字体/图标
```
硬规则：
- 文件必须叫 `SKILL.md`（`SKILL.MD`/`skill.md` 都错）。
- 文件夹 kebab-case：无空格、无下划线、无大写。
- **技能文件夹内不要放 README.md**（分发时仓库级 README 另算）。
- 参考文件用相对路径、一级深度引用。

## 4. Frontmatter 字段规范
**必填：**
- `name`：kebab-case，≤64 字符，只允许小写字母/数字/连字符；不能含 XML 标签；不能用保留词 `claude`/`anthropic`；应与文件夹同名。
- `description`：必填，≤1024 字符，不能含 XML 标签；**必须同时写【做什么】+【何时用（触发条件）】**；包含用户会说的原话触发词、相关文件类型。

**可选：**
- `license`：开源用，如 `MIT` / `Apache-2.0`
- `compatibility`：1–500 字符，环境要求（目标产品、系统依赖、网络需求）
- `metadata`：自定义键值，建议 `author`/`version`/`mcp-server`/`category`/`tags`
- `allowed-tools`：限制工具访问，如 `Bash(python:*) Bash(npm:*) WebFetch`

**安全：** frontmatter 禁 XML 尖括号（防注入）；禁 `claude`/`anthropic` 前缀（保留词）。

## 5. description 公式（决定触发质量）
结构 = **[做什么] + [何时用] + [关键能力]**。
- 好：「Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for 'design specs', 'component documentation', or 'design-to-code handoff'.」
- 坏（太虚）：「Helps with projects.」
- 坏（缺触发）：「Creates sophisticated multi-page documentation systems.」
- 坏（太技术无用户触发）：「Implements the Project entity model with hierarchical relationships.」
- 过多触发 → 加负面触发（Do NOT use for ...）；过少触发 → 加关键词 / 同义说法。

## 6. SKILL.md 正文推荐结构（白皮书模板）
```
# Skill Name
## Instructions
### Step 1: ...
  步骤 + 示例命令 + Expected output
## Examples
  Example 1: [场景]  User says: ...  Actions: ...  Result: ...
## Troubleshooting
  Error: ...  Cause: ...  Solution: ...
```
正文写作守则：
- **具体可执行**：给确切命令 / 参数，而非「验证一下数据」。
- **含错误处理**：常见错误 + 原因 + 解法。
- **关键指令放最前**，用 `## Critical` / `## Important` 强调；可重复关键点。
- **用渐进式披露**：核心留 SKILL.md，细节移 `references/` 并链接。
- 避免冗长 / 歧义；模糊处用代码脚本替代语言指令（代码确定、语言不一定）。
- 针对模型「偷懒」可加 Performance Notes（但加在用户提示比 SKILL.md 更有效）。

## 7. 规划：先用例，再写码
- 动手前先定 **2–3 个具体用例**（触发句 + 步骤 + 结果）。
- 三大用例类别（Anthropic 观察）：
  - 类别1 文档 / 资产创建（用内置能力，无需外部工具）
  - 类别2 工作流自动化（多步、带校验门、迭代改进）
  - 类别3 MCP 增强（给 MCP server 配工作流知识）
- 定义成功标准：量化（触发命中率 ≥90%、工具调用数、0 失败 API）+ 质化（无需提示下一步、无需纠错、跨会话一致）。

## 8. 五种实战模式（白皮书）
1. **Sequential workflow orchestration**：固定顺序多步，每步校验 + 失败回滚。
2. **Multi-MCP coordination**：跨多服务分阶段，阶段间传数据、集中错误处理。
3. **Iterative refinement**：先草稿 → 质量脚本校验 → 修复循环 → 直到达阈值。
4. **Context-aware tool selection**：决策树按上下文选工具 + fallback + 透明说明。
5. **Domain-specific intelligence**：先领域规则 / 合规检查，再动作，留审计轨迹。

## 9. 七种系统级设计模式（SoK 2602.20867，更抽象）
1. **Metadata-Driven Disclosure**（= L1/L2）
2. **Code-as-Skill**（可执行脚本，确定、可测）
3. **Workflow Enforcement**（硬门控流程，换灵活换可靠）
4. **Self-Evolving Skill Libraries**（执行后自动评估 + 蒸馏新技能）
5. **Hybrid NL+Code Macros**（Markdown 含 NL + 代码块，注意边界歧义）
6. **Meta-Skills**（创建 / 修改 / 组合其他技能；递归错误放大风险）
7. **Plugin/Marketplace Distribution**（带依赖 / 兼容 / 治理元数据；供应链风险）

## 10. 测试方法论
三档 rigor：手动(Claude.ai) / 脚本化(Claude Code) / 程序化(API 评估套件)。
推荐覆盖三类：
- **触发测试**：✅ 明显任务 ✅ 同义改写 ❌ 不相关话题。
- **功能测试**：输出正确、API 成功、错误处理、边界。
- **性能对比**：对比开 / 关 skill 的工具调用数、token、失败数。
Pro tip：**先在一个难任务迭代到成功，再扩到多用例**（利用 in-context learning）。
迭代信号：欠触发（描述加关键词）/ 过触发（加负面触发、更具体）/ 执行问题（改进指令 + 错误处理）。
**负面测试清单**（arXiv 12430，确认「只做声称的、不多做」）：
- 幻觉流程 / 级联执行失败 / 冲突 skill 死锁 / 静默权限提升 / 对抗性 skill 链式组合。

## 11. 安全与信任（重点，来自两篇论文）
- **像装软件一样对待 skill**：只用可信来源（自建 / Anthropic / 已审计伙伴）。
- 审计所有捆绑文件（SKILL.md、脚本、资源）：异常网络调用、文件访问模式、与声明目的不符的操作。
- 外部 URL 取数风险高（内容可能含恶意指令）。
- **实证**：SkillScan 分析 31,132 个社区 skill，**26.1% 含至少一种漏洞**（提示注入 / 数据外泄 13.3% / 权限提升 11.8% / 供应链）；带脚本的 skill 漏洞率是指令-only 的 **2.12×**。
- **信任分级（T1–T4，最小权限）**：T1 未审社区 = 仅元数据 + 全隔离 + 绝不授脚本；T2 可读 L2 指令仍无脚本；T3 可跑 L3 脚本；T4 厂商认证 = 完整权限。非二元。
- **治理门（G1–G4）**：静态分析 → LLM 语义分类 → 行为沙箱 → 权限清单比对。
- **ClawHavoc 案例**：~1200 恶意 skill 渗入大市场，偷 API key / 钱包 / 凭证 → 用四层信任 + 沙箱 + 溯源验证防。
- **评估发现**：策展（curated）技能平均 **+16.2pp** 通过率，小模型配 curated 可超无 skill 大模型；自生成（self-generated）技能 **-1.3pp**（可能编码错误 / 过特化启发式）。

## 12. 评估指标（可复用性）
- **reusability**（泛化到未见任务）
- **composability**（能与其他 skill 组合）
- **maintainability**（跨环境鲁棒）
- 触发准确率（单 agent 管理 skill 数有上限——相位转变，别贪多）

## 13. 分发
- 开源：GitHub 公开仓库 + 仓库级 README（安装说明 + 截图）+ 示例；**技能文件夹内不放 README.md**。
- 组织级：管理员可 workspace 级部署、自动更新。
- API：`/v1/skills` 端点 + `container.skills` 参数；需 Code Execution Tool beta。
- 定位：讲结果不讲功能（「几秒搭好项目空间」而非「一个含 YAML 的文件夹」）。

## 14. 快速自检清单（白皮书 Reference A）
- **开始前**：2–3 用例、工具、结构规划。
- **开发中**：kebab-case 文件夹、SKILL.md 精确名、frontmatter 有 `---`、name kebab、description 含 WHAT+WHEN、无 XML、指令清晰、含错误处理、有示例、references 链接清晰。
- **上传前**：触发测试（明显 / 同义 / 不相关）、功能测试、工具集成、zip。
- **上传后**：真实对话测、监控过 / 欠触发、收反馈、迭代、metadata 升版本。

## 15. 与 MCP 的关系（正交）
- MCP = 连通性（工具 / 数据访问）；Skill = 程序性知识（怎么做）。
- 厨房类比：MCP 是专业厨房（工具 / 食材 / 设备），Skill 是菜谱（怎么做）。
- 可同时用：MCP 给工具，skill 教怎么用工具。
