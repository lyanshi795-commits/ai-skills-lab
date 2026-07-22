<div align="center">

# 🧩 WorkBuddy Skills 合集

**一套「工作流 + 经验沉淀」型的 Agent Skills 库**

遵循 Anthropic / OpenAI 风格 Agent Skills 规范，配合 WorkBuddy 使用

<br>

[![GitHub stars](https://img.shields.io/github/stars/lyanshi795-commits/workbuddy-skills?style=flat-square&logo=github)](https://github.com/lyanshi795-commits/workbuddy-skills/stargazers)
[![GitHub license](https://img.shields.io/github/license/lyanshi795-commits/workbuddy-skills?style=flat-square)](./LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/lyanshi795-commits/workbuddy-skills?style=flat-square)](https://github.com/lyanshi795-commits/workbuddy-skills/commits/main)
[![Skills count](https://img.shields.io/badge/skills-6-blue?style=flat-square)](./skills)
[![Repo size](https://img.shields.io/github/repo-size/lyanshi795-commits/workbuddy-skills?style=flat-square)](https://github.com/lyanshi795-commits/workbuddy-skills)

</div>

---

## 📖 这是什么

本仓库是本人用 **WorkBuddy** 沉淀的一套 Agent Skills（技能）。每个技能都是一个独立文件夹，内含：

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 指令正文（核心工作流 + 经验） |
| `scripts/` | 可选的确定性工具（脚本） |
| `references/` | 按需加载的参考资料（长文下沉） |

> 💡 **设计原则**遵循官方《The Complete Guide to Building Skills for Claude》：三级渐进式披露（frontmatter 元数据 → SKILL.md 正文 → references/scripts 按需加载），正文只留核心，长资料下沉。

---

## 📑 目录

- [⚡ 快速安装](#-快速安装)
- [📂 目录结构](#-目录结构)
- [🗂️ 技能清单](#️-技能清单)
- [🛠️ 设计方法论](#️-设计方法论)
- [📄 许可证 & 贡献](#-许可证--贡献)

---

## ⚡ 快速安装

### 方式一：克隆整库（推荐）

```bash
git clone https://github.com/lyanshi795-commits/workbuddy-skills.git
```

克隆后，把 `skills/` 下需要的技能文件夹整体复制到 WorkBuddy 技能目录：

```bash
# 用户级（所有项目通用）
cp -r workbuddy-skills/skills/<技能名> ~/.workbuddy/skills/<技能名>

# 或项目级（仅当前项目）
cp -r workbuddy-skills/skills/<技能名> <你的项目>/.workbuddy/skills/<技能名>
```

### 方式二：手动复制

直接下载本仓库，按方式一复制你需要的技能文件夹即可。

> ✅ 安装后，在 WorkBuddy 对话中直接用触发词或 `/技能名` 调用（见下方各技能说明）。

---

## 📂 目录结构

```
workbuddy-skills/
├── README.md
├── LICENSE
├── .gitignore
└── skills/
    ├── long-screenshot-ocr/      # 🔍 超长截图 OCR
    ├── miniprogram-builder/      # 💬 微信小工具从零到一
    ├── skill-building-playbook/  # 📐 搭建 Skill 的方法论（meta-skill）
    ├── gzh-cover-maker/          # 🖼️ 公众号封面图生成
    ├── gzh-infographic-maker/    # 📊 公众号对比图生成
    └── repo-topic-pipeline/      # 🧠 仓库 → 选题库 → 选题决策表
```

---

## 🗂️ 技能清单

| # | 技能 | 一句话简介 | 触发方式 |
|---|------|-----------|---------|
| 1 | `long-screenshot-ocr` | 超长截图高质量文字提取 | 「OCR 这张截图」「把长图转成文字」 |
| 2 | `miniprogram-builder` | 微信小程序从零到一工作流 | `/miniprogram-builder`、「帮我做个小程序」 |
| 3 | `skill-building-playbook` | 搭建 Skill 的方法论元技能 | `/skill-building-playbook`、「帮我做个 skill」 |
| 4 | `gzh-cover-maker` | 公众号封面图生成 | 「公众号封面」「文章封面」 |
| 5 | `gzh-infographic-maker` | 公众号双栏对比图生成 | 「公众号对比图」「双栏对比图」 |
| 6 | `repo-topic-pipeline` | 仓库转选题库与打分 | 「把仓库变成选题库」「从 GitHub 挖选题」 |

### 1. 🔍 `long-screenshot-ocr` — 超长截图文字提取

- **功能**：对手机长截图（教程页、聊天记录、课程手册）做高质量 OCR。采用「切片 + 2× 放大 + RapidOCR + 阅读顺序重建 + 噪声清洗」流水线，解决整图 OCR 漏标题、乱序、数字噪声的问题。
- **依赖**：`pip install rapidocr-onnxruntime pillow numpy`
- **用法**：
  ```bash
  python skills/long-screenshot-ocr/scripts/ocr_long_screenshot.py <图片路径> <输出md路径>
  ```
- **文件**：`SKILL.md`、`scripts/ocr_long_screenshot.py`

### 2. 💬 `miniprogram-builder` — 微信小工具从零到一

- **功能**：工作流 + 经验决策卡。把模糊想法做成可上线的微信小程序：选题决策（5 张经验卡 A–E）→ 备案/主体/类目选型 → 骨架生成（可选）→ 上线 runbook。附微信服务类目表与小程序实战手册蒸馏。
- **依赖**：可选脚手架 `scripts/generate_miniprogram.py` 需 Python 3（生成合法小程序骨架：计算器/评分/测试/生成器/自定义 5 类）。
- **用法**：对话中调用技能，按 Phase 0–7 推进；需要骨架时运行生成脚本。
- **文件**：`SKILL.md`、`references/manual_synthesis.md`、`references/wechat_service_categories.md`、`scripts/generate_miniprogram.py`、`_demo/`（生成样例）

### 3. 📐 `skill-building-playbook` — 搭建 Skill 的方法论（meta-skill）

- **功能**：元技能。把「如何搭好一个 Skill」固化为可复用工作流：skill-creator 打骨架 → 爬取/搜索沉淀 → 对标本地成熟 Skill（dbs-content / yao-demand-skill）→ 对标 Anthropic 官方规范做研究级校验。
- **依赖**：无（纯方法论 + 参考资料）。
- **用法**：对话中调用，按四步循环执行；深度规范见 `references/agent-skills-official-spec.md`。
- **文件**：`SKILL.md`、`references/agent-skills-official-spec.md`

### 4. 🖼️ `gzh-cover-maker` — 公众号封面图生成

- **功能**：从文章 hook 生成两张可直接用的 PNG：方形 1080×1080（信息流缩略图）+ 宽幅 1080×460（文章首图/分享卡）。暗金高级质感，含大数字/关键词视觉锚点与 5 要素任务 chip。
- **依赖**：`pip install pillow` + 系统中文字体（微软雅黑 / 思源黑体）。
- **用法**：对话中调用技能，按提示生成；脚本在 `scripts/`。
- **文件**：`SKILL.md`、`scripts/gzh_cover.py`、`scripts/gzh_cover_膝盖篇.py`

### 5. 📊 `gzh-infographic-maker` — 公众号对比图生成

- **功能**：生成 1080px 宽双栏对比信息图（公众号配图）。低饱和、高级感：近黑墨色 + 暖金点缀 + 克制红，圆角卡片 + 底部总结条，不依赖字体字形画勾叉。
- **依赖**：`pip install pillow` + 中文字体。
- **用法**：对话中调用技能；脚本在 `scripts/gzh_infographic.py`。
- **文件**：`SKILL.md`、`scripts/gzh_infographic.py`

### 6. 🧠 `repo-topic-pipeline` — 仓库转选题库

- **功能**：把任意 GitHub 仓库（或本地文档/代码目录）变成结构化、可检索的素材库，再跑四阶段流水线产出「排序后的选题决策表」：① 素材采集 ② 选题挖掘（多视角）③ 五维打分 ④ 分类输出（Markdown + CSV）。
- **依赖**：Python 3（本地打分工具，透明权重）；详见 `scripts/`。
- **用法**：对话中调用技能；脚本 `extract_materials.py`、`score_topics.py`。
- **文件**：`SKILL.md`、`scripts/extract_materials.py`、`scripts/score_topics.py`

---

## 🛠️ 设计方法论

搭新技能的标准四步，不跳步：

1. **🦴 skill-creator 打骨架** —— 先 scaffold，保证 frontmatter / 目录格式正确。
2. **📥 爬取 / 搜索 / 沉淀** —— 把领域经验灌进 `references/`，正文只留核心（三级渐进式披露）。
3. **🎯 对标本地成熟 Skill（必须先做）** —— 学 `dbs-content`（哲学 → Phase → 反面案例 → 说话风格）、`yao-demand-skill`（路由边界 → 输出契约 → Reference Map）。缺哪样补哪样。
4. **✅ 对标官方规范做研究级校验** —— 逐条核对 agentskills.io 规范 + Anthropic 白皮书。

> **官方硬约束速记**：`name` 用 kebab-case ≤ 64 字符、与目录同名；`description` 必含【做什么】+【何时用】+ 触发词、≤ 1024 字符；正文 < 500 行；文件夹内不放 README；三级披露（元数据常驻 / 正文触发 / references 按需零 token）。安全上，社区约 26.1% 的技能含漏洞、带脚本的是纯指令的 2.12 倍——只信来源、审计捆绑文件。

---

## 📄 许可证 & 贡献

本项目以 **MIT 许可证** 开源，见 [LICENSE](./LICENSE)。

> ⚠️ 本仓库仅包含**本人创建**的技能（`agent_created: true`）。第三方技能（dbs-*、yao-*、市场安装的 skill_* 等）不在此仓库内，版权归各自作者。

🤝 欢迎提 Issue / PR。新增或修改技能请遵循上方「设计方法论」四步，并保证 `SKILL.md` 符合官方规范（正文 < 500 行、frontmatter 完整）。
