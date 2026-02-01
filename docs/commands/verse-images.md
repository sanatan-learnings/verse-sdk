# verse-images

Generate images for verses using DALL-E 3 based on scene descriptions.

## Synopsis

```bash
verse-images --theme-name THEME [OPTIONS]
```

## Description

The `verse-images` command generates artwork for verses using OpenAI's DALL-E 3 API. It reads scene descriptions from `docs/image-prompts.md` and creates images styled according to a theme configuration.

## Options

### Required

- `--theme-name NAME` - Theme name (must have corresponding `docs/themes/NAME.yml`)

### Optional

- `--regenerate FILE[,FILE...]` - Regenerate specific image files
- `--force` - Regenerate all images (prompts for confirmation)
- `--prompts-file PATH` - Custom path to image prompts file (default: `docs/image-prompts.md`)
- `--output-dir PATH` - Custom output directory (default: `images/THEME_NAME/`)

## Examples

### Generate All Images

```bash
verse-images --theme-name modern-minimalist
```

This reads all scene descriptions from `docs/image-prompts.md` and generates images that don't already exist.

### Regenerate Specific Images

```bash
# Single image
verse-images --theme-name modern-minimalist --regenerate chapter-01-verse-01.png

# Multiple images
verse-images --theme-name modern-minimalist \
  --regenerate chapter-01-verse-01.png,chapter-01-verse-02.png
```

### Force Regenerate All

```bash
verse-images --theme-name modern-minimalist --force
```

This will prompt for confirmation before regenerating all images.

## Theme Configuration

Themes are defined in `docs/themes/THEME_NAME.yml`:

```yaml
name: modern-minimalist
description: Modern minimalist Indian devotional art

style_modifier: |
  Style: Modern minimalist Indian devotional art. Clean composition with balanced negative space.
  Soft, warm color palette featuring deep saffron, spiritual blue, gentle gold accents, and cream tones.
  Simplified forms with spiritual elegance. Subtle divine glow and ethereal lighting.
  Contemporary interpretation of traditional Indian spiritual art.
  Portrait orientation (1024x1792), will be cropped to 1024x1536 for final display.

size: 1024x1792        # Portrait format
quality: standard      # Options: standard, hd
style: natural         # Options: natural, vivid
```

### Theme Options

- **size**: Image dimensions
  - `1024x1024` - Square
  - `1024x1792` - Portrait (recommended)
  - `1792x1024` - Landscape

- **quality**: Image quality
  - `standard` - $0.04 per image
  - `hd` - $0.08 per image, more details

- **style**: Rendering style
  - `natural` - More realistic, balanced
  - `vivid` - More vibrant colors, dramatic

## Scene Descriptions

Scene descriptions are stored in `docs/image-prompts.md`:

```markdown
### Chapter 1, Verse 1

**Scene Description**:
A vast battlefield at Kurukshetra stretches endlessly under a dramatic sky.
Two massive armies face each other - the Kauravas on one side and the Pandavas
on the other, with thousands of warriors, chariots, elephants, and flags visible
in organized formations. [...]
```

### Writing Good Scene Descriptions

- **Length**: 3-5 sentences
- **Details**: Include setting, characters, poses, expressions, clothing, colors
- **Lighting**: Specify mood lighting (golden hour, ethereal glow, dramatic)
- **Balance**: Mix realistic and symbolic/spiritual elements
- **Concrete**: Use visual metaphors, avoid abstract concepts

## Generated Files

Images are saved to: `images/THEME_NAME/chapter-XX-verse-YY.png`

Format:
- Portrait: 1024x1792 (recommended for mobile/web display)
- Quality: Standard or HD based on theme config
- Format: PNG

## Workflow

```bash
# 1. Create theme configuration
cat > docs/themes/mystical-art.yml << EOF
name: mystical-art
style_modifier: |
  Mystical spiritual art with ethereal lighting...
size: 1024x1792
quality: standard
style: natural
EOF

# 2. Add scene descriptions to docs/image-prompts.md
# (Can be done manually or via verse-generate --prompt)

# 3. Generate images
verse-images --theme-name mystical-art

# 4. Review images
open images/mystical-art/

# 5. Regenerate specific images if needed
verse-images --theme-name mystical-art --regenerate chapter-01-verse-05.png
```

## Cost

- **Standard quality**: $0.04 per image
- **HD quality**: $0.08 per image

For 700 verses (complete Bhagavad Gita):
- Standard: ~$28
- HD: ~$56

## Requirements

- `OPENAI_API_KEY` environment variable
- Scene descriptions in `docs/image-prompts.md`
- Theme configuration in `docs/themes/THEME_NAME.yml`

## Notes

- Images are only generated if they don't already exist (unless using `--regenerate` or `--force`)
- Generation takes ~10-15 seconds per image
- DALL-E 3 works best with detailed, concrete visual descriptions
- Portrait orientation (1024x1792) works well for mobile and web display

## See Also

- [verse-generate](verse-generate.md) - Generate scene descriptions automatically
- [Troubleshooting](../troubleshooting.md) - Common issues
