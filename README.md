# verse-content-sdk

Python SDK for generating multimedia content for spiritual text collections (Hanuman Chalisa, Sundar Kaand, etc.)

## Features

- **📚 Collection-Aware**: Organized support for multiple verse collections
- **🎯 Simple Generation**: Generate images and audio for specific verses
- **🤖 AI-Powered**: DALL-E 3 for images, ElevenLabs for audio
- **🔍 Semantic Search**: Vector embeddings for intelligent verse search
- **🎨 Theme System**: Configurable visual styles for images
- **🎵 Audio**: Verse pronunciation in full and slow speeds

## Quick Start

```bash
# Install
pip install verse-content-sdk

# Set up API keys
export OPENAI_API_KEY=sk-...
export ELEVENLABS_API_KEY=...

# List available collections
verse-generate --list-collections

# Generate image and audio for a verse
verse-generate --collection hanuman-chalisa --verse 15 --all --theme modern-minimalist

# Or generate specific components
verse-generate --collection sundar-kaand --verse 3 --image --theme modern-minimalist
verse-generate --collection sankat-mochan-hanumanashtak --verse 5 --audio
```

The `--all` flag generates:
- ✅ DALL-E 3 generated image (saved to `images/{collection}/{theme}/`)
- ✅ Full-speed pronunciation (saved to `audio/{collection}/{verse}_full.mp3`)
- ✅ Slow-speed pronunciation (saved to `audio/{collection}/{verse}_slow.mp3`)

## Installation

### From PyPI (Recommended)

```bash
pip install verse-content-sdk
```

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

## Commands

### verse-generate

Orchestrates image and audio generation for a specific verse.

```bash
# Generate both image and audio
verse-generate --collection hanuman-chalisa --verse 15 --all --theme modern-minimalist

# Generate only image
verse-generate --collection sundar-kaand --verse 3 --image --theme modern-minimalist

# Generate only audio
verse-generate --collection sankat-mochan-hanumanashtak --verse 5 --audio

# List available collections
verse-generate --list-collections
```

**[Full documentation](docs/commands/verse-generate.md)**

### verse-images

Generate images using DALL-E 3 for a collection.

```bash
# Generate all images for a collection and theme
verse-images --collection hanuman-chalisa --theme modern-minimalist

# Generate specific verse
verse-images --collection sundar-kaand --theme modern-minimalist --verse chaupai_03

# Regenerate specific image
verse-images --collection hanuman-chalisa --theme kids-friendly --regenerate verse-15.png

# List available collections
verse-images --list-collections
```

**[Full documentation](docs/commands/verse-images.md)**

### verse-audio

Generate audio pronunciations using ElevenLabs for a collection.

```bash
# Generate all audio for a collection
verse-audio --collection hanuman-chalisa

# Generate specific verse
verse-audio --collection sundar-kaand --verse chaupai_03

# Regenerate specific files
verse-audio --collection hanuman-chalisa --regenerate verse_01_full.mp3,verse_01_slow.mp3

# List available collections
verse-audio --list-collections
```

**[Full documentation](docs/commands/verse-audio.md)**

### verse-embeddings

Generate vector embeddings for semantic search. Supports single or multi-collection processing.

```bash
# Single collection (default)
verse-embeddings --verses-dir _verses --output data/embeddings.json

# Multi-collection mode (process multiple collections at once)
verse-embeddings --multi-collection --collections-file ./collections.yml

# Using local models (free)
verse-embeddings --provider huggingface
```

**[Full documentation](docs/commands/verse-embeddings.md)** | **[Multi-collection guide](docs/multi-collection.md)**

### verse-deploy

Deploy Cloudflare Worker for API proxy.

```bash
verse-deploy
```

## Configuration

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Directory Structure Conventions

The SDK follows a **convention-over-configuration** approach. Your project must follow this structure:

