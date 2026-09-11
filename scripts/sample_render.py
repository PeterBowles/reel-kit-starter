"""Render a 5-second sample so you can SEE your caption style before any real footage.

Usage: python scripts/sample_render.py [-o work/brand_sample.mp4] [--brand brand/brand.json]

Background = your brand background colour; a faux "talking" transcript drives the captions,
so changing brand.json and re-running shows exactly what real captions will look like.
"""
import argparse, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import brand as B, captions

_LINE = "This is how your captions will look. The spoken word gets highlighted. Change anything in brand.json"
FAKE = {"words": [
    {"type": "word", "text": w, "start": 0.4 + i * 0.42, "end": 0.4 + i * 0.42 + 0.36}
    for i, w in enumerate(_LINE.split())]}


def render(b, outdir):
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    ass = outdir / "sample.ass"; captions.write_ass(FAKE, b, ass)
    bg = b["palette"]["background"].lstrip("#"); out = outdir / "brand_sample.mp4"
    fontsdir = str(B.ROOT / "fonts").replace("\\", "/").replace(":", "\\:")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    f"color=c=0x{bg}:size=1080x1920:rate=30", "-t", "5",
                    "-vf", f"subtitles={ass.name}:fontsdir={fontsdir}", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", out.name], check=True, cwd=str(outdir))
    print(f"wrote {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", default="work/brand_sample.mp4"); ap.add_argument("--brand", default=None)
    a = ap.parse_args(); b = B.load(a.brand); out = pathlib.Path(a.o)
    r = render(b, out.parent)
    if r != out: r.rename(out); print(f"moved to {out}")
