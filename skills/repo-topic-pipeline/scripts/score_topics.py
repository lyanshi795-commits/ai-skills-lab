#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题打分：基于 素材库 与候选清单，对选题做 5 维量化评分并排名。
维度：内容价值(value) / 受众匹配(audience,自动) / 时效性(timeliness) /
      传播潜力(spread) / 差异化(diff,自动)
输出：选题决策表.md + 选题决策表.csv
"""
import os, json, csv

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(BASE, "选题候选.json")
OUT_MD = os.path.join(BASE, "选题决策表.md")
OUT_CSV = os.path.join(BASE, "选题决策表.csv")

# 权重（可调）
WEIGHTS = {"value": 0.25, "audience": 0.20, "timeliness": 0.15, "spread": 0.20, "diff": 0.20}

# 目标受众（AI号）相关主题标签 —— 用于自动计算「受众匹配」
PERSONA_TAGS = {"自动化任务", "技能Skill", "自媒体增长", "知识管理",
                "连接器与API", "视频生成", "远程控制", "资讯整合",
                "多智能体", "案例拆解", "岗位行业落地"}

def auto_audience(tags):
    """受众匹配：候选标签与目标受众标签的重合度（1-5）。"""
    overlap = len(set(tags) & PERSONA_TAGS)
    return min(5, max(1, overlap + 1))  # 至少1，封顶5

def auto_diff(cands):
    """差异化：相同(角度,类型)组合越少，得分越高。"""
    combo = {}
    for c in cands:
        k = (c["angle"], c["content_type"])
        combo[k] = combo.get(k, 0) + 1
    diff = {}
    for c in cands:
        k = (c["angle"], c["content_type"])
        same = combo[k]
        diff[c["id"]] = max(2, 6 - same)  # 唯一=5，重复递减，下限2
    return diff

def main():
    cands = json.load(open(CAND, encoding="utf-8"))
    diff_map = auto_diff(cands)

    rows = []
    for c in cands:
        aud = auto_audience(c["tags"])
        dif = diff_map[c["id"]]
        comp = round(
            WEIGHTS["value"] * c["value"] +
            WEIGHTS["audience"] * aud +
            WEIGHTS["timeliness"] * c["timeliness"] +
            WEIGHTS["spread"] * c["spread"] +
            WEIGHTS["diff"] * dif, 2)
        rows.append({
            "id": c["id"],
            "title": c["title"],
            "angle": c["angle"],
            "content_type": c["content_type"],
            "value": c["value"],
            "audience": aud,
            "timeliness": c["timeliness"],
            "spread": c["spread"],
            "diff": dif,
            "composite": comp,
            "source": " / ".join(c["source"]),
            "tags": "、".join(c["tags"]),
            "note": c["note"],
        })
    rows.sort(key=lambda r: r["composite"], reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    # Markdown 决策表
    L = ["# 选题决策表（Day 3 · WorkBuddyGuide 素材库）", "",
         f"- 候选数：{len(rows)} ｜ 权重：内容价值{WEIGHTS['value']} / 受众匹配{WEIGHTS['audience']} / "
         f"时效性{WEIGHTS['timeliness']} / 传播潜力{WEIGHTS['spread']} / 差异化{WEIGHTS['diff']}",
         "- 受众匹配、差异化由本地脚本基于标签自动计算；价值/时效/传播为人工评分（含理由）", "",
         "## 排名总览", "",
         "| 排名 | 编号 | 选题 | 角度 | 类型 | 综合 | 价值 | 受众 | 时效 | 传播 | 差异 |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['rank']} | {r['id']} | {r['title']} | {r['angle']} | {r['content_type']} | "
                 f"**{r['composite']}** | {r['value']} | {r['audience']} | {r['timeliness']} | {r['spread']} | {r['diff']} |")
    L += ["", "## 明细与依据", ""]
    for r in rows:
        L.append(f"### #{r['rank']} {r['id']} · {r['title']}")
        L.append(f"- 角度：{r['angle']} ｜ 类型：{r['content_type']} ｜ 综合分：**{r['composite']}**")
        L.append(f"- 素材来源：`{r['source']}`")
        L.append(f"- 主题标签：{r['tags']}")
        L.append(f"- 评分理由：{r['note']}")
        L.append("")

    # CSV
    fields = ["rank","id","title","angle","content_type","composite","value","audience","timeliness","spread","diff","tags","source","note"]
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields})

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"决策表已生成：{len(rows)} 条，Top3 = " + "、".join(r["id"] for r in rows[:3]))
    print(f"  MD：{OUT_MD}")
    print(f"  CSV：{OUT_CSV}")

if __name__ == "__main__":
    main()
