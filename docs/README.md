# verse-content-sdk Documentation

Python SDK for generating multimedia content for spiritual texts (Bhagavad Gita, Hanuman Chalisa, etc.)

## Features

- **Unified Generation**: Single command to create text, images, and audio
- **AI-Powered**: GPT-4 for content, DALL-E 3 for images, ElevenLabs for audio
- **Flexible**: Generate everything at once or individual components
- **Theme System**: Configurable visual styles for images
- **Embeddings**: Semantic search with OpenAI or local models

## Installation

```bash
pip install verse-content-sdk
```

Or install from source:

```bash
git clone https://github.com/sanatan-learnings/verse-content-sdk
cd verse-content-sdk
pip install -e .
```

## Quick Start

```bash
# Set up API keys
export OPENAI_API_KEY=sk-...
export ELEVENLABS_API_KEY=...

# Generate complete verse (text, image, audio)
verse-generate --chapter 1 --verse 5 --all

# Generate only image
verse-generate --chapter 1 --verse 5 --image

# Generate embeddings for search
verse-embeddings --verses-dir _verses --output data/embeddings.json
```

## Commands

- **[verse-generate](commands/verse-generate.md)** - Unified command for complete verse generation
- **[verse-images](commands/verse-images.md)** - Generate images using DALL-E 3
- **[verse-audio](commands/verse-audio.md)** - Generate audio using ElevenLabs
- **[verse-embeddings](commands/verse-embeddings.md)** - Generate vector embeddings

See [Troubleshooting](troubleshooting.md) for common issues.

## Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...           # Required for text/images/embeddings
ELEVENLABS_API_KEY=...          # Required for audio
```

## Project Structure

Your project should have this structure:

```
your-project/
├── .env                        # API keys
├── _verses/                    # Verse markdown files
├── docs/
│   ├── image-prompts.md        # Scene descriptions
│   └── themes/
│       └── modern-minimalist.yml  # Theme config
├── images/                     # Generated images
│   └── modern-minimalist/
├── audio/                      # Generated audio
└── data/
    └── embeddings.json         # Search embeddings
```

## Workflow

1. **Generate verse content:**
   ```bash
   verse-generate --chapter 2 --verse 47 --all
   ```

2. **Review generated files:**
   - `_verses/chapter_02_verse_47.md` - Verse text
   - `docs/image-prompts.md` - Scene description
   - `images/modern-minimalist/chapter-02-verse-47.png` - Image
   - `audio/chapter_02_verse_47_*.mp3` - Audio files

3. **Generate embeddings:**
   ```bash
   verse-embeddings --verses-dir _verses --output data/embeddings.json
   ```

## API Costs

| Component | Cost per Verse | Provider |
|-----------|---------------|----------|
| Text generation | ~$0.02 | OpenAI GPT-4 |
| Image | $0.04 (standard) / $0.08 (HD) | DALL-E 3 |
| Audio (2 files) | ~$0.001 | ElevenLabs |
| **Total per verse** | **~$0.06** | |

## Examples

### Generate Everything

```bash
verse-generate --chapter 3 --verse 10 --all
```

### Generate Only Images

```bash
verse-images --theme-name modern-minimalist
```

### Regenerate Specific Files

```bash
verse-images --theme-name modern-minimalist --regenerate chapter-01-verse-01.png
verse-audio --regenerate chapter_01_verse_01_full.mp3,chapter_01_verse_01_slow.mp3
```

## Documentation

- [verse-generate](commands/verse-generate.md) - Complete verse generation
- [verse-images](commands/verse-images.md) - Image generation details
- [verse-audio](commands/verse-audio.md) - Audio generation details
- [verse-embeddings](commands/verse-embeddings.md) - Embeddings generation
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Support

- [GitHub Issues](https://github.com/sanatan-learnings/verse-content-sdk/issues)
- [Examples](https://github.com/sanatan-learnings/bhagavad-gita) - See the Bhagavad Gita project

## License

MIT License
