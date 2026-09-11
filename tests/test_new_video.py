import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import new_video

def test_creates_contract_and_moves_clip(tmp_path):
    inbox = tmp_path/"videos"/"_inbox"; inbox.mkdir(parents=True)
    (inbox/"IMG_0001.MOV").write_bytes(b"x")
    proj = new_video.create(tmp_path/"videos", "breathing-tip", date="2026-09-11")
    assert proj == tmp_path/"videos"/"2026-09-11-breathing-tip"
    assert (proj/"raw"/"IMG_0001.MOV").exists() and not (inbox/"IMG_0001.MOV").exists()
    assert (proj/"work").is_dir() and (proj/"export").is_dir()
    assert "status: new" in (proj/"notes.md").read_text()

def test_slug_is_normalised(tmp_path):
    (tmp_path/"videos"/"_inbox").mkdir(parents=True)
    proj = new_video.create(tmp_path/"videos", "My Big Idea!!", date="2026-09-11")
    assert proj.name == "2026-09-11-my-big-idea"
