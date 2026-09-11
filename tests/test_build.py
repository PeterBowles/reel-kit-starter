import json, subprocess, sys, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build, brand

def _probe(p, key):
    return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",f"stream={key}",
        "-of","default=noprint_wrappers=1:nokey=1",str(p)],capture_output=True,text=True).stdout.strip()

def test_cut_and_caption_pass(tmp_path):
    proj = tmp_path / "2026-01-01-test"; (proj / "raw").mkdir(parents=True)
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","testsrc=size=1920x1080:rate=30",
        "-f","lavfi","-i","sine=frequency=440:sample_rate=48000","-t","4","-shortest",str(proj/"raw"/"t.mp4")],check=True)
    (proj/"edl.json").write_text(json.dumps({"sources":{"t":"raw/t.mp4"},
        "ranges":[{"source":"t","start":0.5,"end":2.0,"beat":"a"},{"source":"t","start":2.5,"end":3.5,"beat":"b"}]}))
    b = brand.load(ROOT/"brand"/"brand.template.json")
    cut = build.build_cut(proj, b, fast=True)
    assert cut.exists() and _probe(cut,"width") == "1080" and _probe(cut,"height") == "1920"
    (proj/"work"/"captions.ass").write_text("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Montserrat Black,100,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,0,0,2,60,60,60,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\nDialogue: 0,0:00:00.00,0:00:02.00,Default,,0,0,0,,hello\n")
    final = build.build_final(proj, b, fast=True)
    assert final == proj/"export"/"FINAL.mp4" and final.exists()
    assert abs(float(_probe(final,"duration") or 2.5) - 2.5) < 0.2
