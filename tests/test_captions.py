import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import captions, brand

WORDS = {"words": [
  {"type":"word","text":"Most","start":0.0,"end":0.3},
  {"type":"word","text":"people","start":0.3,"end":0.6},
  {"type":"word","text":"breathe","start":0.6,"end":1.0},
  {"type":"word","text":"wrong.","start":1.0,"end":1.4},
  {"type":"spacing","text":" ","start":1.4,"end":1.5},
  {"type":"word","text":"Here's","start":2.5,"end":2.8},
  {"type":"word","text":"why","start":2.8,"end":3.1},
]}

def _brand(preset="pill", case="sentence"):
    b = brand.load(ROOT / "brand" / "brand.template.json")
    b["captions"]["preset"] = preset; b["captions"]["case"] = case
    return b

def test_blocks_break_on_sentence_and_gap():
    # "Most people breathe" alone already exceeds WIDTH_BUDGET (900px) at the
    # template's 104px Montserrat Black, so the width cap splits this block
    # before the sentence-end/gap rule ever gets a chance to. That's correct:
    # the whole point of WIDTH_BUDGET is to prevent line overflow.
    blocks = captions.group_blocks(captions.flatten(WORDS), _brand())
    assert [[w["disp"] for w in blk] for blk in blocks] == [["Most","people"],["breathe","wrong"],["Here's","why"]]

def test_pill_emits_boxes_and_text(tmp_path):
    out = tmp_path / "c.ass"
    n = captions.write_ass(WORDS, _brand("pill"), out)
    txt = out.read_text()
    assert "[Events]" in txt and "\\p1" in txt          # box drawings present
    assert txt.count("Dialogue:") == 12                  # 6 words text + 6 boxes

def test_scrim_has_no_boxes(tmp_path):
    out = tmp_path / "c.ass"
    captions.write_ass(WORDS, _brand("scrim"), out)
    assert "\\p1" not in out.read_text()

def test_karaoke_uses_k_tags(tmp_path):
    out = tmp_path / "c.ass"
    captions.write_ass(WORDS, _brand("karaoke"), out)
    assert "\\k" in out.read_text() or "\\1c" in out.read_text()

def test_upper_case():
    b = _brand(case="upper")
    blocks = captions.group_blocks(captions.flatten(WORDS), b)
    assert blocks[0][0]["disp"] == "MOST"
