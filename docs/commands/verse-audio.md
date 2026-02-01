# verse-audio

Generate audio pronunciations for verses using ElevenLabs text-to-speech.

## Synopsis

```bash
verse-audio [OPTIONS]
```

## Description

The `verse-audio` command generates pronunciation audio files using ElevenLabs' text-to-speech API. It reads text from the `devanagari:` field in verse markdown files and creates two versions:
- Full speed (normal)
- Slow speed (0.75x for learning pronunciation)

## Options

- `--verses-dir PATH` - Path to verses directory (default: `_verses/`)
- `--output-dir PATH` - Path to output directory (default: `audio/`)
- `--voice-id ID` - ElevenLabs voice ID (default: pre-configured voice)
- `--regenerate FILE[,FILE...]` - Regenerate specific audio files
- `--force` - Regenerate all audio files (prompts for confirmation)
- `--start-from FILE` - Start generation from specific file

## Examples

### Generate All Audio

```bash
verse-audio
```

Scans `_verses/` directory and generates audio for all verses that don't have audio files yet.

### Regenerate Specific Files

```bash
# Single file
verse-audio --regenerate chapter_01_verse_01_full.mp3

# Multiple files
verse-audio --regenerate chapter_01_verse_01_full.mp3,chapter_01_verse_01_slow.mp3

# Regenerate both speeds for a verse
verse-audio --regenerate chapter_02_verse_47_full.mp3,chapter_02_verse_47_slow.mp3
```

### Resume from Specific Verse

```bash
verse-audio --start-from chapter_05_verse_10_full.mp3
```

Useful for resuming generation after interruption.

### Force Regenerate All

```bash
verse-audio --force
```

This will prompt for confirmation before regenerating all audio files.

## Generated Files

For each verse, two MP3 files are created:

- `chapter_XX_verse_YY_full.mp3` - Full speed (normal)
- `chapter_XX_verse_YY_slow.mp3` - Slow speed (0.75x)

Naming for texts without chapters (e.g., Hanuman Chalisa):
- `verse_XX_full.mp3`
- `verse_XX_slow.mp3`

## Voice Configuration

The SDK uses a pre-configured voice ID. To use a different voice:

```bash
verse-audio --voice-id YOUR_VOICE_ID
```

Find voice IDs in your ElevenLabs dashboard: https://elevenlabs.io/app/voice-library

## Verse File Format

Audio is generated from the `devanagari:` field in verse files:

```yaml
---
devanagari: |
  धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।
  मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।
---
```

The command reads this field and generates audio pronunciation.

## Workflow

```bash
# 1. Ensure verse files exist with devanagari field
cat _verses/chapter_01_verse_01.md

# 2. Generate audio
verse-audio

# 3. Verify files
ls -lh audio/chapter_01_verse_01_*.mp3

# 4. Test audio playback
afplay audio/chapter_01_verse_01_full.mp3  # macOS
mpg123 audio/chapter_01_verse_01_full.mp3  # Linux

# 5. Commit
git add audio/
git commit -m "Add audio pronunciations"
```

## Cost

ElevenLabs pricing is character-based:
- Verses average ~150-300 characters
- Each verse generates 2 files (full + slow)
- Cost: ~$0.001-0.002 per verse

For 700 verses (complete Bhagavad Gita):
- Total cost: ~$0.70-1.40

Very affordable compared to image generation.

## Performance

- Generation speed: ~2-3 seconds per file
- For 700 verses (1400 files): ~45-60 minutes
- Audio files average 200-400 KB each

## Requirements

- `ELEVENLABS_API_KEY` environment variable
- Verse files in `_verses/` with `devanagari:` field populated
- ElevenLabs account with sufficient credits

## Notes

- Audio is only generated if files don't already exist (unless using `--regenerate` or `--force`)
- The slow speed version (0.75x) is ideal for learning pronunciation
- Generated files are MP3 format for broad compatibility
- Both EU and US production environments are supported (auto-detected)

## Troubleshooting

### "Error: ELEVENLABS_API_KEY not set"

Set your API key:

```bash
export ELEVENLABS_API_KEY=your_key_here
```

Or add to `.env` file:

```
ELEVENLABS_API_KEY=your_key_here
```

### "Error: No devanagari field found"

Ensure verse file has the `devanagari:` field in frontmatter:

```yaml
---
devanagari: |
  Your verse text in Devanagari script here
---
```

### "Generation failed for some files"

Check:
- ElevenLabs API key is valid
- Account has sufficient credits
- Internet connection is stable

Use `--regenerate` to retry failed files.

## See Also

- [verse-generate](verse-generate.md) - Generate audio automatically with other content
- [ElevenLabs Documentation](https://elevenlabs.io/docs) - API reference
- [Troubleshooting](../troubleshooting.md) - Common issues
