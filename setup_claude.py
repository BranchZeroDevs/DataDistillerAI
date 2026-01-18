#!/usr/bin/env python3
"""
Setup script to integrate Claude API with DataDistillerAI
"""

import os
import sys
from pathlib import Path

print("\n" + "="*80)
print("🧠 CLAUDE (ANTHROPIC) API SETUP")
print("="*80 + "\n")

print("📋 SETUP STEPS:\n")

print("1️⃣  GET YOUR API KEY:")
print("   • Visit: https://console.anthropic.com/")
print("   • Sign up or log in")
print("   • Go to Settings → API Keys")
print("   • Generate new API key")
print("   • Copy the API key (starts with sk-ant-)\n")

print("2️⃣  ADD TO .env FILE:")
api_key = input("Paste your Claude API key (press Enter to skip): ").strip()

env_file = Path('.env')
if api_key:
    # Read existing .env
    env_content = env_file.read_text() if env_file.exists() else ""
    
    # Add Claude key
    if "ANTHROPIC_API_KEY" not in env_content:
        with open(env_file, 'a') as f:
            f.write(f"\nANTHROPIC_API_KEY={api_key}\n")
        print("✓ Claude API key added to .env\n")
    else:
        # Replace existing
        lines = env_content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('ANTHROPIC_API_KEY'):
                new_lines.append(f"ANTHROPIC_API_KEY={api_key}")
            else:
                new_lines.append(line)
        env_file.write_text('\n'.join(new_lines))
        print("✓ Claude API key updated in .env\n")
    
    print("3️⃣  INSTALL LIBRARY:")
    os.system(f"{sys.executable} -m pip install -q anthropic")
    print("✓ anthropic library installed\n")
    
    print("4️⃣  TEST CONNECTION:")
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        # Test API call
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[
                {"role": "user", "content": "Say 'Claude is ready!' in one sentence."}
            ]
        )
        print(f"✓ Claude Connection: SUCCESS")
        print(f"  Response: {response.content[0].text}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
        sys.exit(1)

else:
    print("⏭️  Skipped. To use Claude, run this script again.\n")

print("="*80)
print("✅ NEXT STEPS:")
print("="*80)
print("""
Now test Claude with your RAG system:

  python test_claude.py

Or use it directly:

  from src.llm_claude import ClaudeClient
  
  client = ClaudeClient()
  response = client.generate("Your question here")
  print(response)
""")
