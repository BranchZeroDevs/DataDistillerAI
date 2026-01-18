#!/usr/bin/env python3
"""System Status Dashboard"""

import requests
import subprocess
import json

API_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)

def check_docker():
    """Check Docker services"""
    print_section("🐳 DOCKER SERVICES")
    result = subprocess.run(
        ["docker", "compose", "ps", "--format", "json"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        services = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
        for svc in services:
            name = svc['Service'].ljust(15)
            state = svc['State']
            health = svc.get('Health', 'N/A')
            status_icon = "✅" if state == "running" else "❌"
            print(f"  {status_icon} {name} {state:10} {health}")
    else:
        print("  ❌ Docker not running")

def check_api():
    """Check API health"""
    print_section("🚀 API SERVER")
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        if r.status_code == 200:
            data = r.json()
            print(f"  ✅ API: {data['status']} (v{data['version']})")
            for svc, status in data.get('services', {}).items():
                print(f"     • {svc}: {status}")
        else:
            print(f"  ❌ API returned {r.status_code}")
    except:
        print("  ❌ API not responding")

def check_documents():
    """Check indexed documents"""
    print_section("📄 INDEXED DOCUMENTS")
    try:
        r = requests.get(f"{API_URL}/api/v2/documents/list", timeout=3)
        if r.status_code == 200:
            data = r.json()
            print(f"  Total: {data['total']} documents")
            print()
            for doc in data['documents']:
                status_icon = "✅" if doc['status'] == 'completed' else "🔄" if doc['status'] == 'embedding' else "⏳"
                print(f"  {status_icon} {doc['filename']}")
                print(f"     Status: {doc['status']} ({doc['progress']}%)")
                print(f"     Chunks: {doc.get('total_chunks', 0)}")
                print(f"     Size: {doc['file_size']} bytes")
                print()
        else:
            print("  ❌ Failed to fetch documents")
    except:
        print("  ❌ Cannot connect to API")

def check_workers():
    """Check worker processes"""
    print_section("⚙️  WORKERS")
    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True
    )
    
    ingestion_running = "ingestion_worker.py" in result.stdout
    embedding_running = "embedding_worker.py" in result.stdout
    
    print(f"  {'✅' if ingestion_running else '❌'} Ingestion Worker")
    print(f"  {'✅' if embedding_running else '❌'} Embedding Worker")

def main():
    print("\n" + "="*70)
    print("  DATADISTILLER 2.0 - SYSTEM STATUS")
    print("="*70)
    
    check_docker()
    check_api()
    check_workers()
    check_documents()
    
    print("\n" + "="*70)
    print("  QUICK COMMANDS")
    print("="*70)
    print("\n  View logs:")
    print("    docker compose logs -f kafka")
    print("    docker compose logs -f postgres")
    print()
    print("  Access UIs:")
    print("    Kafka UI:  http://localhost:9000")
    print("    MinIO:     http://localhost:9001 (minioadmin/minioadmin123)")
    print("    Grafana:   http://localhost:3000 (admin/admin123)")
    print()
    print("  Test upload:")
    print("    python quick_test.py")
    print()

if __name__ == "__main__":
    main()
