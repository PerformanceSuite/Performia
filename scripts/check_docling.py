#!/usr/bin/env python3
"""
Verify Docling Installation

This script checks that all RAG knowledge base dependencies are installed
and working correctly.

Usage:
    python scripts/check_docling.py

Exit codes:
    0 - All dependencies installed and working
    1 - One or more dependencies missing or broken
"""

import sys


def check_docling():
    """Check if Docling and related dependencies are installed."""
    print("🔍 Checking Docling installation...\n")

    all_ok = True

    # Check Docling
    try:
        from docling.document_converter import DocumentConverter
        print("✅ Docling installed")
    except ImportError as e:
        print(f"❌ Docling not installed: {e}")
        print("   Install with: pip install docling==2.55.1")
        all_ok = False

    # Check ChromaDB
    try:
        import chromadb
        print("✅ ChromaDB installed")
    except ImportError:
        print("❌ ChromaDB not installed")
        print("   Install with: pip install chromadb")
        all_ok = False

    # Check Sentence Transformers
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence Transformers installed")
    except ImportError:
        print("❌ Sentence Transformers not installed")
        print("   Install with: pip install sentence-transformers")
        all_ok = False

    # Check PyTorch (required by transformers)
    try:
        import torch
        print(f"✅ PyTorch installed (version {torch.__version__})")

        # Check CUDA availability
        if torch.cuda.is_available():
            print(f"   🚀 CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("   💡 CUDA not available (CPU mode)")
    except ImportError:
        print("❌ PyTorch not installed")
        print("   Install with: pip install torch")
        all_ok = False

    # Check Transformers
    try:
        import transformers
        print(f"✅ Transformers installed (version {transformers.__version__})")
    except ImportError:
        print("❌ Transformers not installed")
        print("   Install with: pip install transformers")
        all_ok = False

    # Check Accelerate
    try:
        import accelerate
        print("✅ Accelerate installed")
    except ImportError:
        print("⚠️  Accelerate not installed (optional, but recommended)")
        print("   Install with: pip install accelerate")
        # Not critical, so don't fail

    # Summary
    print("\n" + "="*50)
    if all_ok:
        print("✅ All RAG dependencies ready!")
        print("\nNext steps:")
        print("  1. Build knowledge base: python knowledge_rag.py")
        print("  2. Verify knowledge base: python verify_knowledge.py")
        return True
    else:
        print("❌ Some dependencies are missing")
        print("\nInstall all at once:")
        print("  pip install docling==2.55.1 chromadb sentence-transformers")
        return False


def check_storage():
    """Check available storage space for models."""
    print("\n📦 Checking storage requirements...\n")

    try:
        import shutil
        total, used, free = shutil.disk_usage("/")

        gb_free = free // (2**30)
        print(f"💾 Free disk space: {gb_free} GB")

        if gb_free < 5:
            print("⚠️  Warning: Low disk space. Docling models require ~2-3 GB.")
            print("   Consider freeing up space before installation.")
        else:
            print("✅ Sufficient disk space available")

    except Exception as e:
        print(f"⚠️  Could not check disk space: {e}")


def test_basic_conversion():
    """Test basic document conversion if dependencies are available."""
    print("\n🧪 Testing basic document conversion...\n")

    try:
        from docling.document_converter import DocumentConverter
        from pathlib import Path
        import tempfile

        # Create a test markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\n\nThis is a test.")
            test_file = Path(f.name)

        try:
            converter = DocumentConverter()
            result = converter.convert(test_file)

            if result.document:
                print("✅ Document conversion test passed")
                print(f"   Converted: {test_file.name}")
                return True
            else:
                print("❌ Document conversion test failed")
                return False
        finally:
            # Clean up test file
            test_file.unlink(missing_ok=True)

    except Exception as e:
        print(f"❌ Document conversion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    print("="*50)
    print("Performia RAG Dependency Checker")
    print("="*50 + "\n")

    # Check dependencies
    deps_ok = check_docling()

    # Check storage
    check_storage()

    # Test conversion if deps are OK
    if deps_ok:
        test_ok = test_basic_conversion()
        if test_ok:
            print("\n" + "="*50)
            print("🎉 All checks passed! RAG system ready.")
            print("="*50)
            return 0

    print("\n" + "="*50)
    print("Please install missing dependencies and try again.")
    print("="*50)
    return 1


if __name__ == "__main__":
    sys.exit(main())
