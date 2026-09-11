"""Load and validate brand/brand.json. Every other script imports this."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
PRESETS = ("pill", "scrim", "karaoke")
CASES = ("sentence", "upper", "natural")

def hex_to_ass(h):
    h = h.lstrip("#"); return f"{h[4:6]}{h[2:4]}{h[0:2]}".upper()

def hex_to_rgba(h, a=255):
    h = h.lstrip("#"); return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), a)

def load(path=None):
    path = pathlib.Path(path) if path else ROOT / "brand" / "brand.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing. Copy brand/brand.template.json to brand/brand.json.")
    b = json.loads(path.read_text(encoding="utf-8"))
    c = b["captions"]
    if c["preset"] not in PRESETS: raise ValueError(f"captions.preset must be one of {PRESETS}")
    if c["case"] not in CASES: raise ValueError(f"captions.case must be one of {CASES}")
    for k in ("display_ttf", "body_ttf"):
        f = ROOT / b["font"][k]
        if not f.exists(): raise FileNotFoundError(f"font.{k} not found: {f}")
    b["_font_display"] = ROOT / b["font"]["display_ttf"]
    b["_font_body"] = ROOT / b["font"]["body_ttf"]
    return b
