# Verse Content SDK

A Python SDK for generating rich multimedia content for verse-based texts. Provides utilities for:

- **Embeddings**: Generate vector embeddings for semantic search (local and OpenAI)
- **Audio**: Text-to-speech generation using ElevenLabs
- **Images**: AI-generated images using DALL-E
- **Deployment**: Cloudflare Workers deployment utilities

## Installation

### From GitHub
```bash
pip install git+https://github.com/sanatan-learnings/verse-content-sdk.git
```

### For Development
```bash
git clone https://github.com/sanatan-learnings/verse-content-sdk.git
cd verse-content-sdk
pip install -e .
```

## Usage

### Command-Line Tools (Recommended)

After installation, the SDK provides command-line tools:

#### Generate All Content for a Verse (Unified Command)
```bash
# Generate everything (text, image, audio) for Chapter 2, Verse 47
verse-generate --chapter 2 --verse 47 --all

# Generate only image and audio
verse-generate --chapter 2 --verse 47 --image --audio

# Generate only image with specific theme
verse-generate --chapter 2 --verse 47 --image --theme modern-minimalist

# For texts without chapters (like Hanuman Chalisa)
verse-generate --verse 15 --all
```

#### Generate Embeddings
```bash
# Using OpenAI (default)
verse-embeddings --verses-dir _verses --output data/embeddings.json

# Using local models (free)
verse-embeddings --verses-dir _verses --output data/embeddings.json --provider huggingface

# With custom paths
verse-embeddings --verses-dir path/to/verses --output path/to/output.json
```

#### Generate Audio
```bash
# Generate all audio files
verse-audio

# Regenerate specific files
verse-audio --regenerate chapter_01_verse_01_full.mp3,chapter_01_verse_01_slow.mp3

# Generate from a specific verse
verse-audio --start-from chapter_02_verse_01_full.mp3
```

#### Generate Images
```bash
# Generate all images for a theme
verse-images --theme-name modern-minimalist

# Regenerate specific images
verse-images --theme-name modern-minimalist --regenerate chapter-01-verse-01.png

# Force regenerate all images
verse-images --theme-name modern-minimalist --force
```

#### Deploy Cloudflare Worker
```bash
# Run from your project root (where wrangler.toml is located)
cd /path/to/your/project
verse-deploy
```

### Python API (For Custom Scripts)

You can also import and use the SDK in your Python code:

```python
from verse_content_sdk.embeddings import generate_embeddings

generate_embeddings(
    verses_dir="path/to/_verses",
    output_file="path/to/embeddings.json",
    provider="openai"  # or "huggingface"
)
```

## Configuration

Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your-openai-key
ELEVENLABS_API_KEY=your-elevenlabs-key
```

## Requirements

- Python 3.8+
- OpenAI API key (for embeddings and image generation)
- ElevenLabs API key (for audio generation)

## License

MIT License - See LICENSE file for details
