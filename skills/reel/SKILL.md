---
name: reel
description: Use when the user says "make a reel", "start a new video", "edit this clip", "cut my footage", or drops footage in videos/_inbox.
---

# reel

Turn raw footage into a captioned, brand-styled vertical reel.

## Ground rules

- `brand/brand.json` is the only source of style. Never ask the user to re-describe
  captions, colors, or fonts, it is already decided there.
- The folder contract is fixed: run `python scripts/new_video.py <slug>` first, then
  write ONLY inside that project folder (`raw/`, `work/`, `export/`, `notes.md`).
  Never write into `videos/_inbox` or outside the project.
- Two passes, always: build the cut WITHOUT captions, show the contact sheet and the
  mp4, wait for approval, then add captions. This way a caption tweak never forces a
  full re-render of the cut.
- Verify by looking at real frames (`contact_sheet.py`), never by trusting timestamps
  or assuming the render worked.
- Every deliverable ends up with `-movflags +faststart` baked in (already handled by
  `build.py`), so it plays instantly on a phone instead of buffering.

## Pipeline

1. **Start the project.** Two ways in, both end in the same folder:
   - **Footage first.** Files are already in `videos/_inbox/` and the user says
     "make a reel". If they didn't name it, ask for a 2 to 4 word name, then run
     `python scripts/new_video.py <slug>` from the repo root. That moves everything
     out of `_inbox` into `videos/<date>-<slug>/raw/` and creates `work/`, `export/`,
     `notes.md`.
   - **Folder first.** The user says "start a new video" or "new project" with nothing
     in `_inbox`. Ask what to call it, run the same `new_video.py <slug>` (it creates
     the empty project), then tell them the exact path to drop footage into:
     `videos/<date>-<slug>/raw/`. Stop there and wait until they say the footage is in.
   Then `ffprobe` each file in `raw/`. If `raw/` is empty, say so and wait; never
   go looking for footage elsewhere.
2. **Transcribe each source** with the video-use toolkit (cloned separately, see
   `CLAUDE.md` for where `<VIDEO_USE>` points on this machine):
   ```
   python <VIDEO_USE>/helpers/transcribe.py raw/<file> --edit-dir work
   python <VIDEO_USE>/helpers/pack_transcripts.py --edit-dir work
   ```
   Read `work/takes_packed.md`, it is the phrase-level view you reason from.
3. **Propose the cut** in plain English: which takes, what's being dropped, target
   length. Wait for the user to say OK before writing anything.
4. **Write `edl.json`** in the project folder (format documented in `HOW-TO-USE.md`).
   Cut on word boundaries, pad 30 to 200 ms on each edge, use clean takes only.
5. **Build the cut, no captions yet:**
   ```
   python scripts/build.py videos/<slug> --fast
   ```
   That produces `videos/<slug>/work/CUT_nocaptions.mp4`. Then:
   ```
   python scripts/contact_sheet.py videos/<slug>/work/CUT_nocaptions.mp4 -o videos/<slug>/work/sheet_cut.jpg
   ```
   Look at the sheet. Show the user the mp4 and the sheet. WAIT for approval before
   moving on.
6. **After approval, add captions.** Transcribe the cut itself, not the raw source,
   so any b-roll or cutaway audio in the final timeline is covered too:
   ```
   python <VIDEO_USE>/helpers/transcribe.py videos/<slug>/work/CUT_nocaptions.mp4 --edit-dir videos/<slug>/work
   python scripts/captions.py videos/<slug>/work/transcripts/CUT_nocaptions.json -o videos/<slug>/work/captions.ass
   python scripts/build.py videos/<slug> --captions
   ```
   That last command reads `work/captions.ass` and produces `videos/<slug>/export/FINAL.mp4`.
   Run the contact sheet again on the final export and check: captions sit above the
   bottom UI zone (`pos_y` in `brand.json`, don't go lower than 1530), and the
   highlighted word tracks the audio correctly.
7. **Thumbnail.** Grab the last clean frame of the cut:
   ```
   ffmpeg -sseof -1 -i videos/<slug>/work/CUT_nocaptions.mp4 -frames:v 1 videos/<slug>/work/last.png
   ```
   Optionally overlay a hook card (`scripts/cards.py hook ...` then
   `scripts/cards.py thumb --frame ... --hook ... -o videos/<slug>/export/THUMBNAIL.jpg`).
   If posting to Instagram, its cover image MUST be 4:5, not 9:16:
   ```
   ffmpeg -i videos/<slug>/export/THUMBNAIL.jpg -vf "crop=1080:1350:0:120,setsar=1" videos/<slug>/export/COVER.jpg
   ```
8. **Per-platform captions.** Write `videos/<slug>/export/captions.md`: Instagram
   (hook first, 5 hashtags max), TikTok (short, 3 to 4 lowercase tags), YouTube (a
   real title plus a longer searchable description), Facebook (no hashtags), LinkedIn
   (professional tone). Paste them into chat too.
9. **Update `notes.md`** status field as you go: `new` -> `cut` -> `approved` ->
   `captioned` -> `exported`. Posting is a separate step, see `posting/`.

## Verify before saying it's done

- `ffprobe` on `export/FINAL.mp4` reports 1080x1920 at 30 fps.
- The contact sheet has actually been viewed, not assumed.
- `export/COVER.jpg`, if made, is exactly 1080x1350.
- `notes.md` reflects the current status.
