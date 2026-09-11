# How to use reel-kit-starter

## Daily use

1. Drop your clip (or clips) into `videos/_inbox/`, any filename.
2. Open this folder in Claude Desktop's Code tab.
3. Say: `make a reel from the clip in inbox, call it <slug>` (pick any short name
   for `<slug>`, for example `morning-routine`).
4. Claude runs `scripts/new_video.py`, transcribes your footage, proposes a cut, and
   builds it. It shows you the cut plus a contact sheet before adding captions, say
   "yes" or ask for changes.
5. Once you approve, Claude adds captions in your brand style and exports the final
   video.
6. Find everything in `videos/<date>-<slug>/export/`: `FINAL.mp4`, and if you asked
   for one, `THUMBNAIL.jpg` and `COVER.jpg`.
7. To post it, say `post it` (see `posting/blotato.md` or `posting/postiz.md` for
   what that actually does and what it costs).

## Changing your look

Your colors, fonts, and caption style all live in one file: `brand/brand.json`.
To see a change before touching real footage:

1. Edit `brand/brand.json`.
2. Run:
   ```
   python scripts/sample_render.py
   ```
3. Watch `work/brand_sample.mp4`, it shows your caption style burned onto a 5-second
   clip in your background color, no real footage needed.

Repeat until it looks right. Every real video you make afterward uses whatever is in
`brand/brand.json` at the time.

## The EDL format

`edl.json` is the file that tells `scripts/build.py` which parts of your raw footage
to keep, in what order. It lives at `videos/<slug>/edl.json`:

```json
{
  "sources": { "take1": "raw/take1.mp4" },
  "ranges": [
    { "source": "take1", "start": 2.4, "end": 9.1, "beat": "hook" }
  ],
  "crop_x": null
}
```

- `sources` maps a short name to a file path relative to the project folder.
- `ranges` is an ordered list of clips to keep. Each entry names its `source`, a
  `start` and `end` time in seconds, and an optional `beat` label (used only in
  logging, to help you tell segments apart).
- `crop_x` is optional. Leave it `null` to let `reframe.py` auto-detect a face and
  pick a crop, or set an integer to force the same horizontal crop position for
  every source.

Cut on word boundaries (never mid-word), and pad each edge by 30 to 200 ms so a fast
cut doesn't clip the start or end of a word.

## Folder contract

Every video gets exactly one folder, and nothing is written outside it:

```
videos/
  _inbox/                 drop raw footage here, any filename, before it has a project
  YYYY-MM-DD-slug/        one per video, created by scripts/new_video.py
    raw/                  original footage, moved out of _inbox
    work/                 transcripts, edl.json, captions.ass, contact sheets, test renders
    export/               FINAL.mp4, THUMBNAIL.jpg, COVER.jpg (4:5), captions.md
    notes.md              what was cut and why, and a status line: new | cut | approved | captioned | posted
brand/brand.json
```
