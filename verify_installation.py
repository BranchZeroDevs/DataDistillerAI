"""
Installation Verification Script
=================================

Run this script to verify that DataDistiller AI is properly installed.
"""

import sys
import importlib
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.10+)")
        return False


def check_package(package_name, display_name=None):
    """Check if a package is installed"""
    display = display_name or package_name
    try:
        importlib.import_module(package_name)
        print(f"✅ {display}")
        return True
    except ImportError:
        print(f"❌ {display} (not installed)")
        return False


def check_ollama():
    """Check if Ollama is accessible"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama (running)")
            return True
        else:
            print("❌ Ollama (not responding)")
            return False
    except Exception:
        print("⚠️  Ollama (not running - start with 'ollama serve')")
        return False


def check_directories():
    """Check if required directories exist"""
    dirs = {
        "data": Path("./data"),
        "data/documents": Path("./data/documents"),
        "src": Path("./src")
    }
    
    all_exist = True
    for name, path in dirs.items():
        if path.exists():
            print(f"✅ {name}/ directory")
        else:
            print(f"❌ {name}/ directory (missing)")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("DataDistiller AI - Installation Verification")
    print("=" * 60)
    
    print("\n📋 Checking Python Version:")
    python_ok = check_python_version()
    
    print("\n📦 Checking Required Packages:")
    packages = [
        ("langchain", "LangChain"),
        ("streamlit", "Streamlit"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "FAISS"),
        ("spacy", "spaCy"),
        ("networkx", "NetworkX"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
    ]
    
    packages_ok = all(check_package(pkg, name) for pkg, name in packages)
    
    print("\n🔧 Checking spaCy Model:")
    spacy_model_ok = check_package("en_core_web_sm", "en_core_web_sm (spaCy model)")
    
    print("\n🤖 Checking Ollama:")
    ollama_ok = check_ollama()
    
    print("\n📁 Checking Directory Structure:")
    dirs_ok = check_directories()
    
    print("\n" + "=" * 60)
    
    if python_ok and packages_ok and spacy_model_ok and dirs_ok:
        print("✅ All checks passed! You're ready to use DataDistiller AI.")
        print("\nQuick start:")
        print("  streamlit run app.py")
        
        if not ollama_ok:
            print("\n⚠️  Note: Ollama is not running. Start it with:")
            print("  ollama serve")
            print("  ollama pull qwen2.5:3b")
        
        return 0
    else:
        print("❌ Some checks failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")
        return 1


if __name__ == "__main__":
    sys.exit(main())
