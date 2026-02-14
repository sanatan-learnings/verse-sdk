# verse-fetch-text (Removed)

> **⚠️ This command was removed in v0.9.1**

The `verse-fetch-text` command is no longer available as of v0.9.1.

## Why Was It Removed?

Since v0.8.0, web scraping was removed in favor of **local-only canonical sources**. The command only read from local YAML files and no longer "fetched" anything, making the name misleading.

## Current Approach

All commands now **automatically read verse text from local YAML files**:

**Required file**: `data/verses/{collection}.yaml` or `.yml`

```yaml
# Example: data/verses/sundar-kaand.yaml
chaupai_01:
  devanagari: "जामवंत के बचन सुहाए। सुनि हनुमंत हृदय अति भाए।।"

chaupai_02:
  devanagari: "तब हनुमंत मध्य आकाश। बोले जोरि कर प्रभु भाष।।"
```

## Migration Guide

### Before (v0.8.x and earlier)

```bash
# Separate command to fetch text
verse-fetch-text --collection sundar-kaand --verse chaupai_01
```

### After (v0.9.1+)

No separate command needed. All commands read directly from local files:

```bash
# Text is automatically read from data/verses/sundar-kaand.yaml
verse-generate --collection sundar-kaand --verse 1
verse-status --collection sundar-kaand --verse 1
verse-sync --collection sundar-kaand --verse 1
```

## Related Commands

- **[verse-generate](verse-generate.md)** - Generate verse content (reads text automatically)
- **[verse-status](verse-status.md)** - Check status and validate text against canonical source
- **[verse-sync](verse-sync.md)** - Sync verse text with canonical source (fix mismatches)
- **[verse-translate](verse-translate.md)** - Translate verses into multiple languages

## See Also

- **[Local Verses Guide](../local-verses.md)** - How to create and manage local YAML verse files
- **[Usage Guide](../usage.md)** - Complete workflows and best practices

## Version History

- **v0.8.0** - Removed web scraping, local files became required
- **v0.9.1** - Removed command entirely (redundant with local-only approach)
