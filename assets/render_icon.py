#!/usr/bin/env python3
"""渲染「金融宣教 / Financial Literacy Education」品牌图标。

设计：深蓝 #071789 底 + 纯白扁平剪影（取自参考图 2816.JPG 的配色与负空间语言），
图形为「翻开的书 + 带 ¥ 的圆币 + 三道知识传播线」——书=知识普及，币=金融。

输出（4x 超采样抗锯齿）：
  ../_icon.png                 512x512，SkillHub / WorkBuddy 技能图标（含中英文名称）
  ./avatar-512.png             512x512，专家头像（纯图形，无文字）
  ./logo-horizontal.png       1200x320，横版标志（白底，README / 页眉 / 物料落款）

重新生成：python3 render_icon.py
仅依赖 Pillow；字体使用 macOS 自带 Hiragino Sans GB（W6 粗体 / W3 细体）。
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

S = 4  # 超采样倍数

BLUE = (7, 23, 137, 255)        # #071789 主蓝
BLUE_SOFT = (74, 86, 168, 255)  # #4A56A8 辅助蓝（仅横版副标题）
WHITE = (255, 255, 255, 255)
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"


# --------------------------------------------------------------------------
# 基础几何
# --------------------------------------------------------------------------
def cubic(p0, p1, p2, p3, n=40):
    """三次贝塞尔曲线采样为折线点列（与 SVG 的 C 指令控制点一致）。"""
    pts = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def page_left():
    """左书页轮廓，(x, y) 为 512 图标基准坐标。"""
    return (
        [(249, 306)]
        + cubic((249, 306), (208, 276), (146, 258), (92, 258))
        + [(92, 304)]
        + cubic((92, 304), (150, 304), (208, 320), (249, 346))
    )


def page_right():
    """右书页轮廓（左页沿 x=256 镜像）。"""
    return [(512 - x, y) for x, y in page_left()]


def draw_stroke(d, tf, pts, width, color):
    """画带圆头的折线。width 为基准坐标下的线宽（已含 scale 调整）。"""
    w = max(1, int(round(width * S)))
    p = [tf(x, y) for x, y in pts]
    d.line(p, fill=color, width=w, joint="curve")
    r = w / 2
    for x, y in (p[0], p[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def draw_mark(d, tf, scale):
    """绘制无文字的图形标志。

    tf: (x, y) -> (X, Y) 超采样后的画布坐标
    scale: 图形缩放系数，用于同步缩放线宽
    """
    lw = lambda v: v * scale  # 线宽缩放

    # 圆币
    x0, y0 = tf(186, 72)
    x1, y1 = tf(326, 212)
    d.ellipse([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=WHITE)

    # ¥ 符号：用背景蓝在白币上挖出负空间
    for pts in (
        [(226, 108), (256, 148), (286, 108)],
        [(256, 148), (256, 186)],
        [(224, 154), (288, 154)],
        [(224, 172), (288, 172)],
    ):
        draw_stroke(d, tf, pts, lw(10), BLUE)

    # 三道知识传播线
    for pts in (
        [(228, 226), (284, 226)],
        [(237, 236), (275, 236)],
        [(245, 246), (267, 246)],
    ):
        draw_stroke(d, tf, pts, lw(8), WHITE)

    # 翻开的书（中间 V 形留蓝形成书脊）
    d.polygon([tf(x, y) for x, y in page_left()], fill=WHITE)
    d.polygon([tf(x, y) for x, y in page_right()], fill=WHITE)

    # 书页上的文字行：以背景蓝挖出，呼应参考图的负空间语言
    for pts in (
        [(118, 276), (204, 292)],
        [(118, 292), (204, 308)],
        [(394, 276), (308, 292)],
        [(394, 292), (308, 308)],
    ):
        draw_stroke(d, tf, pts, lw(7), BLUE)


def font(size, bold=False):
    return ImageFont.truetype(FONT, int(size * S), index=2 if bold else 0)


def tracked_text(d, text, cx, baseline, size, tracking, color, bold=False, anchor_left=None):
    """逐字符绘制带字距的英文。cx 为居中位置；anchor_left 给定时改为左对齐。"""
    f = font(size, bold)
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * S * (len(text) - 1)
    x = (cx * S - total / 2) if anchor_left is None else (anchor_left * S)
    for ch, w in zip(text, widths):
        d.text((x, baseline * S), ch, font=f, fill=color, anchor="ls")
        x += w + tracking * S


def save(img, w, h, path):
    out = img.resize((w, h), Image.LANCZOS).convert("RGB")
    out.save(path, optimize=True)
    print(f"saved {path.relative_to(ROOT)}  {w}x{h}")


# --------------------------------------------------------------------------
# 1) 主图标 _icon.png（512x512，含中英文名称）
# --------------------------------------------------------------------------
def render_icon():
    img = Image.new("RGBA", (512 * S, 512 * S), BLUE)
    d = ImageDraw.Draw(img)
    tf = lambda x, y: (x * S, y * S)
    draw_mark(d, tf, 1.0)

    d.text((256 * S, 422 * S), "金融宣教", font=font(58, True),
           fill=WHITE, anchor="ms")
    tracked_text(d, "FINANCIAL LITERACY EDUCATION", 256, 458, 15, 2.0,
                 (215, 220, 248, 255), bold=True)
    save(img, 512, 512, ROOT / "_icon.png")


# --------------------------------------------------------------------------
# 2) 专家头像 avatar-512.png（纯图形，居中放大 1.15 倍）
# --------------------------------------------------------------------------
def render_avatar():
    s = 1.15
    img = Image.new("RGBA", (512 * S, 512 * S), BLUE)
    d = ImageDraw.Draw(img)
    tf = lambda x, y: ((256 + (x - 256) * s) * S, (256 + (y - 209) * s) * S)
    draw_mark(d, tf, s)
    save(img, 512, 512, HERE / "avatar-512.png")


# --------------------------------------------------------------------------
# 3) 横版标志 logo-horizontal.png（1200x320，白底）
# --------------------------------------------------------------------------
def render_horizontal():
    w, h = 1200, 320
    s = 0.72
    img = Image.new("RGBA", (w * S, h * S), WHITE)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([24 * S, 24 * S, 296 * S, 296 * S],
                        radius=44 * S, fill=BLUE)
    tf = lambda x, y: ((160 + (x - 256) * s) * S, (160 + (y - 209) * s) * S)
    draw_mark(d, tf, s)

    d.text((348 * S, 146 * S), "金融宣教", font=font(76, True),
           fill=BLUE, anchor="ls")
    tracked_text(d, "FINANCIAL LITERACY EDUCATION", 0, 192, 21, 1.6,
                 BLUE_SOFT, bold=True, anchor_left=352)
    d.rounded_rectangle([352 * S, 215.5 * S, 472 * S, 220.5 * S],
                        radius=2.5 * S, fill=BLUE)
    d.text((352 * S, 258 * S), "公益性 · 普惠性 · 让金融知识走进日常生活",
           font=font(22), fill=BLUE_SOFT, anchor="ls")
    save(img, w, h, HERE / "logo-horizontal.png")


if __name__ == "__main__":
    render_icon()
    render_avatar()
    render_horizontal()
