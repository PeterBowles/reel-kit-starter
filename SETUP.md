# SETUP

This is what `BOOTSTRAP.md` does, spelled out for a human who wants to run it by
hand, or check what Claude actually did. Steps match `BOOTSTRAP.md` 1 to 9.

## 1. Check prerequisites

You need `git`, `ffmpeg` (and the `ffprobe` that ships with it), Python 3.10 or
newer, and Node.js 22 or newer (Node is only needed later, for Remotion animation
slots).

```bash
git --version
ffmpeg -version
ffprobe -version
python3 --version
node --version
```

Install whatever's missing:

- **macOS:** `brew install git ffmpeg python node`
- **Windows:** `winget install Git.Git`, `winget install Gyan.FFmpeg`,
  `winget install Python.Python.3.12`, `winget install OpenJS.NodeJS`. Also confirm
  Git for Windows is installed (it usually comes with the `git` winget package).
- **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install -y git ffmpeg python3 python3-venv nodejs npm`

## 2. Clone the repos

```bash
git clone https://github.com/<OWNER>/reel-kit-starter .
```

(run this inside an empty folder). Then clone the video engine this toolkit depends
on, next to your other projects, not inside this repo:

```bash
git clone https://github.com/browser-use/video-use ~/Developer/video-use
```

On Windows, a natural equivalent path is `%USERPROFILE%\Developer\video-use`. Once
it's cloned, open `CLAUDE.md` in this repo and replace the `<VIDEO_USE>` placeholder
with the real path.

## 3. Python environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt      # Windows: .venv\Scripts\pip install -r requirements.txt
.venv/bin/pip install -e ~/Developer/video-use  # Windows: .venv\Scripts\pip install -e path\to\video-use
```

## 4. ElevenLabs API key

Transcription (turning your footage into word-level timestamps) runs on ElevenLabs
Scribe. Get a key at elevenlabs.io under Profile -> API keys, then write it to the
video-use clone's own `.env` file (not this repo's):

```bash
printf 'ELEVENLABS_API_KEY=your-key-here\n' > ~/Developer/video-use/.env
```

Never commit this file, and never paste the key into a chat log or a document.

## 5. Brand interview

Copy the template and fill it in:

```bash
cp brand/brand.template.json brand/brand.json
```

Edit `brand/brand.json` by hand, or have Claude walk you through it: your name or
company name, three hex colors (primary, accent, background), an optional logo file
copied to `brand/logo.png`, which caption preset you want (`pill`, `scrim`, or
`karaoke`, see `brand/README.md` for what each looks like), and whether captions
should be sentence case or upper case.

## 6. Preview your style

```bash
.venv/bin/python scripts/sample_render.py
```

Open `work/brand_sample.mp4` and look at it. Edit `brand/brand.json` and re-run
until it looks right, no real footage is needed for this step.

## 7. Smoke test with a real clip

Record 10 to 15 seconds of yourself talking on your phone and drop the file into
`videos/_inbox/`. Then follow `skills/reel/SKILL.md` end to end using `hello` as the
slug. You should end up with `videos/<date>-hello/export/FINAL.mp4`.

## 8. Posting (optional, can be done later)

Read `posting/blotato.md` (the easier hosted option) or `posting/postiz.md` (free,
self-hosted, more setup) and decide which one you want, if either, right now.

## 9. You're set up

From here on, daily use is the workflow in `HOW-TO-USE.md`: drop a clip in
`videos/_inbox/`, say "make a reel", approve the cut, get your export.
