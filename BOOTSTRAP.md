# BOOTSTRAP

Paste everything below the line into Claude Desktop's Code tab with an EMPTY folder open.

---

You are setting up the reel-kit-starter video toolkit on this machine. Do every step yourself, ask me only for things you cannot generate (API keys, confirmation before installing software). Explain each step in one plain sentence before running it.

1. Detect my OS. Check for git, ffmpeg, ffprobe, python3 (>=3.10), node (>=22). Install missing ones with brew (macOS) / winget (Windows) / apt (Linux), asking me first. On Windows also confirm Git for Windows is installed.
2. In the current folder run: git clone https://github.com/<OWNER>/reel-kit-starter . (this folder must be empty). Then clone https://github.com/browser-use/video-use into ~/Developer/video-use (skip if present). Record the video-use path in CLAUDE.md where it says <VIDEO_USE>.
3. Create a Python venv at .venv, install requirements.txt, and pip install -e ~/Developer/video-use. Use .venv/bin/python -m pip on macOS/Linux and .venv\Scripts\python -m pip on Windows.
4. Ask me for my ElevenLabs API key (needed for transcription; elevenlabs.io -> Profile -> API keys). Write it as ELEVENLABS_API_KEY=... into ~/Developer/video-use/.env. Never print it back.
5. Brand interview, one question at a time: company name; primary colour, accent colour, background colour (hex, or describe and propose); logo file (optional, copy to brand/logo.png); caption style, show me the three presets from brand/README.md and ask which; text case (sentence/upper). Write brand/brand.json from brand/brand.template.json.
6. Run python scripts/sample_render.py and show me work/brand_sample.mp4 (open it). Ask if I want changes; loop until I say it's right.
7. Smoke test: ask me to record 10-15 seconds of myself talking on my phone and drop it in videos/_inbox/. Then follow skills/reel/SKILL.md end to end (slug "hello"), showing me the cut before captions.
8. Ask whether I want posting set up now (posting/blotato.md or posting/postiz.md) or later.
9. Finish by printing the "Daily use" section of HOW-TO-USE.md.
