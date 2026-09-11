# Posting with Postiz

Postiz is an open source (AGPL licensed), self-hostable alternative to Blotato. It
has an official MCP server, so it can also be driven from Claude Desktop. The
tradeoff is that you're responsible for your own developer apps with each platform.

## Setup

Two ways to run it:

- **Self-host with Docker:**
  ```
  docker run -d --name postiz -p 5000:5000 ghcr.io/gitroomhq/postiz-app
  ```
  (check the Postiz repo's README for current environment variables and any
  database setup it now expects, that detail changes across releases).
- **Their hosted cloud** version, if you'd rather not run Docker yourself.

To connect it to Claude Desktop, add the official MCP server, either with the CLI:

```
claude mcp add postiz --transport http --url https://api.postiz.com/mcp/<your-key>
```

or as a custom connector inside Claude Desktop's settings, using the same URL and
key. Check Postiz's own MCP docs for the current setup flow before assuming this
command still matches exactly.

## The honest caveat

Self-hosting means YOU create your own developer apps with Meta, TikTok, and Google,
and go through each platform's app review process to get posting permission. That
review can take time and isn't guaranteed to pass on the first try.

As of this writing, TikTok's auto-publish API is failing review for self-hosters
(see github.com/gitroomhq/postiz-app/issues/1563 for the current status). Until
that's resolved, treat TikTok as: Postiz saves your video as a draft to your phone,
and you tap to finish publishing it yourself in the TikTok app.

## Recommendation

Start on Blotato unless you enjoy app reviews.
