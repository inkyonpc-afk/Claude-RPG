"""Check what the FTB Quests map shows when each chapter opens, without starting the game.

Replicates FTB Quests 2001.4.22 (QuestPanel.updateMinMax / alignWidgets / resetScroll, QuestScreen zoom 16, theme quest_spacing 1.0) on the
generated chapter files and reports, per chapter, how many quests are inside the visible map area of the opening view. Also flags chapter
images whose `alpha` FTB reads as 0 (ChapterImage.readData uses nbt.getInt, so a double such as 0.55d floors to 0 = invisible).

Why: a chapter image counts toward the map's bounding box and FTB centers the opening view on that box. FTB treats an image's x/y as its
CENTER; an image placed by its top-left corner shifts the view off the quests, and with alpha 0 the map then looks empty.

Usage: python tools/questmap_check.py [--dir config/ftbquests/quests/chapters] [--spacing 1.0] [--zoom 16] [--verbose]
Exit code 1 if any chapter opens with no quest in view at a common screen size, or any image is effectively invisible."""
import argparse, glob, math, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# GUI-scaled screen sizes (window / GUI scale) the opening view must work at: 1280x720 at auto scale 3 and 2, 1920x1080 at 4, 3 and 2.
SCREENS = [(426, 240), (640, 360), (480, 270), (640, 360), (960, 540)]


# ---- minimal SNBT reader (FTB Library format: unquoted keys, newline- or comma-separated entries, typed number suffixes) ----------------------
class SnbtError(ValueError):
    pass


def parse_snbt(text):
    pos = [0]
    n = len(text)

    def ws():
        while pos[0] < n:
            c = text[pos[0]]
            if c in " \t\r\n,":
                pos[0] += 1
            elif c == "#" or text.startswith("//", pos[0]):
                while pos[0] < n and text[pos[0]] != "\n":
                    pos[0] += 1
            else:
                break

    def string():
        quote = text[pos[0]]
        pos[0] += 1
        out = []
        while pos[0] < n:
            c = text[pos[0]]
            if c == "\\":
                nxt = text[pos[0] + 1]
                out.append({"n": "\n", "t": "\t"}.get(nxt, nxt))
                pos[0] += 2
            elif c == quote:
                pos[0] += 1
                return "".join(out)
            else:
                out.append(c)
                pos[0] += 1
        raise SnbtError("unterminated string")

    def bare():
        start = pos[0]
        while pos[0] < n and (text[pos[0]].isalnum() or text[pos[0]] in "_-.+"):
            pos[0] += 1
        if start == pos[0]:
            raise SnbtError("unexpected %r at %d" % (text[pos[0]:pos[0] + 20], pos[0]))
        return text[start:pos[0]]

    def scalar(tok):
        if tok in ("true", "false"):
            return tok == "true"
        m = re.fullmatch(r"([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)([bBsSlLfFdD]?)", tok)
        if not m:
            return tok
        num, suf = m.group(1), m.group(2).lower()
        if suf in ("f", "d") or (not suf and any(c in num for c in ".eE")):
            return float(num)
        return int(num)

    def value():
        ws()
        c = text[pos[0]]
        if c == "{":
            pos[0] += 1
            obj = {}
            while True:
                ws()
                if text[pos[0]] == "}":
                    pos[0] += 1
                    return obj
                key = string() if text[pos[0]] in "\"'" else bare()
                ws()
                if text[pos[0]] != ":":
                    raise SnbtError("expected ':' after %s" % key)
                pos[0] += 1
                obj[key] = value()
        if c == "[":
            pos[0] += 1
            if re.match(r"[BIL];", text[pos[0]:pos[0] + 2]):
                pos[0] += 2
            arr = []
            while True:
                ws()
                if text[pos[0]] == "]":
                    pos[0] += 1
                    return arr
                arr.append(value())
        if c in "\"'":
            return string()
        return scalar(bare())

    result = value()
    ws()
    if pos[0] != n:
        raise SnbtError("trailing data at %d" % pos[0])
    return result


# ---- FTB Quests 2001.4.22 opening-view replica ---------------------------------------------------------------------------------------------
def java_round(v):
    return int(math.floor(v + 0.5))


