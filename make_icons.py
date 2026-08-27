#!/usr/bin/env python3
"""生成足球小程序 PWA 图标 (绿底+金色足球)"""
from PIL import Image, ImageDraw
import math, os

def make_icon(size, path, maskable=False):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 圆形/圆角背景
    pad = 0 if maskable else int(size*0.06)
    bg = (11, 93, 59, 255)
    if maskable:
        d.rounded_rectangle([0,0,size,size], radius=int(size*0.18), fill=bg)
    else:
        d.ellipse([pad,pad,size-pad,size-pad], fill=bg)
    # 中心圆(足球底色白)
    cx = cy = size/2
    R = size*0.30
    d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=(248,248,248,255))
    # 五边形(黑色中心)
    pent = []
    for i in range(5):
        ang = -90 + i*72
        pent.append((cx+R*0.42*math.cos(math.radians(ang)), cy+R*0.42*math.sin(math.radians(ang))))
    d.polygon(pent, fill=(30,30,30,255))
    # 黑色接线(五边形顶点到外圆,形成足球纹路)
    for p in pent:
        d.line([p, (cx,cy)], fill=(30,30,30,255), width=max(2,int(size*0.02)))
    # 保存
    img.save(path, "PNG")

os.makedirs("icons", exist_ok=True)
make_icon(192, "icons/icon-192.png")
make_icon(512, "icons/icon-512.png")
make_icon(512, "icons/icon-maskable-512.png", maskable=True)
print("图标生成完成:", os.listdir("icons"))
