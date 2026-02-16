# verse-validate

Validate project structure and configuration for sanatan-sdk projects.

## Synopsis

```bash
verse-validate [OPTIONS]
```

## Description

The `verse-validate` command checks if your project follows the recommended directory structure and conventions. It identifies missing directories, configuration errors, and provides actionable recommendations for fixing issues.

This is especially useful for:
- Debugging setup issues
- Verifying project structure after cloning
- Ensuring conventions are followed before deployment
- CI/CD validation pipelines

## Options

### Optional

- `--detailed` - Show detailed validation information
- `--fix` - Auto-fix common issues (creates missing directories and files)
- `--dry-run` - Preview changes without making them (use with `--fix`)
- `--collection NAME` - Validate specific collection only
- `--format FORMAT` - Output format: `text` (default) or `json`

## Examples

### Basic Validation

```bash
# Validate current project
verse-validate

# Output:
# ✅ _data/ directory exists
# ✅ _verses/ directory exists
# ✅ _data/collections.yml is valid (2 enabled collections)
# ⚠️  .env file not found - copy .env.example and add your API keys
# ✅ Project structure is valid!
```

### Detailed Validation

```bash
verse-validate --detailed
```

Shows additional information about:
- API key configuration status
- Number of verse files per collection
- Theme files availability
- Canonical verse YAML files

### Preview Changes (Dry-Run)

```bash
verse-validate --fix --dry-run

# Output:
# 🔍 Dry-run mode: Previewing changes (no files will be modified)...
#   → Would create data/themes/
#   → Would create .env.example
#   → Would create _data/collections.yml
```

See what would be fixed without actually making changes.

### Auto-Fix Common Issues

```bash
verse-validate --fix

# Output:
# 🔧 Auto-fixing common issues...
#   ✓ Created data/themes/
#   ✓ Created .env.example
#   ✓ Created _data/collections.yml
```

Creates missing:
- Required directories (`_data`, `_verses`, `data`)
- Template files (`.env.example`, `_data/collections.yml`)

### Validate Specific Collection

```bash
verse-validate --collection hanuman-chalisa

# Output:
# 📚 Collection Validation:
#   Collection: hanuman-chalisa
#   ✅ Found 43 verse files in _verses/hanuman-chalisa/
#   ✅ Canonical verse file exists: hanuman-chalisa.yaml (43 verses)
#   ✅ Found 2 theme(s) in data/themes/hanuman-chalisa/
#   ✅ Scene descriptions file exists
```

### JSON Output

```bash
verse-validate --format json

# Output for scripting/CI pipelines:
{
  "project_dir": "/path/to/project",
  "issues": [],
  "warnings": ["API key not configured"],
  "successes": ["Directory structure valid"],
  "is_valid": true,
  "total_issues": 0,
  "total_warnings": 1
}
```

## Validation Checks

### Required Structure

The command checks for:

1. **Directories**
   - ✅ `_data/` - Collection registry
   - ✅ `_verses/` - Verse markdown files
   - ✅ `data/` - Canonical text and themes

2. **Configuration Files**
   - ✅ `_data/collections.yml` - Valid YAML with collections
   - ⚠️ `.env` - API keys (warns if missing or placeholder values)
   - ⚠️ `.env.example` - Template (optional but recommended)

### Collection-Specific Checks

For each enabled collection:

1. **Verse Files**
   - `_verses/<collection>/` directory exists
   - Contains `.md` files

2. **Canonical Text**
   - `data/verses/<collection>.yaml` exists
   - Valid YAML syntax
   - Contains verse entries

3. **Themes**
   - `data/themes/<collection>/` directory
   - Theme YAML files exist

4. **Scene Descriptions**
   - `docs/image-prompts/<collection>.md` (auto-generated if missing)

## Exit Codes

- `0` - Validation passed (no critical issues)
- `1` - Validation failed (critical issues found)

Use in CI/CD:
```bash
# Fail build if validation doesn't pass
verse-validate || exit 1
```

## Output Format

### Text Format (Default)

Human-readable output with:
- ✅ Successes in green
- ⚠️ Warnings in yellow (optional items)
- ❌ Issues in red (must be fixed)
- 💡 Recommendations section

### JSON Format

Machine-readable output with:
- `project_dir` - Project root path
- `issues` - Array of critical issues
- `warnings` - Array of warnings
- `successes` - Array of successful checks
- `is_valid` - Boolean validation status
- `collections` - Per-collection validation results (if applicable)

## Common Issues

### "❌ _data/collections.yml not found"

**Fix:**
```bash
verse-validate --fix
# Or manually:
mkdir -p _data
cat > _data/collections.yml << EOF
# Collection registry
EOF
```

### "❌ _data/collections.yml has invalid YAML syntax"

**Fix:**
Validate YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('_data/collections.yml'))"
```

### "⚠️ OPENAI_API_KEY is set but appears to be placeholder"

**Fix:**
```bash
# Edit .env and add your actual API key
nano .env
# Change from: OPENAI_API_KEY=sk-your_openai_key_here
# To: OPENAI_API_KEY=sk-actual_key_from_openai
```

### "⚠️ data/themes/<collection>/ not found"

**Fix:**
```bash
mkdir -p data/themes/hanuman-chalisa
# Create theme file
cat > data/themes/hanuman-chalisa/modern-minimalist.yml << EOF
name: Modern Minimalist
theme:
  generation:
    style_modifier: |
      Modern minimalist spiritual art...
size: "1024x1792"
quality: "standard"
style: "natural"
EOF
```

## Workflow

```bash
# 1. After cloning repository
git clone <repo-url>
cd <repo>
verse-validate

# 2. Fix any issues
verse-validate --fix

# 3. Configure API keys
cp .env.example .env
# Edit .env

# 4. Validate again
verse-validate

# 5. Start generating content
verse-generate --collection <collection> --verse 1
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Validate Project Structure

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install sanatan-sdk
        run: pip install sanatan-sdk
      - name: Validate structure
        run: verse-validate
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
verse-validate || {
    echo "Project validation failed. Fix issues before committing."
    exit 1
}
```

## Notes

- Validation does not require API keys (except for warnings)
- Safe to run multiple times (idempotent)
- `--fix` only creates missing items, never modifies existing files
- JSON output useful for automated tooling and CI/CD
- Warnings don't cause validation to fail (exit code 0)

## See Also

- [verse-init](verse-init.md) - Initialize new project
- [verse-generate](verse-generate.md) - Generate content
- [Usage Guide](../usage.md) - Directory structure conventions
- [Troubleshooting](../troubleshooting.md) - Common issues
