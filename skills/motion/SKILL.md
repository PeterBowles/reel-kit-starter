---
name: motion
description: Use when the user wants an animated element, a kinetic text card, a counter, a diagram, a logo sting, or a full motion-graphics clip.
---

# motion

Build one animated element at a time as an isolated "slot", render it standalone,
verify it, then composite it into the reel.

## The slot pattern

Each animated element gets its own directory:

```
videos/<slug>/work/animations/slot_<id>/
```

Never build an animation inline in the main project folder, and never install
anything at the repo root, everything for one element lives and installs inside its
own slot. This keeps `node_modules` and engine-specific scaffolding out of git (the
`.gitignore` already excludes `node_modules/`) and lets you throw a slot away and
retry without touching anything else.

## Pick the engine per element, not globally

- **Remotion** (React + CSS compositions, good for anything with component state or
  a reusable system of text/graphics). Scaffold it inside the slot:
  ```
  cd videos/<slug>/work/animations/slot_<id>
  npx create-video@latest
  ```
  Render with:
  ```
  npx remotion render
  ```
  to `render.mp4`. The Code tab's preview pane can show `npx remotion studio` live
  while you iterate. Requires Node.js 22 or newer, installed only inside the slot.
- **Manim** (formal diagrams, equations, graph morphs). Read
  `<VIDEO_USE>/skills/manim-video/SKILL.md` for the setup and render commands, `<VIDEO_USE>`
  is the video-use clone, see `CLAUDE.md` for where it lives on this machine.
- **PIL + ffmpeg PNG sequence** (simple cards: counters, typewriter text, bar
  reveals). Fastest option when the element doesn't need a full animation engine,
  generate frames with Pillow, then `ffmpeg -framerate ... -i frame_%04d.png ...` to
  turn them into `render.mp4`.

Whichever engine you use, colors and fonts for the element come from
`brand/brand.json`, the same file every other script reads. Never hardcode a color or
font inside a slot.

## Verify before compositing

Before an animation slot's output goes anywhere near the main timeline:

```
python scripts/contact_sheet.py videos/<slug>/work/animations/slot_<id>/render.mp4 -o videos/<slug>/work/animations/slot_<id>/sheet.jpg
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 videos/<slug>/work/animations/slot_<id>/render.mp4
```

Look at the contact sheet. Check the duration matches what the timeline expects.

## Compositing into the reel

For a single element, a direct ffmpeg overlay is usually simplest:

```
ffmpeg -i base.mp4 -i videos/<slug>/work/animations/slot_<id>/render.mp4 -filter_complex \
  "[1:v]setpts=PTS-STARTPTS+T/TB[ov];[0:v][ov]overlay=enable='between(t,T,T+DUR)'" out.mp4
```

The `setpts=PTS-STARTPTS+T/TB` shift is required, without it the overlay starts
mid-animation instead of at frame 0 when it enters the timeline. For multiple
overlay elements composited at once, the video-use toolkit's `render.py` handles the
PTS-shifted overlay chain for you, see `<VIDEO_USE>/SKILL.md`.

Captions are always composited last, after every overlay, so an overlay never covers
burned-in text.
