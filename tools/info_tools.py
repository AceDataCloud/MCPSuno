"""Informational tools for Suno API."""

from core.server import mcp


@mcp.tool()
async def list_models() -> str:
    """List available Suno models and their capabilities.

    Shows all available model versions with their limits and features.
    """
    return """Available Suno Models:

| Model           | Version | Prompt Limit | Style Limit | Max Duration |
|-----------------|---------|--------------|-------------|--------------|
| chirp-v5        | V5      | 5000 chars   | 1000 chars  | 8 minutes    |
| chirp-v4-5-plus | V4.5+   | 5000 chars   | 1000 chars  | 8 minutes    |
| chirp-v4-5      | V4.5    | 5000 chars   | 1000 chars  | 4 minutes    |
| chirp-v4        | V4      | 3000 chars   | 200 chars   | 150 seconds  |
| chirp-v3-5      | V3.5    | 3000 chars   | 200 chars   | 120 seconds  |
| chirp-v3        | V3      | 3000 chars   | 200 chars   | 120 seconds  |

Recommended: chirp-v4-5 or chirp-v5 for best quality.

Features by Version:
- V4.5+: Vocal gender control ('f' for female, 'm' for male)
- V5: Latest model with improved quality and 8-minute songs
"""


@mcp.tool()
async def list_actions() -> str:
    """List all available Suno API actions and their purposes.

    Reference for what each action does in the Suno API.
    """
    return """Available Suno Actions:

Music Generation:
- generate: Create new music from prompt or custom lyrics
- extend: Continue an existing song from a specific timestamp
- cover: Create a cover/remix version of a song
- concat: Merge extended song segments into complete audio

Upload-based Actions:
- upload_extend: Extend user-uploaded audio
- upload_cover: Create cover of uploaded audio

Persona Actions:
- artist_consistency: Generate with saved persona (voice style)
- artist_consistency_vox: Generate with Persona-v2-vox

Audio Processing:
- stems: Extract stems (vocals, instruments) from audio
- all_stems: Extract all available stems
- remaster: Improve audio quality
- replace_section: Replace a specific section of audio

Tools Available:
- generate_music: Simple prompt-based generation
- generate_custom_music: Full control with lyrics and style
- extend_music: Continue existing songs
- cover_music: Create cover versions
- concat_music: Merge song segments
- generate_with_persona: Use saved voice styles
- generate_lyrics: Create lyrics from prompt
- create_persona: Save voice styles for reuse
- get_task: Check generation status
- get_tasks_batch: Check multiple tasks at once
"""


@mcp.tool()
async def get_lyric_format_guide() -> str:
    """Get guidance on formatting lyrics for Suno.

    Shows how to structure lyrics with section markers for best results.
    """
    return """Lyric Format Guide for Suno:

Section Markers (use square brackets):
- [Verse] or [Verse 1], [Verse 2]: Main storytelling sections
- [Chorus]: Repeated catchy section
- [Pre-Chorus]: Build-up before chorus
- [Bridge]: Contrasting section, usually near the end
- [Outro]: Ending section
- [Intro]: Opening instrumental or vocals

Example Structure:
```
[Verse 1]
First verse lyrics here
Setting up the story

[Pre-Chorus]
Building anticipation
Leading to the hook

[Chorus]
The main hook goes here
Most memorable part
Repeat this section

[Verse 2]
Second verse continues
The narrative unfolds

[Chorus]
The main hook goes here
Most memorable part
Repeat this section

[Bridge]
Something different here
A twist or climax

[Chorus]
The main hook goes here
Most memorable part
Final repetition

[Outro]
Winding down
Fade out
```

Tips:
- Keep lines concise for better singing flow
- Use simple, clear language
- Include rhymes for catchiness
- Leave some creative freedom for the AI
"""
