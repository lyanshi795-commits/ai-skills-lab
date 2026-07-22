# Contributing to WorkBuddy Skills

Thanks for wanting to improve this collection. We hold a consistent quality bar so every skill here is spec-compliant and genuinely useful.

## Before you start

Every skill in this repo is built through a **benchmarked 4-step loop** — please follow it for new skills:

1. **Scaffold** with `skill-creator` (correct `name` + `description` frontmatter, correct folder format).
2. **Distill** domain knowledge into `references/`; keep the `SKILL.md` body to core content only (progressive disclosure).
3. **Benchmark** against mature local skills (`dbs-content`, `yao-demand-skill`) — match their structure (philosophy → phases → anti-patterns → output contract → reference map).
4. **Validate** against the official spec (`agentskills.io` + Anthropic whitepaper).

## Skill format rules

- `name`: kebab-case, ≤ 64 chars, matches the folder name, no reserved prefixes (`claude`, `anthropic`).
- `description`: must state **what** + **when** + trigger words, ≤ 1024 chars.
- `SKILL.md` body: **under 500 lines**. Long material → `references/`.
- No `README.md` inside a skill folder (reserved name per spec).
- Declare `license`, `allowed-tools`, and `metadata` where relevant.
- Security: audit every bundled script; never commit secrets; only trust first-party sources.

## How to submit

1. Fork the repo and create a branch: `git checkout -b feature/<skill-name>`.
2. Add `skills/<skill-name>/` with `SKILL.md` + optional `scripts/` + `references/`.
3. Test any bundled script; confirm it runs cleanly.
4. Commit: `git commit -m "feat: add <skill-name>"`.
5. Push and open a Pull Request describing:
   - **Trigger** phrases
   - **Inputs** the skill expects
   - **Outputs** it produces
   - Any **dependencies** (Python packages, fonts, tools)

## Review checklist (maintainers)

- [ ] Frontmatter valid (`name` + `description` present and correct)
- [ ] `SKILL.md` < 500 lines
- [ ] Progressive disclosure respected (no giant reference dumped into body)
- [ ] Every bundled script runs without secrets/network calls at runtime
- [ ] `agent_created: true` set for first-party skills
- [ ] PR description documents trigger / inputs / outputs

By contributing, you agree your skill is released under the repository's MIT License.
