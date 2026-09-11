import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sample_render, brand

def test_sample_renders_5s_vertical(tmp_path):
    b = brand.load(ROOT/"brand"/"brand.template.json")
    out = sample_render.render(b, tmp_path)
    assert out.exists()
    d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of",
        "default=noprint_wrappers=1:nokey=1",str(out)],capture_output=True,text=True).stdout.strip()
    assert abs(float(d) - 5.0) < 0.3