def opening_view(chapter, screen_w, screen_h, zoom=16, spacing=1.0):
    """Return (visible quest titles, all quest titles, view center in quest units) for the view FTB shows when the chapter is selected."""
    items = []
    for img in chapter.get("images", []):
        if img.get("dev") or img.get("dependency"):
            continue   # editor-only or dependency-gated images are not added for players (QuestPanel.addWidgets)
        items.append(("image", None, img.get("x", 0.0), img.get("y", 0.0), img.get("width", 0.0), img.get("height", 0.0)))
    default_size = chapter.get("default_quest_size", 1.0)
    for qd in chapter.get("quests", []):
        size = qd.get("size", 0.0) or default_size
        items.append(("quest", qd.get("title", qd.get("id")), qd.get("x", 0.0), qd.get("y", 0.0), size, size))
    if not items:
        return [], [], (0.0, 0.0)
    min_x = min(x - w / 2 for _, _, x, _, w, _ in items) - 40
    min_y = min(y - h / 2 for _, _, _, y, _, h in items) - 30
    max_x = max(x + w / 2 for _, _, x, _, w, _ in items) + 40
    max_y = max(y + h / 2 for _, _, _, y, _, h in items) + 30
    bs, bp = zoom * 3 / 2, zoom * spacing / 4
    scroll_w, scroll_h = (max_x - min_x) * (bs + bp), (max_y - min_y) * (bs + bp)
    px, py, pw, ph = 20, 1, screen_w - 40, screen_h - 2          # QuestPanel.setPosAndSize(20, 1, width - 40, height - 2)
    off_x, off_y = int(-((scroll_w - pw) / 2)), int(-((scroll_h - ph) / 2))   # resetScroll, then Panel.setOffset: (int) -scroll
    visible, titles = [], []
    for kind, title, x, y, w, h in items:
        if kind != "quest":
            continue
        titles.append(title)
        wx = java_round((x - min_x - w / 2) * (bs + bp) + bp / 2 + bp * (w - 1) / 2)
        wy = java_round((y - min_y - h / 2) * (bs + bp) + bp / 2 + bp * (h - 1) / 2)
        ww, wh = java_round(bs * w), java_round(bs * h)
        sx, sy = px + off_x + wx, py + off_y + wy
        if sx < px + pw and sx + ww > px and sy < py + ph and sy + wh > py:
            visible.append(title)
    center = (min_x + (pw / 2 - off_x) / (bs + bp), min_y + (ph / 2 - off_y) / (bs + bp))
    return visible, titles, center


def check_dir(chapter_dir, zoom=16, spacing=1.0, verbose=False, out=print):
    problems = []
    files = sorted(glob.glob(os.path.join(chapter_dir, "*.snbt")))
    for f in files:
        ch = parse_snbt(open(f, encoding="utf-8").read())
        name = os.path.basename(f)
        for img in ch.get("images", []):
            alpha = img.get("alpha", 255)
            if int(math.floor(alpha)) <= 0:
                problems.append("%s: image %s alpha %r is read as %d (invisible); FTB stores alpha as an int 0-255" % (name, img.get("image"), alpha, int(math.floor(alpha))))
        worst = None
        for sw, sh in sorted(set(SCREENS)):
            visible, titles, center = opening_view(ch, sw, sh, zoom, spacing)
            if titles and (worst is None or len(visible) < len(worst[0])):
                worst = (visible, titles, center, (sw, sh))
            if titles and not visible:
                problems.append("%s: opening view at %dx%d GUI px shows 0 of %d quests (view centered at %.1f, %.1f)" % (name, sw, sh, len(titles), center[0], center[1]))
        if verbose and worst:
            visible, titles, center, (sw, sh) = worst
            out("%-28s worst %dx%d: %2d/%2d quests in view, center (%.1f, %.1f)" % (name, sw, sh, len(visible), len(titles), center[0], center[1]))
    return files, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(ROOT, "config", "ftbquests", "quests", "chapters"))
    ap.add_argument("--zoom", type=int, default=16)
    ap.add_argument("--spacing", type=float, default=1.0, help="theme quest_spacing (FTB default 1.0)")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    files, problems = check_dir(a.dir, a.zoom, a.spacing, a.verbose)
    for p in problems:
        print("PROBLEM", p)
    print("chapters: %d | problems: %d" % (len(files), len(problems)))
    sys.exit(1 if problems or not files else 0)


if __name__ == "__main__":
    main()
