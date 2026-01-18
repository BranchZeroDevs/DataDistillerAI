#!/usr/bin/env python3
"""Quick query test"""

import requests

print("Testing query endpoint...")

response = requests.post(
    "http://localhost:8000/api/v2/query",
    json={"query": "What is machine learning?", "top_k": 2},
    timeout=30
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ SUCCESS!")
    print(f"\nQuery: {data['question']}")
    print(f"\nAnswer:\n{data['answer'][:200]}...")
    print(f"\nSources: {len(data['sources'])}")
    print(f"Latency: {data['latency_ms']}ms")
else:
    print(f"\n❌ ERROR:")
    print(response.text)
