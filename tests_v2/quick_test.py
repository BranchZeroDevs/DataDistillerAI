#!/usr/bin/env python3
"""Quick test of DataDistiller 2.0"""

import requests
import time

API_URL = "http://localhost:8000"

print("=" * 70)
print("QUICK TEST - DataDistiller 2.0")
print("=" * 70)

# 1. Health check
print("\n1️⃣  Health Check...")
try:
    r = requests.get(f"{API_URL}/health", timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ API is healthy: {r.json()}")
    else:
        print(f"   ❌ API returned {r.status_code}")
except Exception as e:
    print(f"   ❌ Failed to connect: {e}")
    exit(1)

# 2. Upload document
print("\n2️⃣  Uploading Document...")
try:
    with open("data/documents/machine_learning.txt", "rb") as f:
        files = {"file": ("ml.txt", f, "text/plain")}
        r = requests.post(f"{API_URL}/api/v2/documents/upload", files=files, timeout=10)
        print(f"   Status: {r.status_code}")
        if r.status_code == 202:
            data = r.json()
            job_id = data["job_id"]
            print(f"   ✅ Upload accepted")
            print(f"   Job ID: {job_id}")
            print(f"   File: {data['filename']} ({data['file_size']} bytes)")
        else:
            print(f"   ❌ Upload failed: {r.text}")
            exit(1)
except FileNotFoundError:
    print("   ❌ Test file not found")
    exit(1)
except Exception as e:
    print(f"   ❌ Upload failed: {e}")
    exit(1)

# 3. Check status
print("\n3️⃣  Checking Status...")
for i in range(10):
    try:
        r = requests.get(f"{API_URL}/api/v2/documents/status/{job_id}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            status = data["status"]
            progress = data.get("progress", 0)
            print(f"   [{i+1}/10] Status: {status} ({progress}%)")
            
            if status == "completed":
                print(f"   ✅ Processing complete!")
                print(f"   Total chunks: {data.get('total_chunks', 0)}")
                break
            elif status == "failed":
                print(f"   ❌ Processing failed: {data.get('error')}")
                exit(1)
        else:
            print(f"   ❌ Status check failed: {r.status_code}")
        
        time.sleep(3)
    except Exception as e:
        print(f"   ❌ Status check error: {e}")
        time.sleep(3)

# 4. List documents
print("\n4️⃣  Listing Documents...")
try:
    r = requests.get(f"{API_URL}/api/v2/documents/list", timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Found {data['total']} documents")
        for doc in data["documents"][:3]:
            print(f"      • {doc['filename']} - {doc['status']}")
    else:
        print(f"   ❌ List failed: {r.status_code}")
except Exception as e:
    print(f"   ❌ List error: {e}")

# 5. Query
print("\n5️⃣  Testing Query...")
try:
    query_data = {
        "query": "What is machine learning?",
        "top_k": 3
    }
    r = requests.post(f"{API_URL}/api/v2/query", json=query_data, timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Query successful")
        print(f"   Answer: {data['answer'][:200]}...")
        print(f"   Sources: {len(data['sources'])} chunks")
    else:
        print(f"   ⚠️  Query returned {r.status_code}: {r.text[:100]}")
except Exception as e:
    print(f"   ⚠️  Query error: {e}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)
