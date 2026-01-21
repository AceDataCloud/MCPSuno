# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-21

### Added

- Initial release of MCP Suno Server
- Audio generation tools:
  - `generate_music` - Generate music from text prompts
  - `generate_custom_music` - Generate with custom lyrics and style
  - `extend_music` - Extend existing songs
  - `cover_music` - Create cover versions
  - `concat_music` - Merge extended segments
  - `generate_with_persona` - Use saved voice styles
- Lyrics generation:
  - `generate_lyrics` - Create lyrics from prompts
- Persona management:
  - `create_persona` - Save voice styles for reuse
- Task tracking:
  - `get_task` - Query single task status
  - `get_tasks_batch` - Query multiple tasks
- Information tools:
  - `list_models` - List available models
  - `list_actions` - List available actions
  - `get_lyric_format_guide` - Lyric formatting help
- Support for all Suno models (v3, v3.5, v4, v4.5, v4.5+, v5)
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/mcp-suno/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/mcp-suno/releases/tag/v0.1.0
