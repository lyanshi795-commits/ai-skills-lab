---
name: long-screenshot-ocr
description: Extract Chinese/English text from very long screenshot images (e.g., mobile scroll captures, course handbooks, chat logs) using slicing, upscaling, reading-order reconstruction and noise cleanup. Use this skill when the user asks to OCR or extract text from one or more PNG/JPG screenshots.
license: MIT
compatibility: 适用于 WorkBuddy / Claude Code / 任意 agentskills.io 兼容运行时
metadata:
  author: SHR
  collection: SHR Skills
  version: 1.0.0
agent_created: true
---

# Long Screenshot OCR

## Overview

This skill performs high-quality text extraction from long/narrow screenshots by splitting the image into overlapping slices, upscaling each slice, running RapidOCR (PP-OCR), rebuilding the reading order, and cleaning common screenshot noise (page numbers, console timestamps, edge artifacts).

## When to Use

- User says "extract text from this image", "OCR this screenshot", "把这张图里的文字提取出来", etc.
- The image is a long vertical screenshot (common for WeChat mini-program manuals, course pages, chat histories).
- Standard whole-image OCR misses the title, scrambles reading order, or leaves a lot of numeric noise.

## Workflow

1. Determine the input image path and desired output markdown path.
2. Ensure the managed Python venv has the required packages installed:
   - `rapidocr-onnxruntime`
   - `Pillow`
   - `numpy`
3. Run the bundled script:
   ```bash
   <managed-python> <skill-dir>/scripts/ocr_long_screenshot.py <input.png> <output.md>
   ```
4. Inspect the output. If the image contains dense code or console output, some short alphanumeric artifacts may remain; only remove them manually when they are clearly noise, to avoid losing useful code/IDs/URLs.
5. Deliver the markdown file to the user with `present_files`.

## Script

- `scripts/ocr_long_screenshot.py` — Main OCR pipeline.

## Default Parameters

- Slice height: 2400 px
- Overlap: 250 px
- Upscale: 2×
- Confidence threshold: 0.5
- Similarity dedupe threshold: 0.8

For extremely small text (dense code), raise upscale to 3 and lower slice height to 1800 to manage memory.
