#!/usr/bin/env python3
"""
Setup script to integrate Google Gemini API with DataDistillerAI
Gemini has a free tier - no payment method required
"""

import os
import sys
from pathlib import Path

print("\n" + "="*80)
print("🟢 GOOGLE GEMINI API SETUP (FREE TIER)")
print("="*80 + "\n")

print("📋 SETUP STEPS:\n")

print("1️⃣  GET YOUR FREE API KEY:")
print("   • Visit: https://ai.google.dev/")
print("   • Click 'Get API Key' button")
print("   • Create new API key (free, no payment required)")
print("   • Copy the API key\n")

print("2️⃣  ADD TO .env FILE:")
api_key = input("Paste your Gemini API key (press Enter to skip): ").strip()

env_file = Path('.env')
if api_key:
    # Read existing .env
    env_content = env_file.read_text() if env_file.exists() else ""
    
    # Add Gemini key
    if "GOOGLE_API_KEY" not in env_content:
        with open(env_file, 'a') as f:
            f.write(f"\nGOOGLE_API_KEY={api_key}\n")
        print("✓ Gemini API key added to .env\n")
    else:
        # Replace existing
        env_content = env_content.replace(
            [line for line in env_content.split('\n') if 'GOOGLE_API_KEY' in line][0],
            f"GOOGLE_API_KEY={api_key}"
        )
        env_file.write_text(env_content)
        print("✓ Gemini API key updated in .env\n")
    
    print("3️⃣  INSTALL LIBRARY:")
    os.system(f"{sys.executable} -m pip install -q google-generativeai")
    print("✓ google-generativeai installed\n")
    
    print("4️⃣  TEST CONNECTION:")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'Hello from Gemini!' in one sentence.")
        print(f"✓ Gemini Connection: SUCCESS")
        print(f"  Response: {response.text}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")

else:
    print("⏭️  Skipped. To use Gemini, run this script again.\n")

print("="*80)
print("✅ NEXT STEPS:")
print("="*80)
print("""
To use Gemini with DataDistillerAI, update the RAG pipeline:

In src/workflows/__init__.py, change:

    from src.llm import LLMClient
    
To:

    from src.llm_gemini import GeminiClient  # New file
    
I can help you create src/llm_gemini.py if needed!
""")

