# reel-kit-starter

Edit vertical reels by talking to Claude. Drop a clip in a folder, say "make a reel",
approve the cut, get a captioned, brand-styled video out the other end, no timeline
editor, no menus. It's a thin brand and workflow layer on top of the open source
`video-use` toolkit, which does the heavy lifting (transcription, cutting,
rendering).

## Quick start (3 steps)

1. Install Claude Desktop and sign in. On Windows, also install Git for Windows.
2. Create an empty folder on your machine and open it in Claude Desktop's Code tab.
3. Paste the contents of `BOOTSTRAP.md` into the chat. Claude installs everything,
   interviews you about your brand (colors, fonts, caption style), and walks you
   through making your first reel.

Everyday use after that is in `HOW-TO-USE.md`.

## What it costs

- A Claude subscription that includes the Code tab.
- An ElevenLabs account for transcription. They have a free tier; heavier use costs
  a small amount per minute transcribed.
- Posting is optional. Blotato (the default option, see `posting/blotato.md`) has
  its own paid plans. Postiz (self-hosted, see `posting/postiz.md`) is free but
  requires more setup.

## What it can't do

- Fix bad footage or bad audio. Garbage in, garbage out, this is an editor, not a
  restoration tool.
- Set a custom image cover on TikTok through the API, that has to be done by hand in
  the TikTok app.
- Anything magic. It follows the same pipeline a human editor would: transcribe,
  cut, reframe, caption, export.

## Tested on

- Linux: 2026-09-11.
- Windows: pending a dry run, this line gets updated after.
- macOS: best-effort, not yet verified end to end.

## Credits

Built on top of `browser-use/video-use` (github.com/browser-use/video-use), which
handles transcription and rendering. This repo adds a brand layer, a folder
contract, and the conversational skills on top of it.

## License

MIT, see `LICENSE`.
