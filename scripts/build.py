"""Build a vertical reel from edl.json + brand/brand.json.

  python scripts/build.py videos/<slug>            # pass 1: cut, NO captions -> work/CUT_nocaptions.mp4
  python scripts/build.py videos/<slug> --captions # pass 2: composite work/captions.ass -> export/FINAL.mp4
  --fast  quick preview encode

EDL format (videos/<slug>/edl.json):
  { "sources": {"take1": "raw/take1.mp4"},
    "ranges": [ {"source":"take1","start":2.4,"end":9.1,"beat":"hook"} ],
    "crop_x": null }
`crop_x` is optional: set an integer to override the detected face crop for every source.

Rules honoured: per-segment extract then -c copy concat; 30 ms audio fades at every cut;
captions composited LAST; loudnorm; -movflags +faststart on deliverables.
"""
import argparse, json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import brand as B, reframe as RF

def run(cmd): subprocess.run(cmd, check=True)

def _dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of",
        "default=noprint_wrappers=1:nokey=1",str(p)],capture_output=True,text=True).stdout.strip() or 0)

def build_cut(proj, b, fast=False):
    proj = pathlib.Path(proj); edl = json.loads((proj/"edl.json").read_text(encoding="utf-8"))
    o = b["output"]; rf = b["reframe"]; grade = b["grade"]["filter"]
    preset = "veryfast" if fast else "medium"
    segdir = proj/"work"/"segs"; segdir.mkdir(parents=True, exist_ok=True)
    sources = edl["sources"]; crop = {}
    for sid, rel in sources.items():
        full = proj/rel; land, w, h = RF.is_landscape(str(full))
        if not land: crop[sid] = None; print(f"  {sid}: portrait source, no reframe"); continue
        d = _dur(full)
        cx, why = RF.crop_x_for_segment(str(full), d*0.05, d*0.95, crop_w=rf["crop_w"], frame_w=w, fallback=rf["fallback_x"])
        crop[sid] = cx; print(f"  {sid}: crop_x={cx} ({why}), held for the whole take")
    if edl.get("crop_x") is not None: crop = {k: int(edl["crop_x"]) for k in sources}
    concat = segdir/"concat.txt"
    with open(concat, "w") as cf:
        for i, r in enumerate(edl["ranges"]):
            src = proj/sources[r["source"]]; a, e = float(r["start"]), float(r["end"]); dur = round(e-a, 3)
            af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={round(dur-0.03,3)}:d=0.03"
            out = segdir/f"{i:02d}_{r.get('beat','seg')}.mp4"
            cx = crop[r["source"]]
            vf = RF.reframe_filter(cx, rf["crop_w"], 1080) if cx is not None else f"scale={o['width']}:{o['height']}"
            if grade: vf += "," + grade
            vf += f",fps={o['fps']}"
            run(["ffmpeg","-y","-v","error","-ss",f"{a:.3f}","-to",f"{e:.3f}","-i",str(src),"-vf",vf,"-af",af,
                 "-c:v","libx264","-preset",preset,"-crf",str(o["crf"]),"-pix_fmt","yuv420p",
                 "-c:a","aac","-b:a",o["audio_bitrate"],"-ar",str(o["sample_rate"]),"-r",str(o["fps"]),str(out)])
            cf.write(f"file '{out.name}'\n"); print(f"  [{i:02d}] {r.get('beat',''):10s} {a:.2f}-{e:.2f} ({dur}s)")
    base = proj/"work"/"cut_base.mp4"
    run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(base)])
    out = proj/"work"/"CUT_nocaptions.mp4"
    run(["ffmpeg","-y","-v","error","-i",str(base),"-af",
         f"loudnorm=I={o['loudness_I']}:TP={o['loudness_TP']}:LRA={o['loudness_LRA']}",
         "-c:v","copy","-c:a","aac","-b:a",o["audio_bitrate"],"-ar",str(o["sample_rate"]),"-movflags","+faststart",str(out)])
    print(f"== cut done: {out} =="); return out

def build_final(proj, b, fast=False):
    proj = pathlib.Path(proj); o = b["output"]; preset = "veryfast" if fast else "medium"
    cut = proj/"work"/"CUT_nocaptions.mp4"; ass = proj/"work"/"captions.ass"
    if not cut.exists(): sys.exit("run pass 1 first (no work/CUT_nocaptions.mp4)")
    if not ass.exists(): sys.exit("no work/captions.ass — run scripts/captions.py first")
    (proj/"export").mkdir(exist_ok=True); final = proj/"export"/"FINAL.mp4"
    # ffmpeg's subtitles filter parses ':' as an option separator, so escape it in the path.
    fontsdir = str(B.ROOT/"fonts").replace("\\", "/").replace(":", "\\:")
    # Run from the project dir so the short relative paths below need no escaping.
    subprocess.run(["ffmpeg","-y","-v","error","-i","work/CUT_nocaptions.mp4","-vf",
         f"subtitles=work/captions.ass:fontsdir={fontsdir}","-c:v","libx264","-preset",preset,
         "-crf",str(o["crf"]),"-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart","export/FINAL.mp4"],
        check=True, cwd=str(proj))
    print(f"== final: {final} =="); return final

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--captions", action="store_true")
    ap.add_argument("--fast", action="store_true"); ap.add_argument("--brand", default=None); a = ap.parse_args()
    b = B.load(a.brand)
    (build_final if a.captions else build_cut)(a.project, b, fast=a.fast)
