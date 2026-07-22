---
name: gzh-infographic-maker
license: MIT
compatibility: 适用于 WorkBuddy / Claude Code / 任意 agentskills.io 兼容运行时
metadata:
  author: SHR
  collection: SHR Skills
  version: 1.0.0
agent_created: true
description: Generate high-end 1080px-wide PNG comparison infographics for WeChat public account (公众号) articles. Use this skill when the user asks for 公众号配图, 对比图, 双栏对比, or infographic images with two columns and a bottom caption bar. The skill produces low-saturation, premium-looking images using Python + Pillow + Microsoft YaHei fonts, without relying on font glyphs for check/cross markers.
---

# 公众号对比图生成器

## Overview

Generate two-column comparison infographics sized for WeChat public account full-width images (1080px). The style is restrained and premium: near-black ink, warm gold accent, muted red for the "before" side, rounded cards, and a bottom summary bar.

## When to use

Trigger this skill when the user asks for:

- 公众号配图 / 公众号对比图
- 双栏对比图 / 左右对比图
- 生成对比图 PNG
- 把两张对比做成图片
- 在公众号图片位插入对比图

## Workflow

1. **Identify the two sides**. Ask for (or infer from the user's context):
   - Title and subtitle
   - Left column header + items (missing/problem side)
   - Right column header + items (solution/structured side)
   - Bottom caption line
   - Which article 图片位 (placeholder) the image should slot into

2. **Edit the script data** in `scripts/gzh_infographic.py`. Replace the hardcoded `left1/right1` and `left2/right2` dicts with the new content. Keep the same structure:
   - `header`: column title
   - `accent`: RED or GOLD (or custom color tuple)
   - `header_bg`: RED or INK
   - `bubble_bg`: optional background for a special top card (use REDBG for a red "wish" bubble)
   - `items`: list of dicts with keys `marker` ("x" | "check" | None), `text` (string), and optionally `bubble` (true)

3. **Set output path** in the `make(...)` calls at the bottom of the script.

4. **Run the script** using the managed Python venv:
   ```bash
   C:/Users/User/.workbuddy/binaries/python/envs/default/Scripts/python.exe scripts/gzh_infographic.py
   ```

5. **Verify** by opening the generated PNG. The expected markers are a custom-drawn red "×" and gold "✓" to avoid missing font glyphs.

6. **Deliver** the PNG to the user and tell them which 图片位 to insert it into in the 公众号 editor.

## Technical notes

- Canvas width: 1080px; height computed automatically from content.
- Fonts: `C:/Windows/Fonts/msyh.ttc` (regular) and `msyhbd.ttc` (bold). These must be present on Windows.
- Python venv: install Pillow into `C:/Users/User/.workbuddy/binaries/python/envs/default`.
- Marker icons are drawn with PIL `line(...)` so they survive even when the font lacks check/cross glyphs.
- Avoid em dashes (破折号) in the card text to match the project's voice rules.

## Example output files

- `图一_模糊指令vs五要素任务书.png` — one sentence vs five-element task book
- `图二_资料散落vs整合任务书.png` — scattered sources vs consolidated task book

## Resources

- `scripts/gzh_infographic.py` — the main Pillow generator script. Copy and edit per task.
