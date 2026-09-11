"""Hook card + thumbnail compositor. Colors and fonts come from brand/brand.json.

The hook card is a 1080x1920 transparent PNG: two big lines inside a rounded panel,
sized to fit the frame. Overlay it on a frame (thumb) or on video with ffmpeg.

Usage:
  # two big lines; wrap ONE word of line 2 in {curly braces} to render it in the accent colour
  python scripts/cards.py hook --l1 "Half your life" --l2 "is on {autopilot}" -o work/hook.png

  # thumbnail: composite the hook card onto a frame grabbed from the cut (no captions)
  python scripts/cards.py thumb --frame work/last.png --hook work/hook.png -o export/THUMBNAIL.jpg
"""
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import brand as B
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SHADOW = (0, 0, 0, 120)


def _case(txt, mode):
    return txt.upper() if mode == "upper" else txt


def _tw(d, t, f):
    bb = d.textbbox((0, 0), t, font=f); return bb[2] - bb[0], bb[3] - bb[1]


def make_hook(l1, l2, out, b):
    """l2 may contain one {word} in braces -> rendered in hook_card.accent_color."""
    hc = b["hook_card"]
    panel = B.hex_to_rgba(hc["panel_color"], hc["panel_alpha"])
    accent = B.hex_to_rgba(hc["accent_color"])
    text_col = B.hex_to_rgba(hc["text_color"])
    l1 = _case(l1, hc["case"]); l2 = _case(l2, hc["case"])

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    pre, acc, post = l2, "", ""
    if "{" in l2 and "}" in l2:
        pre, rest = l2.split("{", 1); acc, post = rest.split("}", 1)

    # Auto-fit: shrink from 96 until BOTH lines fit the frame width, so short hooks
    # stay full size and only longer copy scales down.
    padx = 58
    maxw = W - 2 * padx - 24
    fs = 96
    while fs > 44:
        f1 = ImageFont.truetype(str(b["_font_display"]), fs)
        w1 = _tw(d, l1, f1)[0]
        wp = _tw(d, pre, f1)[0]; wa = _tw(d, acc, f1)[0]; wpo = _tw(d, post, f1)[0]
        if max(w1, wp + wa + wpo) <= maxw:
            break
        fs -= 2
    f1 = ImageFont.truetype(str(b["_font_display"]), fs)
    w1, h1 = _tw(d, l1, f1)
    wp, _ = _tw(d, pre, f1); wa, h2 = _tw(d, acc, f1); wpo, _ = _tw(d, post, f1)
    w2 = wp + wa + wpo

    cx, top, lgap = W // 2, 250, 22
    bw, pady = max(w1, w2), 46
    d.rounded_rectangle([cx - bw // 2 - padx, top - pady, cx + bw // 2 + padx,
                         top + h1 + lgap + h2 + pady], radius=44, fill=panel)
    x1 = cx - w1 // 2
    d.text((x1 + 3, top + 4), l1, font=f1, fill=SHADOW); d.text((x1, top), l1, font=f1, fill=text_col)
    y2 = top + h1 + lgap; x2 = cx - w2 // 2
    d.text((x2 + 3, y2 + 4), pre, font=f1, fill=SHADOW); d.text((x2, y2), pre, font=f1, fill=text_col)
    d.text((x2 + wp + 3, y2 + 4), acc, font=f1, fill=SHADOW); d.text((x2 + wp, y2), acc, font=f1, fill=accent)
    d.text((x2 + wp + wa, y2), post, font=f1, fill=text_col)
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    img.save(out); print(f"wrote {out} (font size {fs})")
    return pathlib.Path(out)


def make_thumb(frame, hook, out):
    base = Image.open(frame).convert("RGBA")
    ov = Image.open(hook).convert("RGBA")
    if ov.size != base.size: ov = ov.resize(base.size)
    base = Image.alpha_composite(base, ov)
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out, quality=92); print(f"wrote {out}")
    return pathlib.Path(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("hook"); h.add_argument("--l1", required=True); h.add_argument("--l2", required=True)
    h.add_argument("-o", required=True); h.add_argument("--brand", default=None)
    t = sub.add_parser("thumb"); t.add_argument("--frame", required=True); t.add_argument("--hook", required=True)
    t.add_argument("-o", required=True)
    a = ap.parse_args()
    if a.cmd == "hook": make_hook(a.l1, a.l2, a.o, B.load(a.brand))
    elif a.cmd == "thumb": make_thumb(a.frame, a.hook, a.o)
