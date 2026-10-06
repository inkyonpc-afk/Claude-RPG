"""Title-screen identity for Embers of Aldreth: panorama cube faces, logo, edition tagline, splash texts, pack icon.
Writes into config/paxi/resourcepacks/aldreth_core (loaded globally via Paxi). Usage: python tools/build_menu_art.py"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RP = os.path.join(ROOT, "config", "paxi", "resourcepacks", "aldreth_core")
TITLE = os.path.join(RP, "assets", "minecraft", "textures", "gui", "title")
os.makedirs(os.path.join(TITLE, "background"), exist_ok=True)
os.makedirs(os.path.join(RP, "assets", "minecraft", "texts"), exist_ok=True)
rng = np.random.default_rng(7)
W, H = 4096, 2048


def periodic_noise(n, octaves=6, seed=1):
    r = np.random.default_rng(seed)
    x = np.linspace(0, 2 * np.pi, n, endpoint=False)
    y = np.zeros(n)
    for o in range(1, octaves + 1):
        f = 2 ** o
        y += r.uniform(0.5, 1) / o * np.sin(f * x + r.uniform(0, 2 * np.pi))
        y += r.uniform(0.3, 0.6) / o * np.sin((f + 1) * x + r.uniform(0, 2 * np.pi))
    y = (y - y.min()) / (y.max() - y.min())
    return y


# ---------------------------------------------------------------- equirect scene
yy = np.linspace(0, 1, H)[:, None]            # 0 = zenith, 1 = nadir
xx = np.linspace(0, 1, W, endpoint=False)[None, :]
horizon = 0.5
sky_top = np.array([14, 10, 40]); sky_mid = np.array([92, 36, 70]); sky_hor = np.array([255, 150, 70])
t = np.clip(yy / horizon, 0, 1)
sky = np.where(t[..., None] < 0.55, sky_top + (sky_mid - sky_top) * (t[..., None] / 0.55), sky_mid + (sky_hor - sky_mid) * ((t[..., None] - 0.55) / 0.45))
img = np.broadcast_to(sky, (H, W, 3)).copy()
img[int(horizon * H):] = np.array([12, 8, 14])
pil = Image.fromarray(np.clip(img, 0, 255).astype("uint8"))
d = ImageDraw.Draw(pil, "RGBA")

# stars
for _ in range(2600):
    x, y = rng.integers(0, W), rng.integers(0, int(horizon * H * 0.8))
    b = int(120 + 135 * rng.random() ** 2)
    r = 1 if rng.random() < 0.92 else 2
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 230, b))

# the Ember: a huge broken crown-moon, and aurora ribbons
cx, cy = int(W * 0.30), int(H * 0.28)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
for rad, a in ((380, 40), (260, 70), (170, 110), (110, 180)):
    g.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 150, 70, a))
glow = glow.filter(ImageFilter.GaussianBlur(40))
pil = Image.alpha_composite(pil.convert("RGBA"), glow)
d = ImageDraw.Draw(pil, "RGBA")
d.ellipse([cx - 92, cy - 92, cx + 92, cy + 92], fill=(255, 226, 170, 255))
for k in range(7):   # broken crown spikes
    ang = k * 2 * math.pi / 7 + 0.3
    d.polygon([(cx + math.cos(ang) * 92, cy + math.sin(ang) * 92), (cx + math.cos(ang - 0.12) * 150, cy + math.sin(ang - 0.12) * 150),
               (cx + math.cos(ang + 0.12) * 150, cy + math.sin(ang + 0.12) * 150)], fill=(255, 210, 140, 200))
for band in range(3):
    base = 0.18 + band * 0.07
    n = periodic_noise(W, 4, 30 + band)
    pts = [(x, int((base + 0.10 * n[x]) * H)) for x in range(0, W, 16)]
    for dy in range(0, 60, 3):
        d.line([(x, y + dy) for x, y in pts], fill=(120 + band * 40, 255 - band * 60, 200, max(2, 22 - dy // 3)), width=3)

# floating islands
for _ in range(16):
    x, y = rng.integers(0, W), rng.integers(int(H * 0.28), int(H * 0.46))
    w, h = rng.integers(60, 170), rng.integers(14, 40)
    d.polygon([(x - w, y), (x + w, y), (x + w * 0.5, y + h * 1.6), (x, y + h * 2.2), (x - w * 0.4, y + h * 1.5)], fill=(18, 12, 30, 235))
    d.ellipse([x - w, y - h // 2, x + w, y + h // 2], fill=(28, 52, 40, 240))
    for k in range(int(w // 18)):
        tx = x - w + 14 + k * 18 + rng.integers(-4, 4)
        d.polygon([(tx, y - h // 2), (tx - 5, y - h // 2 - 14), (tx + 5, y - h // 2 - 14)], fill=(14, 38, 28, 240))

# mountains (3 layers) with periodic ridges, a ruined tower and a castle silhouette on the nearest ridge
horizon_px = int(horizon * H)
for layer, (col, amp, off) in enumerate(((60, 0.17, -0.02), (36, 0.20, 0.0), (18, 0.24, 0.02))):
    n = periodic_noise(W, 7, 50 + layer)
    pts = [(0, H)] + [(x, int(horizon_px - amp * H * n[x] + off * H + 150)) for x in range(W)] + [(W - 1, H)]
    d.polygon(pts, fill=(col + 10, col, col + 34, 255))
n = periodic_noise(W, 7, 52)
for tx in rng.integers(0, W, 7):
    ground = int(horizon_px - 0.24 * H * n[tx] + 0.02 * H + 150)
    th = rng.integers(70, 190)
    d.rectangle([tx - 18, ground - th, tx + 18, ground], fill=(10, 8, 16, 255))
    d.polygon([(tx - 24, ground - th), (tx, ground - th - 46), (tx + 24, ground - th)], fill=(10, 8, 16, 255))
    d.rectangle([tx - 4, ground - th + 18, tx + 4, ground - th + 34], fill=(255, 190, 90, 255))   # lit window
# forest strip
for x in range(0, W, 9):
    hgt = int(30 + 90 * periodic_noise(W, 5, 80)[x] + rng.integers(0, 28))
    base = int(horizon_px + 60)
    d.polygon([(x, base), (x - 11, base), (x - 4, base - hgt), (x + 3, base - hgt - 16), (x + 11, base)], fill=(6, 8, 10, 255))
# embers / fireflies
for _ in range(900):
    x, y = rng.integers(0, W), rng.integers(int(H * 0.2), int(H * 0.75))
    r = rng.integers(1, 3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 190 + rng.integers(0, 60), 80, int(70 + 150 * rng.random())))
equi = np.asarray(pil.convert("RGB")).astype("float32")


def sample(u, v):
    """bilinear sample of equirect at u (0..1 wrapped), v (0..1)"""
    px = (u % 1.0) * W
    py = np.clip(v, 0, 1) * (H - 1)
    x0 = np.floor(px).astype(int) % W
    x1 = (x0 + 1) % W
    y0 = np.floor(py).astype(int)
    y1 = np.clip(y0 + 1, 0, H - 1)
    fx = (px - np.floor(px))[..., None]
    fy = (py - np.floor(py))[..., None]
    return equi[y0, x0] * (1 - fx) * (1 - fy) + equi[y0, x1] * fx * (1 - fy) + equi[y1, x0] * (1 - fx) * fy + equi[y1, x1] * fx * fy


S = 1024
a = (np.arange(S) + 0.5) / S * 2 - 1
U, V = np.meshgrid(a, a)
faces = {
    0: lambda: (U, -V, np.ones_like(U)),     # front  (+z)
    1: lambda: (np.ones_like(U), -V, -U),    # right  (+x)
    2: lambda: (-U, -V, -np.ones_like(U)),   # back   (-z)
    3: lambda: (-np.ones_like(U), -V, U),    # left   (-x)
    4: lambda: (U, np.ones_like(U), V),     # top (y up)
    5: lambda: (U, -np.ones_like(U), -V),   # bottom
}
for idx, fn in faces.items():
    x, y, z = fn()
    lon = np.arctan2(x, z)
    lat = np.arcsin(y / np.sqrt(x * x + y * y + z * z))   # +lat up
    u = lon / (2 * np.pi) + 0.5
    v = 0.5 - lat / np.pi
    out = np.clip(sample(u, v), 0, 255).astype("uint8")
    Image.fromarray(out).save(os.path.join(TITLE, "background", "panorama_%d.png" % idx), optimize=True)
Image.fromarray(np.clip(sample(np.linspace(0, 1, 360, endpoint=False)[None, :].repeat(180, 0), np.linspace(0, 1, 180)[:, None].repeat(360, 1)), 0, 255).astype("uint8")).save(os.path.join(TITLE, "background", "panorama_overlay.png"))

# ---------------------------------------------------------------- logo: 310x44 split into two 155x44 halves on a 256x256 sheet
def font(size, bold=True):
    for f in ("georgiab.ttf", "cambriab.ttf", "constanb.ttf", "georgia.ttf"):
        p = os.path.join("C:/Windows/Fonts", f)
        if os.path.isfile(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


logo = Image.new("RGBA", (310 * 4, 44 * 4), (0, 0, 0, 0))
ld = ImageDraw.Draw(logo)
text = "EMBERS OF ALDRETH"
size = 150
while True:
    ft = font(size)
    bbox = ld.textbbox((0, 0), text, font=ft)
    if (bbox[2] - bbox[0]) <= 1170 and (bbox[3] - bbox[1]) <= 150 or size <= 40:
        break
    size -= 4
tx = (logo.width - (bbox[2] - bbox[0])) // 2
ty = (logo.height - (bbox[3] - bbox[1])) // 2 - bbox[1]
glow = Image.new("RGBA", logo.size, (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.text((tx, ty), text, font=ft, fill=(255, 140, 50, 255))
glow = glow.filter(ImageFilter.GaussianBlur(14))
logo = Image.alpha_composite(logo, glow)
ld = ImageDraw.Draw(logo)
for off in range(6, 0, -1):
    ld.text((tx + off, ty + off), text, font=ft, fill=(40, 14, 6, 255))
ld.text((tx, ty), text, font=ft, fill=(255, 226, 170, 255))
# gradient tint: ember orange at the bottom of letters
grad = Image.new("RGBA", logo.size)
gp = grad.load()
for y in range(logo.height):
    for x in range(logo.width):
        k = y / logo.height
        gp[x, y] = (255, int(190 - 90 * k), int(110 - 80 * k), int(70 * k))
mask = Image.new("L", logo.size, 0)
ImageDraw.Draw(mask).text((tx, ty), text, font=ft, fill=255)
logo = Image.composite(Image.alpha_composite(logo, grad), logo, mask)
logo = logo.resize((310, 44), Image.LANCZOS)
sheet = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
sheet.paste(logo.crop((0, 0, 155, 44)), (0, 0))
sheet.paste(logo.crop((155, 0, 310, 44)), (0, 45))
sheet.save(os.path.join(TITLE, "minecraft.png"))
edition = Image.new("RGBA", (128, 14), (0, 0, 0, 0))
ed = ImageDraw.Draw(edition)
ef = font(10, False)
etext = "A FANTASY ACTION RPG"
eb = ed.textbbox((0, 0), etext, font=ef)
ed.text(((128 - (eb[2] - eb[0])) // 2, 1 - eb[1]), etext, font=ef, fill=(255, 200, 140, 255))
edition.save(os.path.join(TITLE, "edition.png"))

# ---------------------------------------------------------------- splashes
splash = ["The Ember remembers.", "Seven Wardens, one Crown.", "Roll! Roll! Roll!", "Mind the keystones.", "Fly only where the Wardens allow.", "A hero is a bad plan with good gear.",
          "Respec responsibly.", "Mounts are people too.", "Salvage everything.", "Never overfly a boss arena.", "Spend your points wisely.", "The Constellation is large.",
          "Dragons grow up.", "Keep your waystones close.", "Try the stew.", "Hybrid builds welcome.", "What's behind that portal?", "Gems are forever.", "Reforge your favourite.",
          "Embers of Aldreth!", "Now with more Wardens!", "620 stars!", "Everything has a price."]
open(os.path.join(RP, "assets", "minecraft", "texts", "splashes.txt"), "w", encoding="utf-8").write("\n".join(splash) + "\n")

# pack icon
icon = Image.new("RGBA", (128, 128), (20, 10, 30, 255))
idr = ImageDraw.Draw(icon)
for r, c in ((60, (255, 120, 60, 80)), (44, (255, 160, 80, 140)), (28, (255, 214, 150, 255))):
    idr.ellipse([64 - r, 64 - r, 64 + r, 64 + r], fill=c)
icon.save(os.path.join(RP, "pack.png"))
print("menu art done")
