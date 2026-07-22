#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成公众号封面图（浩然养生号 · 膝盖篇 · 暖色中式养生版）
- 竖屏方图 1080x1080（订阅信息流缩略图）
- 宽图     1080x460（文章首图 / 分享卡片）
钩子：老人膝盖疼别只歇着，练肌肉=天然护膝，3个零成本动作
配色：宣纸米底 + 深赭墨字 + 铜暖金大字 + 朱砂红矛盾标（亲和不吓人）
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

# 配色（暖色中式养生：宣纸米 + 深赭墨 + 铜暖金 + 朱砂红）
BG_TOP  = (245, 235, 217)   # 宣纸米（上）
BG_BOT  = (233, 220, 197)   # 暖杏（下）
INK     = (60, 47, 35)      # 深赭墨（主文字）
INK_SOFT= (112, 92, 72)     # 暖灰棕（副文字）
GOLD    = (184, 142, 74)    # 铜暖金（大字/强调）
GOLD_D  = (150, 112, 54)
RED     = (193, 72, 52)     # 朱砂红（矛盾标）
RED_TXT = (255, 242, 235)
PILL_BG = (249, 242, 229)
PILL_TXT= (94, 72, 52)
GRID    = (205, 190, 165)

def text_w(s, fnt):
    return fnt.getlength(s)

def radial_glow(img, cx, cy, radius, color, max_alpha=130):
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
    """暖米底 + 右上铜金柔光 + 极淡网格"""
    img = Image.new("RGB", size, BG_TOP)
    W, H = size
    top, bot = BG_TOP, BG_BOT
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        ImageDraw.Draw(img).line([(0, y), (W, y)], fill=c)
    imga = img.convert("RGBA")
    imga = radial_glow(imga, int(W * 0.84), int(H * 0.16), int(min(W, H) * 0.6), GOLD, 110)
    img = imga.convert("RGB")
    d = ImageDraw.Draw(img)
    for x in range(0, W, 96):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    return img, d

def pill(d, x, y, w, h, text, fnt, fill=PILL_BG, outline=GOLD, txt_fill=PILL_TXT):
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill, outline=outline, width=2)
    tw = text_w(text, fnt)
    d.text((x + (w - tw) / 2, y + h / 2), text, font=fnt, fill=txt_fill, anchor="lm")

def red_tag(d, x, y, w, h, text, fnt):
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=RED, outline=RED, width=2)
    tw = text_w(text, fnt)
    d.text((x + (w - tw) / 2, y + h / 2), text, font=fnt, fill=RED_TXT, anchor="lm")

# ---------- 竖屏方图 1080x1080 ----------
def build_square(path):
    W = H = 1080
    img, d = base((W, H))
    M = 80
    # 顶左 badge
    bf = font(28, True)
    badge = "浩然养生 · 实用小妙招"
    bw = text_w(badge, bf) + 44
    d.rounded_rectangle([M, M, M + bw, M + 56], radius=28, outline=GOLD, width=2, fill=PILL_BG)
    d.text((M + 22, M + 28), badge, font=bf, fill=GOLD_D, anchor="lm")
    # 顶右 红标（矛盾钩子）
    rf = font(28, True)
    rtag = "越歇越废"
    rw = text_w(rtag, rf) + 44
    red_tag(d, W - M - rw, M, rw, 56, rtag, rf)

    # 主标题
    tf = font(60, True)
    d.text((M, 280), "老人膝盖疼，别只歇着", font=tf, fill=INK, anchor="lt")

    # 钩子行：练会 [大3] 个动作
    pre = "练会 "
    pf = font(50, True)
    wp = text_w(pre, pf)
    y_text = 470
    d.text((M, y_text), pre, font=pf, fill=INK, anchor="lt")

    big = font(180, True)
    w3 = text_w("3", big)
    x3 = M + wp + 18
    y3 = y_text - 52
    d.text((x3, y3), "3", font=big, fill=GOLD, anchor="lt")
    d.rectangle([x3, y3 + 158, x3 + w3, y3 + 170], fill=GOLD_D)

    post = " 个动作"
    d.text((x3 + w3 + 18, y_text), post, font=pf, fill=INK, anchor="lt")

    # 副钩子小字
    sf = font(34, True)
    d.text((M, 600), "给膝盖穿上「天然护膝」· 不用吃药", font=sf, fill=INK_SOFT, anchor="lt")

    # 五个要点药丸
    elems = ["直腿抬高", "靠墙静蹲", "按揉膝眼", "不用药", "零成本"]
    ef = font(30, True)
    ey = 730
    gap = 22
    pill_w = (W - 2 * M - gap * 4) / 5
    for i, e in enumerate(elems):
        px = M + i * (pill_w + gap)
        pill(d, px, ey, pill_w, 64, e, ef)

    # 底部品牌行
    bf2 = font(26, False)
    d.text((M, 960), "浩然养生 · 爸妈的实用小妙招", font=bf2, fill=INK_SOFT, anchor="lt")
    hf = font(26, True)
    d.text((W - M, 960), "转给爸妈看看 ↓", font=hf, fill=RED, anchor="rt")

    img.save(path, "PNG")
    print("saved", path)

# ---------- 宽图 1080x460 ----------
def build_wide(path):
    W, H = 1080, 460
    img, d = base((W, H))
    M = 56
    bf = font(24, True)
    badge = "浩然养生 · 实用小妙招"
    bw = text_w(badge, bf) + 38
    d.rounded_rectangle([M, M, M + bw, M + 46], radius=23, outline=GOLD, width=2, fill=PILL_BG)
    d.text((M + 20, M + 23), badge, font=bf, fill=GOLD_D, anchor="lm")
    rf = font(24, True)
    rtag = "越歇越废"
    rw = text_w(rtag, rf) + 38
    red_tag(d, W - M - rw, M, rw, 46, rtag, rf)

    # 标题
    tf = font(48, True)
    d.text((M, 150), "老人膝盖疼，别只歇着", font=tf, fill=INK, anchor="lt")
    # 钩子行
    pre = "练会 "
    pf = font(44, True)
    wp = text_w(pre, pf)
    y_text = 250
    d.text((M, y_text), pre, font=pf, fill=INK, anchor="lt")
    big = font(140, True)
    w3 = text_w("3", big)
    x3 = M + wp + 14
    d.text((x3, y_text - 42), "3", font=big, fill=GOLD, anchor="lt")
    d.rectangle([x3, y_text - 42 + 120, x3 + w3, y_text - 42 + 130], fill=GOLD_D)
    d.text((x3 + w3 + 16, y_text), "个动作，给膝盖「天然护膝」", font=pf, fill=INK, anchor="lt")

    # 品牌行
    bf2 = font(22, False)
    d.text((M, 400), "浩然养生 · 爸妈的实用小妙招", font=bf2, fill=INK_SOFT, anchor="lt")

    # 右侧竖排要点药丸
    elems = ["直腿抬高", "靠墙静蹲", "按揉膝眼", "不用药"]
    ef = font(24, True)
    rx = W - M - 150
    ry = 110
    rh = 40
    rg = 16
    for i, e in enumerate(elems):
        yy = ry + i * (rh + rg)
        pill(d, rx, yy, 150, rh, e, ef)

    img.save(path, "PNG")
    print("saved", path)

if __name__ == "__main__":
    OUT = "D:/04_Projects/ObsidianVaults/MyVault/07.发布文案/2026年/草稿"
    build_square(OUT + "/封面图_方图_膝盖篇.png")
    build_wide(OUT + "/封面图_宽图_膝盖篇.png")
    print("done")
