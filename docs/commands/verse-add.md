# verse-add

Add new verse placeholders to existing collections.

## Synopsis

```bash
verse-add --collection COLLECTION --verse NUMBER [OPTIONS]
```

## Description

The `verse-add` command adds new verse entries to an existing collection. It updates the canonical YAML file (`data/verses/<collection>.yaml`) with placeholder entries and optionally creates corresponding markdown files in `_verses/<collection>/`.

**Smart Format Detection**: The command automatically infers the verse naming format from existing entries. If you have `verse-01`, `verse-02`, it will continue with `verse-03`. If you have `chaupai-1`, `chaupai-2`, it will use that format. This ensures consistency across your collection.

This is useful when:
- Expanding a collection with additional verses
- Adding missing verses to an incomplete collection
- Batch-creating verse placeholders for new content

## Options

### Required

- `--collection COLLECTION` - Collection key (e.g., `hanuman-chalisa`)
- `--verse NUMBER` - Verse number or range (e.g., `44` or `44-50`)

### Optional

- `--no-markdown` - Don't create markdown files (only update YAML)
- `--format FORMAT` - Verse ID format (default: `verse-{:02d}`)

## Examples

### Add Single Verse

```bash
verse-add --collection hanuman-chalisa --verse 44

# Output:
# 📝 Adding verses to Hanuman Chalisa
#    Collection: hanuman-chalisa
#    Verses: 44 (1 verse(s))
#
# Updating canonical YAML file:
#   ✓ Added verse-44 to hanuman-chalisa.yaml
#
# Creating markdown files:
#   ✓ Created verse-44.md
#
# ✅ Summary:
#    YAML entries added: 1
#    Markdown files created: 1
```

This adds a placeholder entry to `data/verses/hanuman-chalisa.yaml` and creates `_verses/hanuman-chalisa/verse-44.md`.

### Add Multiple Verses (Range)

```bash
verse-add --collection hanuman-chalisa --verse 44-50

# Output:
# 📝 Adding verses to Hanuman Chalisa
#    Collection: hanuman-chalisa
#    Verses: 44-50 (7 verse(s))
#
# Updating canonical YAML file:
#   ✓ Added verse-44 to hanuman-chalisa.yaml
#   ✓ Added verse-45 to hanuman-chalisa.yaml
#   ...
#   ✓ Added verse-50 to hanuman-chalisa.yaml
```

Adds 7 verses in one command (verses 44 through 50).

### Add Without Markdown Files

```bash
verse-add --collection hanuman-chalisa --verse 44-50 --no-markdown

# Only updates data/verses/hanuman-chalisa.yaml
# Does not create markdown files
```

Useful when you want to add canonical text first before creating verse pages.

### Add with Custom Format

```bash
verse-add --collection bhagavad-gita --verse 1 --format "chapter-01-verse-{:02d}"

# Creates: chapter-01-verse-01 instead of verse-01
```

## Output Files

### YAML Entry (data/verses/<collection>.yaml)

```yaml
verse-44:
  devanagari: |
    # Add Devanagari text here
  transliteration: |
    # Add transliteration here (optional)
```

### Markdown File (_verses/<collection>/verse-44.md)

```markdown
---
layout: verse
collection: hanuman-chalisa
verse_number: 44
title: "Verse 44"
---

Add verse content here.
```

## Workflow

Typical workflow for adding new verses:

```bash
# 1. Add verse placeholders
verse-add --collection hanuman-chalisa --verse 44-50

# 2. Edit canonical YAML file
# Edit data/verses/hanuman-chalisa.yaml
# Add Devanagari text for each new verse

# 3. Edit markdown files (if needed)
# Edit _verses/hanuman-chalisa/verse-44.md (and others)

# 4. Update collection configuration
# Edit _data/collections.yml
# Update total_verses: 50

# 5. Generate multimedia content
verse-generate --collection hanuman-chalisa --verse 44-50
```

## Behavior

### Existing Verses

If a verse already exists, it will be skipped:

```bash
verse-add --collection hanuman-chalisa --verse 1

# Output:
# ⚠️  Skipped verse-01 (already exists)
```

Safe to run multiple times - won't overwrite existing content.

### File Creation

- **YAML file**: Created if it doesn't exist, updated if it does
- **Markdown files**: Only created if they don't exist
- **Directories**: Created automatically if needed (`data/verses/`, `_verses/<collection>/`)

## Use Cases

### Expanding a Collection

```bash
# Collection has verses 1-43, add verse 44
verse-add --collection hanuman-chalisa --verse 44
```

### Adding Missing Verses

```bash
# Collection is missing verses 10-15
verse-add --collection sundar-kaand --verse 10-15
```

### Bulk Placeholder Creation

```bash
# Create placeholders for all Bhagavad Gita Chapter 1 verses
verse-add --collection bhagavad-gita --verse 1-46
```

### YAML-Only Updates

```bash
# Add canonical text first, create pages later
verse-add --collection hanuman-chalisa --verse 44-50 --no-markdown

# Later, create markdown files manually or with another tool
```

## Next Steps After Adding

1. **Edit canonical YAML** - Add Devanagari text in `data/verses/<collection>.yaml`
2. **Edit verse files** - Customize markdown files in `_verses/<collection>/`
3. **Update collections.yml** - Set correct `total_verses` count
4. **Generate content** - Run `verse-generate` to create images, audio, etc.

## Integration with Other Commands

- **verse-validate** - Validates that verse files match YAML entries
- **verse-generate** - Generates multimedia for newly added verses
- **verse-init** - Creates initial structure (use verse-add for expansion)

## Error Handling

```bash
# Collection doesn't exist
verse-add --collection unknown --verse 1
# Error: Collection 'unknown' not found in collections.yml

# Invalid verse format
verse-add --collection hanuman-chalisa --verse abc
# Error: Invalid verse format 'abc'. Use a number or range

# Missing required arguments
verse-add --collection hanuman-chalisa
# Error: the following arguments are required: --verse
```

## Tips

- Use ranges (`44-50`) to add multiple verses efficiently
- Run `verse-validate` after adding to check project structure
- Update `total_verses` in `_data/collections.yml` after adding verses
- Use `--no-markdown` if you want to add canonical text before creating pages
- Always commit canonical YAML files to version control

## See Also

- [verse-init](verse-init.md) - Initialize new projects
- [verse-validate](verse-validate.md) - Validate project structure
- [verse-generate](verse-generate.md) - Generate multimedia content
