#!/usr/bin/env python3
"""
Test basic docling functionality with sample documents.
This validates that docling can ingest and process markdown files.
"""

from docling.document_converter import DocumentConverter
from pathlib import Path

def test_basic_ingestion():
    """Test ingesting a simple markdown file."""

    # Initialize converter
    converter = DocumentConverter()

    # Test with our COMMON_MISTAKES.md file
    test_file = Path.home() / ".claude" / "COMMON_MISTAKES.md"

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False

    print(f"📄 Testing ingestion of: {test_file}")

    try:
        # Convert document
        result = converter.convert(test_file)

        # Check if document was processed
        if result.document:
            print(f"✅ Document ingested successfully!")
            print(f"   - Title: {result.document.name}")
            print(f"   - Pages: {len(list(result.document.pages))}")

            # Show first few lines of content
            doc_text = result.document.export_to_markdown()
            lines = doc_text.split('\n')[:5]
            print(f"   - Preview:")
            for line in lines:
                print(f"     {line}")

            return True
        else:
            print("❌ Document conversion failed - no document returned")
            return False

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Docling Basic Ingestion\n")
    success = test_basic_ingestion()

    if success:
        print("\n✅ Basic ingestion test passed!")
        print("Next: Set up RAG system for querying")
    else:
        print("\n❌ Basic ingestion test failed")
        print("Check docling installation and file permissions")
