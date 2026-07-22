import sys
import re
from PIL import Image
import numpy as np
from rapidocr_onnxruntime import RapidOCR

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\User\Pictures\xai\PixPin_2026-07-22_16-47-14.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"D:\04_Projects\ObsidianVaults\MyVault\PixPin_2026-07-22_16-47-14_提取.md"

SLICE_H = 2400      # 切片高度（原图像素）
OVERLAP = 250       # 切片重叠
UP_SCALE = 2        # 每片放大倍数

engine = RapidOCR()

im = Image.open(SRC).convert('RGB')
W, H = im.size
print("image size:", im.size)

all_items = []  # (cy, hx, text, score)

step = SLICE_H - OVERLAP
y = 0
idx = 0
while True:
    y2 = min(y + SLICE_H, H)
    crop = im.crop((0, y, W, y2))
    # 放大
    crop = crop.resize((crop.width * UP_SCALE, crop.height * UP_SCALE), Image.LANCZOS)
    arr = np.array(crop)
    result, _ = engine(arr)
    n = 0
    if result:
        for box, text, score in result:
            score = float(score)
            if score < 0.5:
                continue
            ys = [p[1] for p in box]
            xs = [p[0] for p in box]
            cy = (sum(ys) / len(ys)) / UP_SCALE + y
            hx = min(xs) / UP_SCALE
            all_items.append((cy, hx, text.strip(), score))
            n += 1
    idx += 1
    print(f"slice {idx}: y={y}-{y2}, items={n}")
    if y2 == H:
        break
    y += step

print("total items:", len(all_items))

# 按阅读顺序排序：先 y 后 x
all_items.sort(key=lambda t: (t[0], t[1]))

# 聚合成行（按 y 邻近）
lines_out = []
cur = []
last_y = None
THRESH = 16
for cy, hx, text, score in all_items:
    if last_y is None or abs(cy - last_y) <= THRESH:
        cur.append((hx, text))
    else:
        cur.sort(key=lambda t: t[0])
        # 行内去重（切片重叠会导致同一文本被识别两次，含近似重复）
        dedup = []
        for hx2, txt2 in cur:
            dup = False
            for hx3, txt3 in dedup:
                if txt2 == txt3 or txt2 in txt3 or txt3 in txt2:
                    dup = True
                    break
                if len(txt2) > 6 and len(txt3) > 6:
                    import difflib
                    if difflib.SequenceMatcher(None, txt2, txt3).ratio() > 0.8:
                        dup = True
                        break
            if not dup:
                dedup.append((hx2, txt2))
        lines_out.append(" ".join(t[1] for t in dedup))
        cur = [(hx, text)]
    last_y = cy
if cur:
    cur.sort(key=lambda t: t[0])
    dedup = []
    for hx2, txt2 in cur:
        dup = False
        for hx3, txt3 in dedup:
            if txt2 == txt3 or txt2 in txt3 or txt3 in txt2:
                dup = True
                break
            if len(txt2) > 6 and len(txt3) > 6:
                import difflib
                if difflib.SequenceMatcher(None, txt2, txt3).ratio() > 0.8:
                    dup = True
                    break
        if not dup:
            dedup.append((hx2, txt2))
    lines_out.append(" ".join(t[1] for t in dedup))

# 去除相邻完全重复的整行（切片重叠）
final = []
for l in lines_out:
    if final and l.strip() == final[-1].strip():
        continue
    final.append(l)
lines_out = final

# 去噪：删除纯数字 token（截图边缘的页码/坐标噪点）
def clean_line(line):
    toks = line.split()
    kept = [t for t in toks if not re.fullmatch(r"\d+[cC]?", t)]
    return " ".join(kept)

cleaned = [clean_line(l) for l in lines_out if l.strip()]
out_text = "\n".join(cleaned)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(out_text)

print("saved:", OUT, "lines:", len(cleaned), "chars:", len(out_text))
