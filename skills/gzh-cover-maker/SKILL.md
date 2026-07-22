---
name: gzh-cover-maker
description: Generate hook-driven WeChat public account cover images (PNG) from article themes. Use when the user asks for 公众号封面, 封面图, 公众号首图, 文章封面, or requests a cover image for a WeChat article. Produces a 1080x1080 square feed thumbnail and a 1080x460 wide article-top/share-card cover using Python + Pillow with Microsoft YaHei fonts and a premium dark brand palette.
agent_created: true
---

# gzh-cover-maker

## Overview

Generate high-conversion WeChat cover images that stand out in the subscription feed on mobile. The skill turns an article hook into two ready-to-use PNGs:

1. **Square 1080x1080** — subscription feed thumbnail (竖屏信息流缩略图)
2. **Wide 1080x460** — article top banner / share card (文章首图 / 分享卡)

The default visual style is a dark premium background with warm gold accents, a large numeric or keyword visual anchor, suspenseful copy, and 5-element task chips. This matches the brand palette already used for the content Agent project (ink + gold + cream + muted red).

## When to Use

Trigger this skill when the user asks for:
- "公众号封面图"
- "封面图"
- "设计一张封面"
- "公众号首图"
- "文章封面"
- Any request to create a WeChat article cover image with a hook/clickable effect

## Required Input

Before running, clarify or infer:
- **Article hook / main title** (required): the single sentence that becomes the cover headline
- **Numeric hook** (optional): a number that creates curiosity (e.g., 5 questions, 3 mistakes, 7 steps). If absent, use a word anchor.
- **Supporting chips** (optional): 3-5 short labels that prove the hook (e.g., 目标 / 材料 / 流程 / 边界 / 验收). If absent, infer from the article theme or omit.
- **Output directory** (required): where to save the two PNGs
- **Brand color override** (optional): provide a hex color if the default gold (#bf9b5f) is not appropriate

## Workflow

1. **Confirm the article hook.** If the user says "above article" or the article is ambiguous, check the most recent article context or ask for the title.
2. **Run the generator.** Use `scripts/gzh_cover.py` via the Python venv at `C:/Users/User/.workbuddy/binaries/python/envs/default/Scripts/python.exe`.
3. **Customize the generated script if needed.** The script is self-contained. To change copy or chips, edit the `build_square` and `build_wide` functions in the script before running.
4. **Verify visually.** Read the two PNGs to ensure text is legible and the hook is clear at thumbnail size.
5. **Deliver.** Attach both PNGs and explain which size is for which use case.

## Default Design Recipe

- **Background:** dark ink gradient (#1c1b19 → #241f18) with a warm gold radial glow in the upper-right for premium contrast in the feed
- **Grid:** very subtle vertical guide lines (low opacity) to add texture without noise
- **Top-left badge:** series index, e.g., "第五篇 · 内容 Agent 验证", gold outline pill
- **Top-right hook tag:** a red/muted red pill with a contradiction, e.g., "模糊需求 ≠ 任务"
- **Headline:** 2-3 short lines, white/cream, large bold font, left-aligned
- **Visual anchor:** an oversized gold number (e.g., "5") or keyword with an underline bar
- **Proof chips:** 5 small gold-outline pills at the bottom showing the supporting elements
- **Footer:** brand line + a curiosity question (e.g., "为什么是 5 个？") to leave an open loop

## Usage Example

```bash
C:/Users/User/.workbuddy/binaries/python/envs/default/Scripts/python.exe \
  C:/Users/User/.workbuddy/skills/gzh-cover-maker/scripts/gzh_cover.py
```

The script writes two files to the configured `OUT` directory. To point it elsewhere, edit the `OUT` variable at the bottom of `gzh_cover.py`.

## Notes

- Fonts are Microsoft YaHei (msyh.ttc / msyhbd.ttc) on Windows. The script falls back to the regular font if the bold face is missing.
- The design is intentionally dark because dark covers have higher contrast in the WeChat subscription feed.
- Keep cover text to a few lines only; the feed thumbnail is very small on mobile.
- If the article is not about the five-element framework, replace the five bottom chips with the most relevant short labels or remove them.
