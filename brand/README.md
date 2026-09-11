# brand/brand.json

This file is the ONLY place your visual style lives. Every script (captions,
cards, reframe, build) reads it. Copy `brand.template.json` to `brand.json`
and fill in your own values, `brand.json` is gitignored so your colors and
logo never get committed.

## Fields

- **name**, your company or creator name. Used in card/thumbnail text where
  relevant.
- **palette**, your four core colors, as `#RRGGBB` hex:
  - `primary`, your main brand color.
  - `accent`, a secondary pop color, used for hook cards.
  - `background`, the color behind cards and the sample render.
  - `text`, default text color.
- **font.display_ttf** / **font.body_ttf**, paths (relative to the repo
  root) to the two TTF files used for headlines/captions and body text. The
  starter ships Montserrat Black + Bold in `fonts/`, swap in your own font
  files if you have license to redistribute them, or point at a licensed
  font already installed on your machine.
- **logo**, path to a logo file (e.g. `brand/logo.png`) or `null` if you
  don't have one yet. Never AI-generate or recolor a logo, composite the
  real file.
- **captions**, controls the burned-in subtitles (see "Caption presets"
  below):
  - `preset`, `pill`, `scrim`, or `karaoke`.
  - `case`, `sentence` (keep the transcript's own casing), `upper`
    (ALL CAPS), or `natural` (same as sentence, reserved for future
    per-word casing rules).
  - `font_size`, pixel size of caption text on a 1080x1920 canvas.
  - `pos_y`, vertical baseline position, in pixels from the top. **Don't go
    lower than 1530**, Instagram and TikTok both draw their own UI
    (username, caption, action buttons) over the bottom of the frame, and
    anything lower gets covered.
  - `max_words_per_line`, how many words can share one caption block before
    it wraps to a new one.
  - `highlight_color`, the color used for the "spoken word" treatment
    (the pill fill in `pill`, or the recolor in `karaoke`). Unused in
    `scrim`.
  - `text_color`, the color of the caption text itself.
- **hook_card**, controls the opening hook-card graphic (`scripts/cards.py`):
  - `panel_color` / `panel_alpha`, the translucent panel behind the hook
    text (alpha is 0-255).
  - `accent_color`, color for the `{braced}` accent word in a hook line.
  - `text_color`, color for the rest of the hook text.
  - `case`, `sentence` or `upper`, same meaning as above.
- **reframe**, how landscape footage gets cropped to vertical:
  - `mode`, currently only `face-fixed` is implemented (detect a face,
    lock one crop-x for the whole take).
  - `crop_w`, width in source pixels of the vertical crop window.
  - `fallback_x`, crop-x to use when no face is detected.
- **grade.filter**, any ffmpeg video filter string (e.g. a color LUT or
  `eq=contrast=1.05`) applied to every cut segment. Leave `""` for no grade.
- **output**, final video encode settings: `width`/`height`/`fps`, `crf`
  (quality, lower = better/larger), `audio_bitrate`, `sample_rate`, and the
  three loudness-normalization targets (`loudness_I`/`loudness_TP`/
  `loudness_LRA`, the defaults match the loudness most platforms expect for
  spoken-word video).

## Caption presets

- **pill**, white caption text; the word currently being spoken sits inside
  a filled, rounded rectangle in `highlight_color`. Reads as an on-brand,
  designed caption style.
- **scrim**, plain white text over a soft dark glow (no box at all). The
  most neutral, minimal option.
- **karaoke**, no box; instead the spoken word itself changes color to
  `highlight_color` as it's said, like a lyric video.

Run `python scripts/sample_render.py` any time after editing `brand.json` to
render a 5-second preview clip (`work/brand_sample.mp4`) so you can see your
caption style before touching real footage.
