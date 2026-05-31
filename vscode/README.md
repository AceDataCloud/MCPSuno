# Suno MCP

AI music generation with Suno — songs, lyrics, covers, stems, and more.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-suno?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-suno) [![PyPI](https://img.shields.io/pypi/v/mcp-suno.svg?label=PyPI)](https://pypi.org/project/mcp-suno/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://suno.mcp.acedata.cloud/mcp)

Connect VS Code's AI agents to Suno through Ace Data Cloud. Generate songs from text prompts, write custom lyrics with full musical control, extend tracks, remix or cover, separate stems, export MP4/WAV/MIDI — all from chat.

This extension registers the **suno** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `suno` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a music task — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://suno.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Generate a lofi hip-hop track about late-night coding. Use suno."
- "Write lyrics for a punk song about deadline pressure, then turn them into a song."
- "Cover the song with task id <id> in a jazz piano style."

---

## Tool Reference

**27 tools** available via this server.

| Tool | Description |
| --- | --- |
| `suno_generate_music` | Generate AI music from a text prompt using Suno's Inspiration Mode. |
| `suno_generate_custom_music` | Generate AI music with full control over lyrics, title, and style (Custom Mode). |
| `suno_extend_music` | Extend an existing song from a specific timestamp with new lyrics. |
| `suno_cover_music` | Create a cover or remix version of an existing song in a different style. |
| `suno_concat_music` | Concatenate extended song segments into a single complete audio file. |
| `suno_generate_with_persona` | Generate music using a saved artist persona for consistent vocal style. |
| `suno_remaster_music` | Remaster an existing song to improve audio quality. |
| `suno_stems_music` | Separate a song into individual stems (vocals and instruments). |
| `suno_replace_section` | Replace a specific time range in a song with new generated content. |
| `suno_upload_extend` | Extend an uploaded audio (your own music) with new AI-generated content. |
| `suno_upload_cover` | Create an AI cover of an uploaded audio (your own music). |
| `suno_mashup_music` | Create a musical mashup by blending multiple songs together. |
| `suno_generate_lyrics` | Generate song lyrics from a text prompt. |
| `suno_get_mp4` | Get an MP4 video version of a generated song. |
| `suno_get_timing` | Get timing and subtitle data for a generated song. |
| `suno_extract_vocals` | Extract the vocal track from a generated song (stem separation). |
| `suno_get_wav` | Get the lossless WAV format of a generated song. |
| `suno_get_midi` | Get MIDI data extracted from a generated song. |
| `suno_create_persona` | Create a new artist persona from an existing audio's vocal style. |
| `suno_optimize_style` | Optimize a music style description for better generation results. |
| `suno_mashup_lyrics` | Generate mashup lyrics by combining two sets of lyrics. |
| `suno_upload_audio` | Upload an external audio file to Suno for use in subsequent operations. |
| `suno_get_task` | Query the status and result of a music generation task. |
| `suno_get_tasks_batch` | Query multiple music generation tasks at once. |
| `suno_list_models` | List all available Suno models and their capabilities. |
| `suno_list_actions` | List all available Suno API actions and corresponding tools. |
| `suno_get_lyric_format_guide` | Get guidance on formatting lyrics for Suno music generation. |

## Supported Models

`v3.5`, `v4`, `v4.5`, `v5`

## Pricing

From $0.05 per song. New users get free trial credit at sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "suno": {
      "type": "http",
      "url": "https://suno.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API token",
      "password": true
    }
  ]
}
```

VS Code will prompt for the token on first use and persist it in the OS
secret store (Keychain / Credential Manager / libsecret).

### Alternative: local stdio (no network roundtrip)

If you prefer running the server locally — for offline dev, air-gapped
environments, or to pin to a specific PyPI version — install
[`uv`](https://docs.astral.sh/uv/) and replace your `mcp.json` entry with:

```jsonc
{
  "servers": {
    "suno": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-suno"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-suno`](https://pypi.org/project/mcp-suno/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://suno.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-suno`](https://pypi.org/project/mcp-suno/)
- **Source repository:** https://github.com/AceDataCloud/SunoMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
