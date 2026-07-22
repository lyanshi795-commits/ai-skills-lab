---
name: repo-topic-pipeline
description: Turn any GitHub repo (or local folder of docs/code) into a structured, searchable content material library and an automated WeChat/official-account topic-selection pipeline. Use when the user wants to build a 素材库 from a repository, mine candidate article topics from multiple angles, score them on multiple dimensions with a local tool, and output a ranked topic decision table. Triggered by phrases like: 把仓库变成选题库, 公众号素材库, 选题打分, 选题决策表, 从GitHub挖选题, 素材采集+选题挖掘.
agent_created: true
---

# repo-topic-pipeline

## Overview

Convert a GitHub repository or local docs/code folder into a reusable content material library, then run a four-stage pipeline that produces a ranked topic decision table ready for editorial scheduling:

1. **素材采集 (Collect)** — extract all text (markdown, docs, code comments) into a structured, searchable library with a keyword inverted index and topic tags.
2. **选题挖掘 (Mine)** — generate candidate topics from several angles (technical analysis, usage scenarios, best practices, case studies, industry trends), each bound to a real source path in the repo.
3. **选题打分 (Score)** — score every candidate on five dimensions (content value, audience fit, timeliness, spread potential, differentiation) using a local Python tool with transparent weights.
4. **选题分类 (Classify)** — label each topic's angle and content type (tutorial / opinion / roundup / case), and output a ranked decision table (Markdown + CSV).

The pipeline is deterministic and re-runnable: change the repo, audience tags, or weights without rewriting logic.

## When to Use

Trigger this skill when the user asks to:
- Build a 公众号/内容 素材库 from a GitHub repo or docs folder
- Mine article/topic candidates from existing material
- Score or rank topic candidates automatically
- Produce a 选题决策表 / 选题打分表 for editorial planning
- Phrases: "把仓库变成选题库", "公众号素材库", "选题打分", "从GitHub挖选题"

## Workflow

1. **Clone or point at the source.** `git clone --depth 1 <repo> repo` (or use an existing local folder). Place it as `repo/` next to the scripts.
2. **Collect.** Run `scripts/extract_materials.py`. It walks the repo, skips binary/image dirs (`assets`, `.git`, `node_modules`), extracts `.md` bodies and code comments (JS `//`+`/* */`, Python `#`+docstrings), classifies by top-level folder, applies `TOPIC_RULES` keyword tagging, builds an inverted word index, and writes `素材库.json` + `素材索引.md`. Use `python extract_materials.py --search "关键词"` to verify retrieval.
3. **Mine candidates.** Author `选题候选.json` by hand (one object per candidate). Required fields: `id`, `title`, `angle`, `content_type`, `source` (real repo paths), `tags` (from the 15 topic taxonomy used in `extract_materials.py`), `value`/`timeliness`/`spread` (1-5 with rationale in `note`). Cover multiple angles.
4. **Score + classify.** Run `scripts/score_topics.py`. It auto-computes `audience` (overlap of candidate `tags` with `PERSONA_TAGS`) and `diff` (uniqueness of the `(angle, content_type)` combo), combines with the three manual scores via `WEIGHTS`, ranks, and writes `选题决策表.md` + `选题决策表.csv`.
5. **Deliver.** Present the Top-3 ranked topics and the decision table; attach the CSV/MD.

## Key Tunables (edit in scripts)

- `extract_materials.py` → `TOPIC_RULES`: add/adjust topic tags and their keywords.
- `extract_materials.py` → `SKIP_DIRS`, `TEXT_EXT`, `CODE_EXT`: control which files are indexed.
- `score_topics.py` → `PERSONA_TAGS`: the target-audience topic set used for auto audience-fit.
- `score_topics.py` → `WEIGHTS`: the five-dimension weights (must sum to 1).

## Red Lines

- Every candidate MUST bind to a real source path in the repo — never invent topics with no material backing.
- Manual scores (value/timeliness/spread) MUST carry a `note` rationale; auto scores MUST be recomputable from inputs.
- Scoring is a relative priority signal, not a traffic or monetization guarantee — do not promise reads or revenue.

## Notes

- Scripts run with the managed Python venv: `C:/Users/User/.workbuddy/binaries/python/envs/default/Scripts/python.exe`.
- The reference implementation was built for the AlephAITech/WorkBuddyGuide repo (a WorkBuddy "bluebook" with 4 parts + community cases), but the pipeline is repo-agnostic.
