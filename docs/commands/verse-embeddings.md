# verse-embeddings

Generate vector embeddings for semantic search and RAG (Retrieval Augmented Generation).

## Synopsis

```bash
verse-embeddings --verses-dir PATH --output PATH [OPTIONS]
```

## Description

The `verse-embeddings` command generates vector embeddings for all verses, enabling semantic search and AI-powered guidance features. It supports two providers:
- **OpenAI** (recommended): Higher quality, requires API key
- **HuggingFace** (free): Local models, no API key needed

## Options

### Required

- `--verses-dir PATH` - Path to verses directory (e.g., `_verses/`)
- `--output PATH` - Output JSON file path (e.g., `data/embeddings.json`)

### Optional

- `--provider PROVIDER` - Embedding provider: `openai` or `huggingface` (default: `openai`)
- `--model MODEL` - Model to use (provider-specific)

## Examples

### Using OpenAI (Recommended)

```bash
verse-embeddings --verses-dir _verses --output data/embeddings.json
```

Uses OpenAI's `text-embedding-3-small` model:
- 1536 dimensions
- High quality semantic understanding
- Cost: ~$0.10 for complete Bhagavad Gita (one-time)

### Using Local Models (Free)

```bash
verse-embeddings --verses-dir _verses --output data/embeddings.json --provider huggingface
```

Uses sentence-transformers `all-MiniLM-L6-v2` model:
- 384 dimensions
- Good quality, runs locally
- No API key or cost
- First run downloads model (~80MB)

## Generated Output

Creates a JSON file with embeddings for all verses:

```json
{
  "embeddings": [
    {
      "chapter": 1,
      "verse": 1,
      "verse_id": "chapter_01_verse_01",
      "text": "Combined verse text...",
      "embedding": [0.123, -0.456, ...]
    },
    ...
  ],
  "metadata": {
    "total_verses": 700,
    "provider": "openai",
    "model": "text-embedding-3-small",
    "dimensions": 1536,
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

## Embedding Content

The command combines multiple fields from each verse:

- Sanskrit (devanagari)
- Transliteration
- Translations (English & Hindi)
- Word meanings
- Interpretive meaning
- Story/context
- Practical applications

This creates rich semantic embeddings that capture the full meaning of each verse.

## Workflow

```bash
# 1. Generate embeddings (one-time setup)
verse-embeddings --verses-dir _verses --output data/embeddings.json

# 2. Verify output
ls -lh data/embeddings.json
cat data/embeddings.json | jq '.metadata'

# 3. Use in your application
# The embeddings file is loaded client-side for semantic search

# 4. Regenerate after adding new verses
verse-embeddings --verses-dir _verses --output data/embeddings.json
```

## Integration Example

Client-side semantic search (JavaScript):

```javascript
// Load embeddings
const response = await fetch('/data/embeddings.json');
const { embeddings } = await response.json();

// Search for relevant verses
function findRelevantVerses(query, topK = 3) {
  const queryEmbedding = await generateEmbedding(query);

  const scores = embeddings.map(verse => ({
    ...verse,
    score: cosineSimilarity(queryEmbedding, verse.embedding)
  }));

  return scores
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}
```

## Cost & Performance

### OpenAI

- **Model**: text-embedding-3-small
- **Cost**: $0.00002 per 1,000 tokens
- **For Bhagavad Gita** (700 verses, ~500 tokens each):
  - Total tokens: ~350,000
  - Cost: ~$0.10 (one-time)
- **Generation time**: ~2-3 minutes

### HuggingFace

- **Model**: all-MiniLM-L6-v2
- **Cost**: Free
- **Download size**: ~80MB (first run only)
- **Generation time**: ~10-15 minutes (depends on CPU)
- **Memory**: ~500MB RAM

## Provider Comparison

| Feature | OpenAI | HuggingFace |
|---------|--------|-------------|
| Quality | Excellent | Good |
| Dimensions | 1536 | 384 |
| Cost | ~$0.10 | Free |
| Speed | Fast | Moderate |
| Setup | API key | Model download |
| Best for | Production | Development/testing |

## Requirements

### OpenAI Provider

- `OPENAI_API_KEY` environment variable
- Internet connection

### HuggingFace Provider

- Python packages: `torch`, `sentence-transformers`
- ~80MB disk space for model
- No API key needed

## Use Cases

1. **Semantic Search**: Find verses by meaning, not just keywords
2. **RAG Systems**: Provide context for AI spiritual guidance
3. **Similarity**: Find verses with similar themes
4. **Recommendations**: Suggest related verses to readers

## Notes

- Embeddings are generated once and reused (no need to regenerate on every query)
- Regenerate embeddings when adding new verses
- The output JSON file can be loaded client-side (semantic search runs in browser)
- OpenAI embeddings are recommended for production (better quality)
- HuggingFace is great for development and testing (free, no API needed)

## Troubleshooting

### "Error: OPENAI_API_KEY not set"

For OpenAI provider:

```bash
export OPENAI_API_KEY=sk-...
```

Or use HuggingFace instead:

```bash
verse-embeddings --verses-dir _verses --output data/embeddings.json --provider huggingface
```

### "Error: No verse files found"

Check:
- Verse directory path is correct
- Directory contains `.md` files
- Files have YAML frontmatter

### "Out of memory" (HuggingFace)

HuggingFace model needs ~500MB RAM. If hitting limits:
- Close other applications
- Use OpenAI provider instead (no local processing)

## See Also

- [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings)
- [sentence-transformers Documentation](https://www.sbert.net/)
- [Troubleshooting](../troubleshooting.md) - Common issues
