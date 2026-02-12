# Quick Start Guide

Get DataDistiller AI running in just 5 minutes!

## Prerequisites

- Python 3.10 or higher
- 8 GB RAM (16 GB recommended)
- macOS, Linux, or Windows

## Step 1: Install Ollama

Ollama provides local LLM inference.

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Download from [ollama.ai](https://ollama.ai)

## Step 2: Start Ollama & Download Model

```bash
# Start Ollama service
ollama serve

# In another terminal, download a model
ollama pull qwen2.5:3b
```

## Step 3: Install DataDistiller

```bash
# Clone repository
git clone https://github.com/BranchZeroDevs/DataDistillerAI.git
cd DataDistillerAI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Step 4: Launch the Application

```bash
streamlit run app.py
```

Open your browser to [http://localhost:8501](http://localhost:8501)

## Step 5: Upload Documents & Ask Questions

1. Upload documents (PDF, DOCX, TXT) in the sidebar
2. Wait for indexing to complete
3. Ask questions in natural language
4. Explore knowledge graph visualizations

## Quick Example

Try the quickstart script:

```bash
python examples/quickstart.py
```

## Verify Installation

```bash
python verify_installation.py
```

This checks that all dependencies are installed correctly.

## Troubleshooting

### Ollama not responding

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Model not found

```bash
# List available models
ollama list

# Download model
ollama pull qwen2.5:3b
```

### spaCy model missing

```bash
python -m spacy download en_core_web_sm --force
```

## Next Steps

- Read the [Architecture Overview](../architecture/overview.md)
- Try the [Examples](../guides/examples.md)
- Check the [FAQ](../guides/faq.md)

## Getting Help

- [GitHub Issues](https://github.com/BranchZeroDevs/DataDistillerAI/issues)
- [Discussions](https://github.com/BranchZeroDevs/DataDistillerAI/discussions)
