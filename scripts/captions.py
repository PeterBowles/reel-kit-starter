"""transcript.json (word-level) -> captions.ass in the brand's caption style.
Usage: python scripts/captions.py <transcript.json> -o work/captions.ass [--brand brand/brand.json]
Presets: pill (spoken word in a filled rounded box), scrim (plain white on soft dark glow),
karaoke (spoken word recolors). One short centered line at a time, width-capped.
"""
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import brand as B
from PIL import ImageFont

WIDTH_BUDGET = 900; GAP = 0.6; K = 0.85; SP_K = 0.45
PADX = 10; PADY = 20; RAD = 14

def ass_time(t):
    t = max(0.0, t); cs = int(round(t * 100))
    h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"

def _case(txt, mode):
    if mode == "upper": return txt.upper()
    return txt  # sentence + natural keep the transcript's own casing

def flatten(tr):
    out = []
    for w in tr.get("words", []):
        if w.get("type") != "word": continue
        if w.get("start") is None or w.get("end") is None: continue
        txt = (w.get("text") or "").strip()
        if not txt or txt.endswith("-"): continue
        out.append({"start": float(w["start"]), "end": float(w["end"]), "raw": txt,
                    "disp": txt.rstrip(".!?").rstrip(",;:")})
    return out

def group_blocks(words, b):
    c = b["captions"]; font = ImageFont.truetype(str(b["_font_display"]), c["font_size"])
    maxw = c["max_words_per_line"]
    for w in words: w["disp"] = _case(w["disp"], c["case"])
    def line_w(toks): return sum(font.getlength(t) for t in toks) + font.getlength(" ") * (len(toks) - 1)
    blocks, cur = [], []
    for i, w in enumerate(words):
        trial = [x["disp"] for x in cur] + [w["disp"]]
        if cur and (len(cur) >= maxw or line_w(trial) > WIDTH_BUDGET):
            blocks.append(cur); cur = []
        cur.append(w)
        ends = w["raw"][-1] in ".!?"
        nxt = (words[i + 1]["start"] - w["end"]) if i + 1 < len(words) else 999
        if ends or nxt > GAP: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    return blocks

def _rrect(W, H, r):
    r = int(min(r, W / 2, H / 2))
    return (f"m {r} 0 l {W-r} 0 b {W} 0 {W} 0 {W} {r} l {W} {H-r} b {W} {H} {W} {H} "
            f"{W-r} {H} l {r} {H} b 0 {H} 0 {H} 0 {H-r} l 0 {r} b 0 0 0 0 {r} 0")

def write_ass(tr, b, out):
    c = b["captions"]; FS = c["font_size"]; POS_Y = c["pos_y"]; preset = c["preset"]
    font = ImageFont.truetype(str(b["_font_display"]), FS)
    hl = B.hex_to_ass(c["highlight_color"]); white = B.hex_to_ass(c["text_color"])
    blocks = group_blocks(flatten(tr), b)
    ink_bottom = POS_Y - 0.14 * FS; ink_top = ink_bottom - 0.74 * FS
    box_top = int(ink_top - PADY); box_h = int((ink_bottom + PADY) - box_top)
    text_ev, box_ev = [], []
    for bi, block in enumerate(blocks):
        toks = [w["disp"] for w in block]
        widths = [font.getlength(t) * K for t in toks]; sp = font.getlength(" ") * SP_K
        total = sum(widths) + sp * (len(toks) - 1); left = 540 - total / 2.0
        b_start = block[0]["start"]
        b_end = blocks[bi + 1][0]["start"] if bi + 1 < len(blocks) else block[-1]["end"] + 0.30
        cx = left
        for j, w in enumerate(block):
            wd = widths[j]; wcx = cx + wd / 2.0
            ws = w["start"]; we = block[j + 1]["start"] if j + 1 < len(block) else b_end
            base = f"\\an2\\pos({int(wcx)},{POS_Y})\\bord4\\blur5\\shad0\\3c&H000000&\\3a&H3C&"
            if preset == "karaoke":
                # word is white until spoken, highlight colour while/after spoken within the block
                text_ev.append((b_start, ws, f"{{{base}\\1c&H{white}&}}{w['disp']}", 1))
                text_ev.append((ws, b_end, f"{{{base}\\1c&H{hl}&}}{w['disp']}", 1))
            else:
                text_ev.append((b_start, b_end, f"{{{base}}}{w['disp']}", 1))
            if preset == "pill":
                x0 = int(wcx - wd / 2 - PADX); bw = int(wd + 2 * PADX)
                box_ev.append((ws, we, f"{{\\an7\\pos({x0},{box_top})\\1c&H{hl}&\\1a&H12&\\bord0\\shad0\\p1}}{_rrect(bw, box_h, RAD)}", 0))
            cx += wd + sp
    fontname = ImageFont.truetype(str(b["_font_display"]), 10).getname()[0]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{fontname},{FS},&H00{white},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,0,0,2,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    body = "".join(f"Dialogue: {lay},{ass_time(a)},{ass_time(e)},Default,,0,0,0,,{t}\n" for (a, e, t, lay) in box_ev + text_ev)
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(header + body, encoding="utf-8")
    print(f"wrote {out}: {len(blocks)} blocks, {len(text_ev)} text, {len(box_ev)} boxes")
    return len(blocks)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("transcript"); ap.add_argument("-o", required=True)
    ap.add_argument("--brand", default=None); a = ap.parse_args()
    write_ass(json.loads(pathlib.Path(a.transcript).read_text(encoding="utf-8")), B.load(a.brand), a.o)
