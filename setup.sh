#!/bin/bash
# Quick setup script for DataDistillerAI

set -e

echo "🚀 DataDistillerAI Setup Script"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create necessary directories
mkdir -p data/documents data/vector_store
echo "✓ Data directories created"

# Create .env from template if needed
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your OpenAI API key"
fi

# Create sample data
echo "Creating sample data..."
python examples/sample_data.py
echo "✓ Sample data created"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your OpenAI API key"
echo "2. Run: python examples/basic_rag.py"
echo "3. Or run: python cli.py"
echo ""
