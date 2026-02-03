# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-02-03

### Added
- Multi-collection support for `verse-embeddings` command
  - Process multiple verse collections in a single run
  - New `--multi-collection` and `--collections-file` flags
  - Collection metadata (`collection_key`, `collection_name`) added to embeddings output
  - Permalink extraction from verse frontmatter
  - Enable/disable collections via YAML configuration
- PyPI publishing infrastructure and documentation

### Changed
- `verse-generate` now properly parses and merges generated content into verse files
- Updated README with detailed content generation documentation

### Fixed
- Verse generation YAML frontmatter parsing and merging

## [0.1.0] - Initial Release

### Added
- Core SDK for verse content generation
- `verse-generate` - Complete verse generation with text, images, and audio
- `verse-images` - DALL-E 3 image generation
- `verse-audio` - ElevenLabs audio pronunciation generation
- `verse-embeddings` - Vector embeddings for semantic search
- `verse-deploy` - Cloudflare Worker deployment utilities
- Theme system for configurable visual styles
- Support for chapter-based (Bhagavad Gita) and non-chapter texts (Hanuman Chalisa)
