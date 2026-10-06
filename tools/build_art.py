"""Procedural art for Embers of Aldreth: quest chapter backgrounds (PIL), written into the Paxi resource pack
config/paxi/resourcepacks/aldreth_core (textures at aldreth:textures/quests/<theme>.png).
Usage: python tools/build_art.py
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "config", "paxi", "resourcepacks", "aldreth_core")
QDIR = os.path.join(OUT, "assets", "aldreth", "textures", "quests")
os.makedirs(QDIR, exist_ok=True)
open(os.path.join(OUT, "pack.mcmeta"), "w").write('{"pack": {"pack_format": 15, "description": "Embers of Aldreth: generated art (quest backgrounds, menus)"}}')
W, H = 1280, 720

# theme: (top rgb, bottom rgb, accent rgb, motif)
THEMES = {
    "prologue": ((38, 22, 20), (10, 6, 8), (255, 150, 60), "embers"),
    "act1": ((30, 60, 40), (8, 20, 14), (240, 200, 90), "peaks"),
    "act2": ((44, 24, 70), (12, 8, 24), (120, 220, 150), "trees"),
    "act3": ((30, 70, 120), (10, 20, 50), (250, 230, 160), "clouds"),
    "act4": ((10, 40, 50), (2, 8, 12), (90, 220, 210), "rings"),
    "act5": ((40, 10, 70), (4, 2, 14), (230, 140, 255), "stars"),
    "postgame": ((90, 20, 30), (16, 4, 8), (255, 210, 120), "rings"),
    "skilltree": ((20, 24, 60), (4, 6, 20), (180, 200, 255), "stars"),
    "weapons": ((60, 40, 30), (14, 8, 6), (230, 190, 120), "blades"),
    "armor": ((40, 50, 62), (8, 10, 16), (190, 210, 230), "rings"),
    "apotheosis": ((70, 50, 20), (16, 10, 4), (255, 220, 110), "gems"),
    "enchanting": ((40, 30, 80), (8, 6, 20), (170, 140, 255), "runes"),
    "irons": ((20, 40, 90), (4, 8, 24), (120, 180, 255), "runes"),
    "ars": ((60, 30, 90), (14, 6, 24), (210, 140, 255), "runes"),
    "goety": ((24, 50, 36), (4, 12, 8), (130, 255, 160), "runes"),
    "accessories": ((70, 40, 60), (16, 8, 14), (255, 170, 210), "gems"),
    "traversal": ((60, 70, 40), (12, 16, 8), (210, 230, 150), "peaks"),
    "mounts": ((70, 50, 30), (16, 10, 6), (240, 200, 140), "peaks"),
    "flying": ((40, 80, 120), (10, 20, 40), (255, 245, 200), "clouds"),
    "structures": ((50, 50, 56), (10, 10, 14), (200, 200, 210), "rings"),
    "dimensions": ((40, 20, 80), (6, 4, 18), (120, 255, 240), "rings"),
    "bosses": ((80, 20, 20), (16, 4, 4), (255, 120, 90), "blades"),
    "secrets": ((20, 20, 30), (2, 2, 6), (200, 160, 255), "stars"),
    "farming": ((60, 80, 30), (14, 18, 6), (250, 230, 120), "peaks"),
    "fishing": ((20, 60, 90), (4, 12, 24), (160, 230, 255), "waves"),
    "building": ((80, 60, 40), (18, 12, 8), (240, 210, 170), "rings"),
    "animals": ((40, 80, 50), (8, 18, 10), (200, 240, 170), "trees"),
    "bounties": ((70, 30, 20), (14, 6, 4), (255, 190, 100), "blades"),
    "default": ((30, 30, 50), (6, 6, 14), (200, 200, 240), "stars"),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(top, bottom):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bottom, y / H))
    return img


def noise(img, rnd, amount=10):
    px = img.load()
    for _ in range(W * H // 6):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r, g, b = px[x, y]
        k = rnd.randint(-amount, amount)
        px[x, y] = (max(0, min(255, r + k)), max(0, min(255, g + k)), max(0, min(255, b + k)))
    return img


def glow(layer, radius=6):
    return layer.filter(ImageFilter.GaussianBlur(radius))


def motif(name, accent, rnd):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = accent
    if name == "stars":
        for _ in range(260):
            x, y, s = rnd.randrange(W), rnd.randrange(H), rnd.random()
            r = 1 + (s > 0.93) * 2
            d.ellipse([x - r, y - r, x + r, y + r], fill=a + (int(80 + 150 * s),))
        pts = [(rnd.randrange(120, W - 120), rnd.randrange(80, H - 80)) for _ in range(9)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=a + (60,), width=1)
    elif name == "rings":
        cx, cy = W // 2 + rnd.randint(-120, 120), H // 2 + rnd.randint(-60, 60)
        for i, r in enumerate(range(90, 520, 55)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=a + (70,), width=2)
            for k in range(14 + i * 2):
                ang = k * 2 * math.pi / (14 + i * 2) + i
                d.line([(cx + math.cos(ang) * (r - 9), cy + math.sin(ang) * (r - 9)), (cx + math.cos(ang) * (r + 9), cy + math.sin(ang) * (r + 9))], fill=a + (90,), width=2)
    elif name == "runes":
        cx, cy = W // 2, H // 2
        for r in (150, 250, 340):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=a + (80,), width=2)
        for k in range(36):
            ang = k * math.pi / 18
            r = 340 + rnd.randint(-8, 8)
            x, y = cx + math.cos(ang) * r, cy + math.sin(ang) * r
            glyph = [(x + rnd.randint(-10, 10), y + rnd.randint(-10, 10)) for _ in range(rnd.randint(3, 5))]
            d.line(glyph, fill=a + (140,), width=2)
        d.polygon([(cx + math.cos(k * 2 * math.pi / 5 + 1.57) * 250, cy + math.sin(k * 2 * math.pi / 5 + 1.57) * 250) for k in (0, 2, 4, 1, 3)], outline=a + (70,))
    elif name == "peaks":
        for layer_i, (base, col) in enumerate(((470, 50), (540, 80), (620, 120))):
            pts = [(0, H)]
            x = 0
            while x <= W + 80:
                pts.append((x, base + rnd.randint(-110, 40) + layer_i * 10))
                x += rnd.randint(60, 140)
            pts += [(W, H)]
            d.polygon(pts, fill=a + (col,))
    elif name == "trees":
        for _ in range(26):
            x = rnd.randrange(W)
            h = rnd.randint(160, 520)
            d.rectangle([x - 5, H - h, x + 5, H], fill=a + (60,))
            for k in range(5):
                yy = H - h + k * 38
                d.polygon([(x, yy - 20), (x - 50 + k * 4, yy + 40), (x + 50 - k * 4, yy + 40)], fill=a + (50,))
    elif name == "clouds":
        for _ in range(26):
            x, y = rnd.randrange(-100, W), rnd.randrange(60, H - 60)
            for k in range(6):
                rx = rnd.randint(40, 110)
                d.ellipse([x + k * 40, y - rx // 2, x + k * 40 + rx * 2, y + rx // 2], fill=a + (rnd.randint(20, 60),))
    elif name == "blades":
        for _ in range(16):
            x, y, l = rnd.randrange(W), rnd.randrange(H), rnd.randint(160, 420)
            ang = rnd.choice((-0.6, -0.5, 0.6, 0.5)) + math.pi / 2
            x2, y2 = x + math.cos(ang) * l, y + math.sin(ang) * l
            d.line([(x, y), (x2, y2)], fill=a + (90,), width=3)
            d.line([(x - 18 * math.cos(ang + 1.57), y - 18 * math.sin(ang + 1.57)), (x + 18 * math.cos(ang + 1.57), y + 18 * math.sin(ang + 1.57))], fill=a + (120,), width=3)
    elif name == "gems":
        for _ in range(40):
            x, y, s = rnd.randrange(W), rnd.randrange(H), rnd.randint(14, 46)
            d.polygon([(x, y - s), (x + s * 0.7, y), (x, y + s), (x - s * 0.7, y)], outline=a + (120,), fill=a + (rnd.randint(14, 44),))
    elif name == "waves":
        for k in range(14):
            y0 = 120 + k * 42
            pts = [(x, y0 + math.sin(x / 55 + k) * 14) for x in range(0, W + 20, 20)]
            d.line(pts, fill=a + (70,), width=3)
    elif name == "embers":
        for _ in range(180):
            x, y, s = rnd.randrange(W), rnd.randrange(H), rnd.random()
            r = 1 + s * 3
            d.ellipse([x - r, y - r, x + r, y + r], fill=a + (int(60 + 160 * s),))
    return layer


def vignette(img):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-W * 0.25, -H * 0.4, W * 1.25, H * 1.4], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(img, dark, mask)


for name, (top, bottom, accent, mot) in THEMES.items():
    rnd = random.Random(hash(name) & 0xFFFFFF)
    rnd.seed(sum(ord(c) * (i + 3) for i, c in enumerate(name)))
    img = noise(gradient(top, bottom), rnd)
    layer = motif(mot, accent, rnd)
    img = Image.alpha_composite(img.convert("RGBA"), glow(layer, 3)).convert("RGB")
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    img = vignette(img)
    img.save(os.path.join(QDIR, name + ".png"), optimize=True)
print("themes:", len(THEMES), "->", QDIR)
