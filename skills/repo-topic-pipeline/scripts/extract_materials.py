#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材采集：从 WorkBuddyGuide 仓库抽取全部文本内容，建立结构化、可检索的素材库。
输出：
  - 素材库.json   : {meta, entries[], word_index{}, topic_index{}}
  - 素材索引.md   : 人类可读索引（含路径/分类/标签/字数/摘要）
支持：python extract_materials.py --search "关键词"
"""
import os, re, json, sys

REPO = "repo"
OUT_JSON = "素材库.json"
OUT_MD = "素材索引.md"

SKIP_DIRS = {'.git', 'node_modules', 'assets'}  # assets 多为图片，跳过
TEXT_EXT = {'.md', '.txt', '.ts', '.vue', '.py', '.json', '.yml', '.yaml',
            '.css', '.html', '.mts', '.nvmrc', '.gitignore', '.headers'}
CODE_EXT = {'.ts', '.vue', '.py', '.css', '.html', '.mts'}

# 主题标签关键词映射（命中即打标，可多标）
TOPIC_RULES = [
    ("自动化任务", ["自动化", "定时", "调度", "cron", "schedule", "循环任务"]),
    ("技能Skill", ["skill", "技能", "蒸馏", "书", "视频", "可复用"]),
    ("多智能体", ["多agent", "多智能体", "agent团", "团队协作", "team"]),
    ("连接器与API", ["连接器", "connector", "api", "小程序", "im助理", "企微", "飞书"]),
    ("自媒体增长", ["自媒体", "增长", "公众号", "geo", "流量", "涨粉", "闭环"]),
    ("知识管理", ["知识库", "收藏", "ima", "笔记", "再次用起来", "知识管理"]),
    ("办公三件套", ["word", "excel", "ppt", "文档", "表格", "演示"]),
    ("投资分析", ["投资", "股票", "行情", "财报", "基金"]),
    ("视频生成", ["视频", "ai视频", "剪辑", "分镜", "字幕"]),
    ("会议日程", ["会议", "日程", "纪要", "提醒", "待办"]),
    ("远程控制", ["远程", "控制", "不在电脑前", "向日葵"]),
    ("岗位行业落地", ["岗位", "行业", "路线图", "落地", "工作流"]),
    ("案例拆解", ["案例", "实操", "showreel", "resume"]),
    ("使用入门", ["下载", "安装", "登录", "初识", "更新", "主界面", "任务"]),
    ("资讯整合", ["资讯", "信息流", "每日通知", "新闻", "聚合"]),
]

def read_file(p):
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def extract_code_comments(text, ext):
    """从代码文件抽取注释文本。"""
    out = []
    if ext in ('.py',):
        # # 行注释 + 三引号 docstring
        for m in re.finditer(r'#.*', text):
            out.append(m.group(0).lstrip('# '))
        for m in re.finditer(r'"""[\s\S]*?"""', text):
            out.append(m.group(0).strip('"'))
        for m in re.finditer(r"'''[\s\S]*?'''", text):
            out.append(m.group(0).strip("'"))
    else:
        # // 行注释
        for m in re.finditer(r'//[^\n]*', text):
            out.append(m.group(0).lstrip('/').strip())
        # /* */ 块注释
        for m in re.finditer(r'/\*[\s\S]*?\*/', text):
            out.append(re.sub(r'\*+', '', m.group(0)).strip())
    return "\n".join(out)

def classify_category(rel):
    segs = rel.lower().split('/')
    s = " / ".join(segs)
    if 'bluebook/第一篇' in s or '使用手册' in s:
        return "01_使用手册"
    if 'bluebook/第二篇' in s or '案例篇' in s:
        return "02_案例篇"
    if 'bluebook/第三篇' in s or '进阶篇' in s:
        return "03_进阶篇"
    if 'bluebook/第四篇' in s or '岗位与行业' in s:
        return "04_岗位行业落地"
    if 'bluebook/附录' in s or '附录' in s:
        return "05_附录"
    if 'cases' in segs:
        return "06_社区案例"
    if 'plans' in segs:
        return "07_设计规划"
    if 'community' in segs:
        return "08_社区贡献"
    if 'help' in segs or 'reading-guide' in s or 'seo' in s or 'design-qa' in s:
        return "09_站点文档"
    return "00_根文档"

def tokenize(text):
    terms = set()
    # 英文/数字词
    for w in re.findall(r'[A-Za-z][A-Za-z0-9_]{1,}', text):
        w = w.lower()
        if len(w) >= 2:
            terms.add(w)
    # 中文：全串(>=2) + 二元组，提升召回
    for run in re.findall(r'[\u4e00-\u9fff]+', text):
        if len(run) >= 2:
            terms.add(run)
        for i in range(len(run) - 1):
            terms.add(run[i:i+2])
    return terms

def tags_for(text):
    low = text.lower()
    tags = []
    for tag, kws in TOPIC_RULES:
        if any(kw.lower() in low for kw in kws):
            tags.append(tag)
    return tags

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo = os.path.join(base, REPO)
    if not os.path.isdir(repo):
        print("未找到 repo 目录，请先 git clone"); sys.exit(1)

    entries = []
    eid = 0
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT:
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, repo)
            raw = read_file(full)
            if not raw.strip():
                continue
            if ext in CODE_EXT:
                text = extract_code_comments(raw, ext)
                ftype = "code_comment"
                title = fn
            else:
                text = raw
                ftype = "doc"
                # 标题取首个 H1
                m = re.search(r'^#\s+(.+)$', raw, re.M)
                title = m.group(1).strip() if m else os.path.splitext(fn)[0]
            headings = re.findall(r'^#{1,3}\s+(.+)$', raw, re.M) if ext == '.md' else []
            char_count = len(text)
            if char_count < 20:
                continue
            cat = classify_category(rel)
            entry = {
                "id": eid,
                "file": rel,
                "title": title,
                "category": cat,
                "type": ftype,
                "char_count": char_count,
                "headings": headings[:30],
                "tags": tags_for(text),
                "text": text,
                "excerpt": text[:240].replace("\n", " "),
            }
            entries.append(entry)
            eid += 1

    # 倒排索引
    word_index = {}
    topic_index = {}
    for e in entries:
        for t in tokenize(e["text"]):
            word_index.setdefault(t, []).append(e["id"])
        for tg in e["tags"]:
            topic_index.setdefault(tg, []).append(e["id"])

    lib = {
        "meta": {
            "source": "https://github.com/AlephAITech/WorkBuddyGuide.git",
            "entry_count": len(entries),
            "total_chars": sum(e["char_count"] for e in entries),
            "categories": sorted(set(e["category"] for e in entries)),
            "topic_tags": sorted(topic_index.keys()),
        },
        "entries": entries,
        "word_index": word_index,
        "topic_index": topic_index,
    }
    with open(os.path.join(base, OUT_JSON), 'w', encoding='utf-8') as f:
        json.dump(lib, f, ensure_ascii=False, indent=1)
    print(f"素材库构建完成：{len(entries)} 条，{lib['meta']['total_chars']} 字")

    # 人类可读索引
    lines = ["# WorkBuddyGuide 素材索引", "",
             f"- 来源：{lib['meta']['source']}",
             f"- 条目数：{len(entries)}",
             f"- 总字数：{lib['meta']['total_chars']}", "",
             "## 主题分布", ""]
    for tg in sorted(topic_index, key=lambda x: -len(topic_index[x])):
        lines.append(f"- **{tg}**：{len(topic_index[tg])} 篇")
    lines += ["", "## 条目明细", ""]
    for e in sorted(entries, key=lambda x: x["category"]):
        lines.append(f"### [{e['id']}] {e['title']}")
        lines.append(f"- 路径：`{e['file']}`")
        lines.append(f"- 分类：{e['category']} ｜ 类型：{e['type']} ｜ 字数：{e['char_count']}")
        if e["tags"]:
            lines.append(f"- 标签：{'、'.join(e['tags'])}")
        if e["headings"]:
            lines.append(f"- 结构：{' › '.join(e['headings'][:6])}")
        lines.append(f"- 摘要：{e['excerpt']}")
        lines.append("")
    with open(os.path.join(base, OUT_MD), 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"索引写入：{OUT_MD}")

    # 搜索模式
    if len(sys.argv) > 2 and sys.argv[1] == '--search':
        q = sys.argv[2]
        hits = word_index.get(q, [])
        # 也尝试二元组匹配
        if not hits:
            for k, v in word_index.items():
                if q in k:
                    hits += v
        hits = sorted(set(hits))
        print(f"\n搜索「{q}」命中 {len(hits)} 条：")
        for i in hits[:20]:
            e = entries[i]
            print(f"  [{e['id']}] {e['title']}  ({e['category']})")

if __name__ == "__main__":
    main()
