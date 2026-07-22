#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成两张公众号配图（1080px 全文宽，可直接卡进正文预留图片位）
- 图一：一句"帮我做公众号" vs 一份五要素任务书   -> 第五篇 截图1
- 图二：资料散落 5 处 vs 收进一份任务书          -> 第三篇 截图1
纯 Pillow 绘制，中文用微软雅黑，无外部依赖。
"""
from PIL import Image, ImageDraw, ImageFont

FONT_REG = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except Exception:
        return ImageFont.truetype(FONT_REG, size)

# 配色（低饱和高级）
INK   = (26, 26, 26)
SUB   = (138, 138, 138)
GOLD  = (191, 155, 95)
RED   = (200, 92, 92)
CREAM = (250, 247, 241)
REDBG = (250, 242, 242)
CARD  = (255, 255, 255)
LINE  = (236, 236, 236)
WHITE = (255, 255, 255)

def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        t = cur + ch
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines

def measure_col(header_h, items, fnt_item, inner_w, card_pad, line_h, gap, marker_w=42):
    h = header_h
    for it in items:
        if it.get("bubble"):
            txt_w = inner_w
        else:
            txt_w = inner_w - marker_w - 10
        lines = wrap(it["text"], fnt_item, txt_w)
        h += card_pad * 2 + max(1, len(lines)) * line_h
        h += gap
    return h

def draw_col(d, x, y, w, header, items, accent, header_bg, fnt_title, fnt_item,
             inner_w, card_pad, line_h, gap, bubble_bg=None):
    # 列头
    d.rounded_rectangle([x, y, x + w, y + 60], radius=10, fill=header_bg)
    d.text((x + w / 2, y + 30), header, font=fnt_title, fill=WHITE, anchor="mm")
    cy = y + 60 + gap
    for it in items:
        if it.get("bubble"):
            lines = wrap(it["text"], fnt_item, inner_w)
            ch = card_pad * 2 + len(lines) * line_h
            d.rounded_rectangle([x, cy, x + w, cy + ch], radius=14, fill=bubble_bg or REDBG)
            ty = cy + card_pad
            for ln in lines:
                d.text((x + card_pad, ty), ln, font=fnt_item, fill=INK, anchor="la")
                ty += line_h
            cy += ch + gap
            continue
        lines = wrap(it["text"], fnt_item, inner_w - 42 - 10)
        ch = card_pad * 2 + max(1, len(lines)) * line_h
        d.rounded_rectangle([x, cy, x + w, cy + ch], radius=10, fill=CARD, outline=LINE, width=1)
        # marker: 自定义绘制，避免字体缺字
        mk = it.get("marker")
        mx = x + card_pad + 18
        my = cy + ch / 2
        if mk == "x":
            d.line([(mx - 7, my - 7), (mx + 7, my + 7)], fill=accent, width=3)
            d.line([(mx + 7, my - 7), (mx - 7, my + 7)], fill=accent, width=3)
        elif mk == "check":
            d.line([(mx - 8, my + 2), (mx - 3, my + 6)], fill=accent, width=3)
            d.line([(mx - 3, my + 6), (mx + 8, my - 6)], fill=accent, width=3)
        ty = cy + card_pad
        for ln in lines:
            d.text((x + card_pad + 42 + 10, ty), ln, font=fnt_item, fill=INK, anchor="la")
            ty += line_h
        cy += ch + gap
    return cy

def make(out_path, title, subtitle, left, right, bottom):
    W = 1080
    margin = 48
    gap_col = 40
    col_w = (W - 2 * margin - gap_col) // 2
    inner_w = col_w - 36  # card padding 18*2

    fnt_title = font(42, True)
    fnt_sub = font(22)
    fnt_colh = font(26, True)
    fnt_item = font(24)
    fnt_bottom = font(24, True)

    # 顶部标题区
    title_h = 70
    sub_h = 36
    top = margin + title_h + sub_h + 20

    header_h = 60
    card_pad = 16
    line_h = 34
    gap = 16

    lh = measure_col(header_h, left["items"], fnt_item, inner_w, card_pad, line_h, gap)
    rh = measure_col(header_h, right["items"], fnt_item, inner_w, card_pad, line_h, gap)
    col_h = max(lh, rh)

    bottom_h = 100
    H = top + col_h + bottom_h + margin

    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # 标题
    d.text((W / 2, margin + title_h / 2), title, font=fnt_title, fill=INK, anchor="mm")
    d.text((W / 2, margin + title_h + sub_h / 2), subtitle, font=fnt_sub, fill=SUB, anchor="mm")
    # 金色短线
    d.rounded_rectangle([W / 2 - 28, margin + title_h + sub_h + 6, W / 2 + 28, margin + title_h + sub_h + 9], radius=2, fill=GOLD)

    lx = margin
    rx = margin + col_w + gap_col
    draw_col(d, lx, top, col_w, left["header"], left["items"], left["accent"], left["header_bg"],
             fnt_colh, fnt_item, inner_w, card_pad, line_h, gap, left.get("bubble_bg"))
    draw_col(d, rx, top, col_w, right["header"], right["items"], right["accent"], right["header_bg"],
             fnt_colh, fnt_item, inner_w, card_pad, line_h, gap, right.get("bubble_bg"))

    # 中间 VS 圆
    mid_y = top + col_h / 2
    d.ellipse([W / 2 - 26, mid_y - 26, W / 2 + 26, mid_y + 26], fill=WHITE, outline=GOLD, width=3)
    d.text((W / 2, mid_y), "VS", font=font(26, True), fill=INK, anchor="mm")

    # 底部说明条
    by = top + col_h + 20
    d.rounded_rectangle([margin, by, W - margin, by + bottom_h - 20], radius=12, fill=INK)
    d.rounded_rectangle([margin, by, margin + 6, by + bottom_h - 20], radius=3, fill=GOLD)
    # 底部文字自动换行
    blines = wrap(bottom, fnt_bottom, W - 2 * margin - 50)
    ty = by + (bottom_h - 20 - len(blines) * 32) / 2
    for ln in blines:
        d.text((margin + 30, ty), ln, font=fnt_bottom, fill=WHITE, anchor="la")
        ty += 32

    img.save(out_path, "PNG")
    print("OK", out_path, W, "x", H)

# ============ 图一：模糊指令 vs 五要素任务书 ============
left1 = {
    "header": "你随口说的", "accent": RED, "header_bg": RED, "bubble_bg": REDBG,
    "items": [
        {"bubble": True, "text": "帮我做个公众号"},
        {"marker": "x", "text": "写给谁：受众没说"},
        {"marker": "x", "text": "解决什么：问题没定"},
        {"marker": "x", "text": "用哪些资料：没给旧文/对标"},
        {"marker": "x", "text": "边界在哪：什么不能说没划"},
        {"marker": "x", "text": "怎样算完：验收没定"},
    ],
}
right1 = {
    "header": "Agent 接得住的", "accent": GOLD, "header_bg": INK,
    "items": [
        {"marker": "check", "text": "目标：写给谁、解决什么"},
        {"marker": "check", "text": "材料：旧文 / 对标 / 禁区"},
        {"marker": "check", "text": "流程：六步拆解法"},
        {"marker": "check", "text": "边界：什么绝对不能写"},
        {"marker": "check", "text": "验收：怎样算写完"},
    ],
}
make(
    "D:/04_Projects/ObsidianVaults/MyVault/WorkBuddy个人内容Agent商业验证/配图/图一_模糊指令vs五要素任务书.png",
    "一句“帮我做公众号” vs 一份五要素任务书",
    "同一件事，差的就是这五个空有没有填",
    left1, right1,
    "愿望不能执行，只能许。五个答案填满，Agent 才接得住。",
)

# ============ 图二：资料散落 vs 整合任务书 ============
left2 = {
    "header": "资料散在 5 处", "accent": RED, "header_bg": RED,
    "items": [
        {"marker": "x", "text": "脑子里的念头"},
        {"marker": "x", "text": "微信聊天记录"},
        {"marker": "x", "text": "收藏夹里的文章"},
        {"marker": "x", "text": "Obsidian 旧稿"},
        {"marker": "x", "text": "备忘录的灵感"},
    ],
}
right2 = {
    "header": "收进一份任务书", "accent": GOLD, "header_bg": INK,
    "items": [
        {"marker": "check", "text": "建项目文件夹"},
        {"marker": "check", "text": "倒出口述（先不管结构）"},
        {"marker": "check", "text": "贴旧文（给 Agent 范文）"},
        {"marker": "check", "text": "列对标（想学它的哪点）"},
        {"marker": "check", "text": "标禁区（划清边界）"},
        {"marker": "check", "text": "写任务书（五要素齐全）"},
    ],
}
make(
    "D:/04_Projects/ObsidianVaults/MyVault/WorkBuddy个人内容Agent商业验证/配图/图二_资料散落vs整合任务书.png",
    "资料散在 5 处 vs 收进一份任务书",
    "整理不是归档，是把你已有的东西请出来",
    left2, right2,
    "资料一直在你身上，缺的只是把它摊开的那一步。",
)
