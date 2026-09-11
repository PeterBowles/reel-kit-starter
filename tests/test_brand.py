import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import brand

def test_template_loads_and_validates(tmp_path):
    b = brand.load(ROOT / "brand" / "brand.template.json")
    assert b["captions"]["preset"] == "pill"
    assert b["_font_display"].exists()

def test_hex_to_ass():
    assert brand.hex_to_ass("#123456") == "563412"   # ASS is BGR

def test_invalid_preset_rejected(tmp_path):
    p = tmp_path / "b.json"
    d = json.loads((ROOT / "brand" / "brand.template.json").read_text())
    d["captions"]["preset"] = "sparkle"
    p.write_text(json.dumps(d))
    try:
        brand.load(p); assert False, "should raise"
    except ValueError as e:
        assert "preset" in str(e)
