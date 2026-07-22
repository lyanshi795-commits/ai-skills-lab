#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成公众号封面图（钩子型）
- 竖屏方图 1080x1080（订阅信息流缩略图）
- 宽图     1080x460（文章首图 / 分享卡片）
主题：第五篇《我盯着"帮你做公众号"这五个字看了十分钟，回了他五个问题》
纯 Pillow，中文用微软雅黑。
"""
from PIL import Image, ImageDraw, ImageFont

FONT_REG  = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except Exception:
        return ImageFont.truetype(FONT_REG, size)

# 配色（沿用品牌：墨黑 + 暖金 + 米白 + 克制红）
INK     = (28, 26, 23)
INK2    = (40, 36, 31)
GOLD    = (191, 155, 95)
GOLD_D  = (160, 125, 62)
CREAM   = (250, 247, 241)
CREAM_D = (206, 198, 186)
RED     = (200, 92, 63)
PILLBG  = (46, 42, 36)

def text_w(s, fnt):
    return fnt.getlength(s)

def draw_text(d, xy, s, fnt, fill, anchor="lt"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)

def radial_glow(img, cx, cy, radius, color, max_alpha=150):
    """在 RGBA 层上画径向光晕"""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    step = max(4, radius // 60)
    r = radius
    while r > 0:
        a = int(max_alpha * (1 - r / radius) ** 2)
        dl.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
        r -= step
    return Image.alpha_composite(img, layer)

def base(size):
    """深墨底 + 右上暖金光晕 + 极淡网格"""
    img = Image.new("RGB", size, INK)
    # 竖向渐变（上深下略亮）
    W, H = size
    top = INK
    bot = INK2
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        ImageDraw.Draw(img).line([(0, y), (W, y)], fill=c)
    # 光晕（用 RGBA 合成）
    imga = img.convert("RGBA")
    imga = radial_glow(imga, int(W * 0.82), int(H * 0.18), int(min(W, H) * 0.55), GOLD, 120)
    img = imga.convert("RGB")
    d = ImageDraw.Draw(img)
    # 极淡网格
    grid = ImageDraw.Draw(img)
    for x in range(0, W, 90):
        grid.line([(x, 0), (x, H)], fill=(255, 255, 255, 8) if False else (60, 55, 48), width=1)
    return img, d

def pill(d, x, y, w, h, text, fnt, fill=PILLBG, outline=GOLD, txt_fill=CREAM):
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill, outline=outline, width=2)
    tw = text_w(text, fnt)
    d.text((x + (w - tw) / 2, y + h / 2), text, font=fnt, fill=txt_fill, anchor="lm")

# ---------- 竖屏方图 1080x1080 ----------
def build_square(path):
    W = H = 1080
    img, d = base((W, H))
    M = 80
    # 顶左 badge
    bf = font(28, True)
    badge = "第五篇 · 内容 Agent 验证"
    bw = text_w(badge, bf) + 44
    d.rounded_rectangle([M, M, M + bw, M + 56], radius=28, outline=GOLD, width=2, fill=(46, 42, 36))
    d.text((M + 22, M + 28), badge, font=bf, fill=GOLD, anchor="lm")
    # 顶右 红标（钩子）
    rf = font(28, True)
    rtag = "模糊需求 ≠ 任务"
    rw = text_w(rtag, rf) + 44
    d.rounded_rectangle([W - M - rw, M, W - M, M + 56], radius=28, outline=RED, width=2, fill=(58, 40, 36))
    d.text((W - M - rw + 22, M + 28), rtag, font=rf, fill=(230, 140, 120), anchor="lm")

    # 主标题行1
    tf = font(54, True)
    d.text((M, 250), "一句「帮我做公众号」", font=tf, fill=CREAM, anchor="lt")

    # 主钩子行：我回了 [大5] 个问题
    pre = "我回了 "
    pf = font(54, True)
    wp = text_w(pre, pf)
    x_pre = M
    y_text = 430
    d.text((x_pre, y_text), pre, font=pf, fill=CREAM, anchor="lt")

    big = font(220, True)
    w5 = text_w("5", big)
    x5 = x_pre + wp + 24
    y5 = y_text - 18  # 大字略上探，视觉居中
    d.text((x5, y5), "5", font=big, fill=GOLD, anchor="lt")
    # 金色下划强调
    d.rectangle([x5, y5 + 200, x5 + w5, y5 + 212], fill=GOLD_D)

    post = "个问题"
    x_post = x5 + w5 + 24
    d.text((x_post, y_text), post, font=pf, fill=CREAM, anchor="lt")

    # 五个要素小药丸（证明"5"的来由，强化品牌概念）
    elems = ["目标", "材料", "流程", "边界", "验收"]
    ef = font(30, True)
    ey = 720
    gap = 22
    pill_w = (W - 2 * M - gap * 4) / 5
    for i, e in enumerate(elems):
        px = M + i * (pill_w + gap)
        pill(d, px, ey, pill_w, 64, e, ef)

    # 底部品牌行
    bf2 = font(26, False)
    d.text((M, 960), "WorkBuddy · 个人内容 Agent 商业验证", font=bf2, fill=CREAM_D, anchor="lt")
    # 右下小提示
    hf = font(26, True)
    d.text((W - M, 960), "为什么是 5 个？", font=hf, fill=GOLD, anchor="rt")

    img.save(path, "PNG")
    print("saved", path)

# ---------- 宽图 1080x460 ----------
def build_wide(path):
    W, H = 1080, 460
    img, d = base((W, H))
    M = 56
    # 左：badge
    bf = font(24, True)
    badge = "第五篇 · 内容 Agent 验证"
    bw = text_w(badge, bf) + 38
    d.rounded_rectangle([M, M, M + bw, M + 46], radius=23, outline=GOLD, width=2, fill=(46, 42, 36))
    d.text((M + 20, M + 23), badge, font=bf, fill=GOLD, anchor="lm")
    # 右：红标
    rf = font(24, True)
    rtag = "模糊需求 ≠ 任务"
    rw = text_w(rtag, rf) + 38
    d.rounded_rectangle([W - M - rw, M, W - M, M + 46], radius=23, outline=RED, width=2, fill=(58, 40, 36))
    d.text((W - M - rw + 20, M + 23), rtag, font=rf, fill=(230, 140, 120), anchor="lm")

    # 标题
    tf = font(46, True)
    d.text((M, 150), "一句「帮我做公众号」", font=tf, fill=CREAM, anchor="lt")
    # 钩子行
    pre = "我回了 "
    pf = font(46, True)
    wp = text_w(pre, pf)
    y_text = 250
    d.text((M, y_text), pre, font=pf, fill=CREAM, anchor="lt")
    big = font(150, True)
    w5 = text_w("5", big)
    x5 = M + wp + 18
    d.text((x5, y_text - 30), "5", font=big, fill=GOLD, anchor="lt")
    d.rectangle([x5, y_text - 30 + 132, x5 + w5, y_text - 30 + 142], fill=GOLD_D)
    d.text((x5 + w5 + 18, y_text), "个问题", font=pf, fill=CREAM, anchor="lt")

    # 品牌行
    bf2 = font(22, False)
    d.text((M, 400), "WorkBuddy · 个人内容 Agent 商业验证", font=bf2, fill=CREAM_D, anchor="lt")

    # 右侧五个要素竖排小药丸
    elems = ["目标", "材料", "流程", "边界", "验收"]
    ef = font(24, True)
    rx = W - M - 150
    ry = 120
    rh = 40
    rg = 16
    for i, e in enumerate(elems):
        yy = ry + i * (rh + rg)
        pill(d, rx, yy, 150, rh, e, ef)

    img.save(path, "PNG")
    print("saved", path)

if __name__ == "__main__":
    OUT = "D:/04_Projects/ObsidianVaults/MyVault/WorkBuddy个人内容Agent商业验证/配图"
    build_square(OUT + "/封面图_方图_第五篇.png")
    build_wide(OUT + "/封面图_宽图_第五篇.png")
    print("done")
