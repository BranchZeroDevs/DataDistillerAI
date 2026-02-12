# Installation Verification

Use the verification script to check your setup.

## Running the Verification

```bash
python verify_installation.py
```

## What It Checks

### Python Version ✓
- Requires Python 3.10 or higher

### Required Packages ✓
- LangChain
- Streamlit
- sentence-transformers
- FAISS
- spaCy
- NetworkX
- Pandas
- NumPy

### spaCy Model ✓
- en_core_web_sm

### Ollama Service ✓
- Running on localhost:11434
- Model availability

### Directory Structure ✓
- data/ directory
- data/documents/
- src/ directory

## Example Output

```
============================================================
DataDistiller AI - Installation Verification
============================================================

📋 Checking Python Version:
✅ Python 3.10.5

📦 Checking Required Packages:
✅ LangChain
✅ Streamlit
✅ sentence-transformers
✅ FAISS
✅ spaCy
✅ NetworkX
✅ Pandas
✅ NumPy

🔧 Checking spaCy Model:
✅ en_core_web_sm (spaCy model)

🤖 Checking Ollama:
✅ Ollama (running)

📁 Checking Directory Structure:
✅ data/ directory
✅ data/documents/ directory
✅ src/ directory

============================================================
✅ All checks passed! You're ready to use DataDistiller AI.

Quick start:
  streamlit run app.py
============================================================
```

## Common Issues

### Missing Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Ollama Not Running

```bash
ollama serve
```

### Directory Issues

The verification creates missing directories automatically.

## Development Verification

For development setup:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run full CI checks
make ci
```

This runs:
- Code formatting checks
- Linting
- Type checking
- Tests (if available)

## Next Steps

Once verification passes:

1. [Quick Start Guide](quickstart.md) - Run the app
2. [Examples](../guides/examples.md) - Try sample queries
3. [FAQ](../guides/faq.md) - Common questions
