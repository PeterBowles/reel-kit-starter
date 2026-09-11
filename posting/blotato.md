# Posting with Blotato

Blotato is a hosted service that gives you one API for posting to Instagram,
TikTok, YouTube, Facebook, and LinkedIn. Its main advantage over building this
yourself is that it already has developer apps approved with each platform, so you
skip the app-review process entirely.

## Cost

See blotato.com/pricing for current plans, don't assume a number here, they change
their pricing over time.

## Setup (about 10 minutes, verified against Blotato's help docs, Sept 2026)

Blotato's API and MCP need a paid Blotato plan. Check blotato.com/pricing.

1. Create a Blotato account at blotato.com.
2. In Blotato's own website (my.blotato.com, Settings), connect every social account
   you want to post to: Instagram, TikTok, YouTube, Facebook, LinkedIn. Claude
   cannot do this step for you, it involves logging in to each platform.
3. Connect Blotato to Claude. Blotato runs a hosted MCP server at
   `https://mcp.blotato.com/mcp`, nothing to install:
   - **Claude Desktop:** Settings → Connectors → Add custom connector → name it
     `Blotato`, URL `https://mcp.blotato.com/mcp` → Connect → approve the login
     in your browser (be logged in to Blotato there first).
   - **Claude Code (terminal):** in Blotato, Settings → API → "Claude Code" has a
     "Copy Setup Command" button. It gives you a one-liner of the form
     `claude mcp add blotato --url https://mcp.blotato.com/mcp --header "blotato-api-key: YOUR_KEY"`.
     Run it inside a Claude Code session. Keep any trailing `=` characters in the
     key, dropping them causes a silent 401.
   Official steps: help.blotato.com/api/mcp/setup and help.blotato.com/api/claude-code
4. Test it: ask Claude `list my Blotato accounts`. You should see the accounts you
   connected in step 2. If the connector says "Connected" but tool calls fail with an
   auth error, redo step 3 using the API-key form instead of the browser login
   (help.blotato.com/api/mcp/faqs).

Optional: Blotato publishes free Claude Code skills for writing and scheduling posts
(`/plugin marketplace add Blotato-Inc/blotato-skills`). Not needed for this kit,
the posting flow below is enough, but their `post-writer` and `post-grader` are
decent if you want help with caption copy.

## The posting flow

Once Blotato is connected, posting a finished video looks like this (tool names as
Blotato exposes them):

1. `blotato_list_accounts` to get the account id for each platform.
2. `blotato_create_presigned_upload_url` for `FINAL.mp4` (and `COVER.jpg` if you
   want an Instagram cover).
3. Upload each local file to its presigned URL with a plain HTTP PUT (Claude does
   this with curl; no cloud-storage detour needed).
4. `blotato_create_post` once per platform, using the returned media URL, that
   platform's own caption text from `export/captions.md`, and (if scheduling ahead)
   a `scheduledTime` in UTC.
5. `blotato_get_post_status` to confirm each one went through.

Nothing gets posted until you say so. Claude should show you the exact caption,
platforms, and time, and wait for a yes.

Never post an account ID or API key into a document, a commit, or a chat log.

## Platform gotchas (learned the hard way, still true as of this writing)

- **Instagram:** a post is rejected outright if it has more than 5 hashtags.
- **Instagram Reel cover:** a custom cover image is supported, but only at
  creation time. You cannot swap the cover of an already-published reel through
  the API. The cover image must be exactly 1080x1350 (4:5), not the 1080x1920 (9:16)
  video itself, an aspect-ratio mismatch here is a common cause of a cryptic post
  failure.
- **TikTok:** there is no way to set a custom image cover through the API, only a
  frame chosen by timestamp. If you want a designed cover image on TikTok, you have
  to set it manually inside the TikTok app after the video is up.
- **YouTube:** custom thumbnails require the channel to be phone-verified
  (youtube.com/verify) before Blotato can set one. If a channel was verified after
  you first connected it, reconnect it in Blotato to pick up the new status.
- **Facebook:** a video longer than 90 seconds cannot be posted as a Reel, post it
  as a normal video instead (don't set a reel media type).
- Always convert your intended posting time to UTC for `scheduledTime`, Blotato
  does not do that conversion for you.
