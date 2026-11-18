"""Build web images, the tree mark, favicons, the icon sprite and the WhatsApp/social share image.

Run from the project root:  python -I tools/build_assets.py
Needs Pillow and fontTools (with brotli). Raw images live in _source/ (not in git).
"""
import io
import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_source")
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)

CHAR = (20, 19, 18)
BONE = (236, 230, 220)
MUTED = (176, 166, 152)
EMBER = (232, 116, 52)

IMAGES = {
    "hero-wide": ("gen/hero-wide.png", (960, 1536)),
    "hero-tall": ("gen/hero-tall.png", (480, 864)),
    "steaks": ("gen/steaks.png", (560, 1024)),
    "wors": ("gen/wors.png", (720, 1280)),
    "sosaties": ("gen/sosaties.png", (800, 1536)),
    "crumbed": ("gen/crumbed.png", (560, 1024)),
    "deli": ("gen/deli.png", (800, 1536)),
    "braai": ("gen/braai.png", (960, 1536)),
    "counter": ("gen/counter.png", (720, 1280)),
}


def load(rel):
    return Image.open(os.path.join(SRC, rel)).convert("RGB")


def save_sizes(name, im, widths):
    sizes = []
    for w in widths:
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        q = 72 if name.startswith("hero") else 78
        im.resize((w, h), Image.LANCZOS).save(
            os.path.join(OUT, f"{name}-{w}.webp"), "WEBP", quality=q, method=6)
        sizes.append((w, h))
    return sizes


_CACHE = {}


def font(path, size, **axes):
    key = (path, tuple(sorted(axes.items())))
    if key not in _CACHE:
        from fontTools.varLib.instancer import instantiateVariableFont
        f = TTFont(path)
        f.flavor = None
        if "fvar" in f:
            names = [a.axisTag for a in f["fvar"].axes]
            f = instantiateVariableFont(f, {n: axes.get(n, 400) for n in names})
        buf = io.BytesIO()
        f.save(buf)
        _CACHE[key] = buf.getvalue()
    return ImageFont.truetype(io.BytesIO(_CACHE[key]), size)


DISPLAY = os.path.join(ROOT, "assets", "fonts", "bigshoulders.woff2")
BODY = os.path.join(ROOT, "assets", "fonts", "figtree.woff2")


def tree(color, width=None):
    t = Image.open(os.path.join(SRC, "gen", "tree.png")).convert("RGBA")
    solid = Image.new("RGBA", t.size, color + (255,))
    solid.putalpha(t.getchannel("A"))
    if width:
        solid = solid.resize((width, round(t.height * width / t.width)), Image.LANCZOS)
    return solid


def marks():
    for w in (64, 128):
        tree(BONE, w).save(os.path.join(OUT, f"tree-{w}.png"), optimize=True)


def icon(size, pad=.14, radius=.22):
    sc = 4
    s = size * sc
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * radius), fill=CHAR)
    # ember sun low behind the tree
    r = int(s * .17)
    cx, cy = int(s * .5), int(s * .6)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=EMBER)
    if size < 64:
        pad = .05
    tw = int(s * (1 - 2 * pad))
    t = tree(BONE, tw)
    if size < 64:  # fatten fine branches so they survive at favicon size
        a = t.getchannel("A").filter(ImageFilter.MaxFilter(5))
        t.putalpha(a)
    im.alpha_composite(t, ((s - t.width) // 2, int(s * .80) - t.height))
    d.rectangle((int(s * .1), int(s * .8), int(s * .9), int(s * .8) + max(sc, s // 60)), fill=BONE)
    return im.resize((size, size), Image.LANCZOS)


def favicons():
    for n in (16, 32, 48, 96):
        icon(n).save(os.path.join(ROOT, f"favicon-{n}.png"))
    ico = [icon(n) for n in (16, 32, 48)]
    ico[2].save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    for n, fn in ((192, "icon-192.png"), (512, "icon-512.png")):
        icon(n).save(os.path.join(ROOT, fn))
    icon(180, radius=0).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"))
    bg = Image.new("RGBA", (512, 512), CHAR + (255,))
    bg.alpha_composite(icon(360, radius=0), (76, 76))
    bg.convert("RGB").save(os.path.join(ROOT, "icon-maskable-512.png"))


def og():
    """WhatsApp / social preview: the hero dusk photo with the name set over the dark sky."""
    W, H = 1200, 630
    photo = load("gen/hero-wide.png")
    r = max(W / photo.width, H / photo.height)
    photo = photo.resize((round(photo.width * r), round(photo.height * r)), Image.LANCZOS)
    x = (photo.width - W) // 2
    im = photo.crop((x, 0, x + W, H)).convert("RGBA")
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    for i in range(W):
        sd.line([(i, 0), (i, H)], fill=int(max(0, 215 - i * .3)))
    im = Image.composite(Image.new("RGBA", (W, H), CHAR + (255,)), im, shade)
    im.alpha_composite(tree(BONE, 120), (64, 60))
    d = ImageDraw.Draw(im)
    d.text((62, 168), "WILD BUTCHERY", font=font(DISPLAY, 96, wght=800), fill=BONE)
    d.text((64, 282), "No need to bring meat.", font=font(BODY, 40, wght=600), fill=EMBER)
    sub = font(BODY, 27, wght=450)
    d.text((64, 350), "Steaks, boerewors, biltong and sosaties", font=sub, fill=BONE)
    d.text((64, 386), "for your braai in Marloth Park.", font=sub, fill=BONE)
    d.text((64, 520), "Bush Centre, Marloth Park   |   064 072 5121", font=font(BODY, 25, wght=600), fill=MUTED)
    im.convert("RGB").save(os.path.join(OUT, "og-share.jpg"), quality=86, optimize=True, progressive=True)


def icons():
    src = os.path.join(SRC, "dl", "icons")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for fn in sorted(os.listdir(src)):
        body = open(os.path.join(src, fn), encoding="utf-8").read()
        inner = re.search(r"<svg[^>]*>(.*)</svg>", body, re.S).group(1)
        out.append(f'<symbol id="i-{fn[:-4]}" viewBox="0 0 256 256" fill="currentColor">{inner}</symbol>')
    out.append("</svg>")
    open(os.path.join(ROOT, "assets", "icons.svg"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    lines = []
    for name, (rel, widths) in IMAGES.items():
        sizes = save_sizes(name, load(rel), widths)
        lines.append(f"{name}: " + ", ".join(f"{w}x{h}" for w, h in sizes))
    with open(os.path.join(SRC, "sizes.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    marks()
    favicons()
    og()
    icons()
    print("\n".join(lines))