```
your-project/
├── .env                                  # API keys
├── _data/
│   └── collections.yml                   # Collection registry
├── _verses/
│   ├── <collection-key>/                 # Verse files by collection
│   │   ├── verse_01.md
│   │   ├── verse_02.md
│   │   └── ...
│   ├── sundar-kaand/
│   │   ├── chaupai_01.md
│   │   └── ...
│   └── sankat-mochan-hanumanashtak/
│       ├── verse_01.md
│       └── ...
├── docs/
│   ├── image-prompts/                    # Scene descriptions by collection
│   │   ├── <collection-key>.md
│   │   ├── sundar-kaand.md
│   │   └── sankat-mochan-hanumanashtak.md
│   └── themes/
│       └── <collection-key>/             # Theme configs by collection
│           ├── modern-minimalist.yml
│           ├── kids-friendly.yml
│           └── ...
├── images/
│   └── <collection-key>/                 # Generated images by collection and theme
│       ├── <theme-name>/
│       │   ├── verse-01.png
│       │   └── ...
│       └── kids-friendly/
│           └── ...
├── audio/
│   └── <collection-key>/                 # Generated audio by collection
│       ├── verse_01_full.mp3
│       ├── verse_01_slow.mp3
│       └── ...
└── data/
    └── embeddings.json                   # Search embeddings (all collections)
```

### Key Conventions

1. **Collection Keys**: Use kebab-case (e.g., `hanuman-chalisa`, `sundar-kaand`)
2. **Verse Files**: Named `verse_NN.md` or custom names like `chaupai_NN.md`
3. **Image Prompts**: One file per collection in `docs/image-prompts/<collection-key>.md`
4. **Theme Files**: One YAML file per theme in `docs/themes/<collection-key>/<theme-name>.yml`
5. **Collections Registry**: Define all collections in `_data/collections.yml` with `enabled: true`

### Example collections.yml

```yaml
hanuman-chalisa:
  enabled: true
  name:
    en: "Hanuman Chalisa"
    hi: "हनुमान चालीसा"
  # ... other metadata

sundar-kaand:
  enabled: true
  name:
    en: "Sundar Kaand"
    hi: "सुंदर काण्ड"
```

## API Costs

| Component | Cost per Verse | Provider |
|-----------|---------------|----------|
| Text generation | ~$0.02 | OpenAI GPT-4 |
| Image | $0.04 (standard) / $0.08 (HD) | DALL-E 3 |
| Audio (2 files) | ~$0.001 | ElevenLabs |
| **Total per verse** | **~$0.06** | |

**For 700 verses** (complete Bhagavad Gita): **~$42**

## Examples

### Generate Media for a Verse

Generate image and audio for a specific verse:

```bash
# Generate both image and audio
verse-generate --collection hanuman-chalisa --verse 15 --all --theme modern-minimalist

# Review generated files
ls images/hanuman-chalisa/modern-minimalist/verse-15.png
ls audio/hanuman-chalisa/verse_15_full.mp3
ls audio/hanuman-chalisa/verse_15_slow.mp3
```

### Generate Media for an Entire Collection

Generate all images for a collection:

```bash
# Generate all images for a theme
verse-images --collection sundar-kaand --theme modern-minimalist

# Review generated files
ls images/sundar-kaand/modern-minimalist/
```

Generate all audio for a collection:

```bash
# Generate all audio
verse-audio --collection sankat-mochan-hanumanashtak

# Review generated files
ls audio/sankat-mochan-hanumanashtak/
```

### Generate Embeddings for Search

```bash
# Generate embeddings for all collections
verse-embeddings --multi-collection --collections-file _data/collections.yml

# Review generated file
cat data/embeddings.json
```

### Batch Process Multiple Verses

Generate media for verses 1-10:

```bash
for i in {1..10}; do
  verse-generate --collection hanuman-chalisa --verse $i --all --theme modern-minimalist
  sleep 5  # Rate limiting
done
```

## Documentation

### User Guides

- **[Main Documentation](docs/README.md)** - Overview and quick start
- **[verse-generate](docs/commands/verse-generate.md)** - Complete verse generation
- **[verse-images](docs/commands/verse-images.md)** - Image generation
- **[verse-audio](docs/commands/verse-audio.md)** - Audio generation
- **[verse-embeddings](docs/commands/verse-embeddings.md)** - Embeddings generation
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

### For Maintainers

- **[Publishing to PyPI](docs/publishing.md)** - How to publish new releases

## Example Projects

- [Hanuman Chalisa](https://github.com/sanatan-learnings/hanuman-chalisa) - Multi-collection project with Hanuman Chalisa, Sundar Kaand, and Sankat Mochan Hanumanashtak

## Requirements

- Python 3.8+
- OpenAI API key (for text/images/embeddings)
- ElevenLabs API key (for audio)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

- [GitHub Issues](https://github.com/sanatan-learnings/verse-content-sdk/issues)
- [Documentation](docs/README.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
