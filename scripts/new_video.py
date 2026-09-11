"""Create videos/YYYY-MM-DD-slug/ (raw/ work/ export/ notes.md) and move everything
from videos/_inbox into raw/.

Usage: python scripts/new_video.py <slug>   (from repo root)
"""
import datetime, pathlib, re, shutil, sys

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-"); return s or "video"

def create(videos_dir, slug, date=None):
    videos_dir = pathlib.Path(videos_dir); date = date or datetime.date.today().isoformat()
    proj = videos_dir/f"{date}-{slugify(slug)}"
    for d in ("raw", "work", "export"): (proj/d).mkdir(parents=True, exist_ok=True)
    inbox = videos_dir/"_inbox"; moved = []
    if inbox.exists():
        for f in sorted(inbox.iterdir()):
            if f.name.startswith(".") or f.name == ".gitkeep": continue
            shutil.move(str(f), str(proj/"raw"/f.name)); moved.append(f.name)
    notes = proj/"notes.md"
    if not notes.exists():
        notes.write_text(f"# {proj.name}\n\nstatus: new\n\n## Sources\n"
                         + "".join(f"- raw/{m}\n" for m in moved) + "\n## Decisions\n\n", encoding="utf-8")
    print(f"created {proj} ({len(moved)} file(s) moved from _inbox)"); return proj

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit("usage: new_video.py <slug>")
    create(pathlib.Path("videos"), sys.argv[1])
