# Posting with Blotato

Blotato is a hosted service that gives you one API for posting to Instagram,
TikTok, YouTube, Facebook, and LinkedIn. Its main advantage over building this
yourself is that it already has developer apps approved with each platform, so you
skip the app-review process entirely.

## Cost

See blotato.com/pricing for current plans, don't assume a number here, they change
their pricing over time.

## Setup

1. Create a Blotato account.
2. In their dashboard, connect the social accounts you want to post to (Instagram,
   TikTok, YouTube, Facebook, LinkedIn). This step happens in their UI, not here.
3. Generate an API key from your Blotato account settings.
4. Add the Blotato MCP server to Claude Desktop following Blotato's own connection
   docs (search "Blotato MCP" or check their developer docs page, the exact steps
   change as they update their integration).

## The posting flow

Once the MCP server is connected, posting a finished video looks like this:

1. Create a presigned upload URL through the Blotato MCP tool for creating an
   upload URL.
2. Upload your local `export/FINAL.mp4` to that presigned URL directly (a plain PUT
   request works, no intermediate cloud storage needed).
3. Create a post per platform using the returned media URL, with that platform's
   own caption text and (if scheduling ahead) its own `scheduledTime`.

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
