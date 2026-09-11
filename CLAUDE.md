# CLAUDE.md

## What this folder is

`reel-kit-starter` is a brand-styled layer on top of the open source `video-use`
toolkit. It turns raw talking-head footage into a captioned, vertical reel in one
person's or company's own visual style, driven entirely through conversation with
Claude, no menus, no timeline editor.

## Where things are

- `brand/brand.json`, the single source of truth for colors, fonts, caption style,
  and hook-card style. Every script reads it. Copy it from
  `brand/brand.template.json` and fill it in once.
- `scripts/`, the tools: `brand.py` (loader), `captions.py`, `reframe.py`,
  `build.py`, `cards.py`, `contact_sheet.py`, `sample_render.py`, `new_video.py`.
- `skills/reel/SKILL.md`, the end-to-end workflow for turning footage into a
  finished reel. `skills/motion/SKILL.md`, the pattern for building an animated
  element (Remotion, Manim, or PIL).
- `videos/`, one folder per video (see the folder contract below), plus
  `videos/_inbox/` where new raw footage gets dropped before it has a project.
- `<VIDEO_USE>`, the video-use clone this toolkit depends on for transcription and
  the animation-engine skills. On this machine it lives at: `~/Developer/video-use`
  (Windows: `%USERPROFILE%\Developer\video-use`). If BOOTSTRAP.md set it up
  somewhere else, that path replaces this line.

## Rules

- **Two-pass edit.** Always build the full cut with NO captions first, show it plus
  a contact sheet, wait for approval, only then add captions. A caption tweak should
  never force a full re-render of the cut.
- **`brand/brand.json` is the only source of style.** Never ask the user to
  re-describe captions, colors, or fonts once it's set.
- **Cold-viewer hook gate.** If the first line of a script or the hook card text
  would not make sense to a stranger scrolling past with no context, flag it before
  building anything around it.
- **The folder contract is mandatory.** The `reel` skill writes nowhere outside a
  project's own `raw/`, `work/`, `export/`, `notes.md`. Never write into
  `videos/_inbox` once a project exists, and never write outside `videos/<slug>/`.
- **Verify motion with a contact sheet**, never by trusting a single first or last
  frame, or by trusting a timestamp without looking.
- **Export settings are fixed:** 30 fps, 1080x1920, -14 LUFS loudness. If a cut needs
  to run slower or faster, retime by dropping or duplicating frames, never by
  stretching with `setpts` or changing fps, that introduces audio drift and judder.
- **Platform gotchas** (see `posting/blotato.md` for the full list): Instagram caps
  at 5 hashtags per post; an Instagram Reel cover image must be exactly 1080x1350
  and can only be set at creation time; TikTok has no API for a custom image cover
  (only a frame by timestamp); a video over 90 seconds cannot be posted as a
  Facebook Reel; YouTube custom thumbnails require a phone-verified channel.
- **No `[ ]` or other shell-special characters in file paths.** ffmpeg's subtitles
  filter (and some of its other filters) breaks on brackets in a path.
- **Never commit `.env`** or any file containing a real API key. `.gitignore`
  already excludes it, don't override that.
- **Never write inside the video-use clone itself.** All session outputs belong in
  this repo's `videos/<slug>/` folders, video-use is a dependency, not a workspace.

## Skills

Read `skills/reel/SKILL.md` before editing any footage into a reel. Read
`skills/motion/SKILL.md` before building any animated element (text card, counter,
diagram, logo sting).
