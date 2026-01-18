#!/usr/bin/env python3
"""
Quick Ollama setup for DataDistillerAI
"""

import requests
import sys

print("\n" + "="*80)
print("🦙 OLLAMA SETUP FOR DATADISTILLERAI")
print("="*80 + "\n")

# Check Ollama is running
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    tags_data = response.json()
    models = tags_data.get('models', [])
    
    if not models:
        print("⚠️  No models installed yet")
        print("\nTo install a model, run:")
        print("  ollama pull qwen2.5:7b  (recommended)")
        print("  ollama pull mistral")
        print("  ollama pull llama2")
        sys.exit(1)
    
    print("✓ Ollama is running!\n")
    print("📦 Available models:")
    
    model_names = []
    for model in models:
        name = model['name']
        size = model.get('size', 0)
        size_gb = size / (1024**3) if size else 0
        model_names.append(name)
        print(f"   • {name} ({size_gb:.1f} GB)")
    
    print("\n" + "="*80)
    print("✅ USING MODEL FOR RAG SYSTEM")
    print("="*80 + "\n")
    
    # Use the first/best available model
    selected_model = model_names[0]
    print(f"Selected model: {selected_model}\n")
    
    # Update test script
    test_script = open('test_ollama.py').read()
    test_script = test_script.replace(
        'client = OllamaClient(model="qwen2.5:3b")',
        f'client = OllamaClient(model="{selected_model}")'
    )
    with open('test_ollama.py', 'w') as f:
        f.write(test_script)
    
    print(f"✓ Updated test_ollama.py to use: {selected_model}\n")
    print("Now run:")
    print("  python test_ollama.py\n")
    
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to Ollama at http://localhost:11434")
    print("\nMake sure Ollama is running:")
    print("  ollama serve")
    print("\nIn a new terminal window\n")
    sys.exit(1)

except Exception as e:
    print(f"✗ Error: {e}\n")
    sys.exit(1)
