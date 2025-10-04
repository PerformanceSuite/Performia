#!/usr/bin/env python3
"""
Knowledge Base RAG System using Docling
Ingests documentation and provides query interface
"""

from docling.document_converter import DocumentConverter
from pathlib import Path
import json

class KnowledgeBase:
    def __init__(self, knowledge_dir="knowledge-base"):
        self.knowledge_dir = Path(knowledge_dir)
        self.converter = DocumentConverter()
        self.documents = {}
        self.index = {}

    def ingest_all(self):
        """Ingest all markdown files from knowledge base."""
        print("📚 Ingesting knowledge base...")

        md_files = list(self.knowledge_dir.rglob("*.md"))
        print(f"   Found {len(md_files)} documents")

        for md_file in md_files:
            try:
                result = self.converter.convert(md_file)
                if result.document:
                    # Store document
                    doc_id = str(md_file.relative_to(self.knowledge_dir))
                    self.documents[doc_id] = {
                        'path': str(md_file),
                        'content': result.document.export_to_markdown(),
                        'name': result.document.name
                    }

                    # Build simple word index
                    content_lower = self.documents[doc_id]['content'].lower()
                    words = content_lower.split()
                    for word in set(words):
                        if word not in self.index:
                            self.index[word] = []
                        self.index[word].append(doc_id)

                    print(f"   ✅ Ingested: {doc_id}")
            except Exception as e:
                print(f"   ❌ Failed to ingest {md_file}: {e}")

        print(f"\n✅ Ingestion complete!")
        print(f"   - {len(self.documents)} documents indexed")
        print(f"   - {len(self.index)} unique terms\n")

    def query(self, search_terms):
        """Query the knowledge base for relevant documents."""
        if isinstance(search_terms, str):
            search_terms = search_terms.lower().split()

        # Find documents containing search terms
        matches = {}
        for term in search_terms:
            if term in self.index:
                for doc_id in self.index[term]:
                    matches[doc_id] = matches.get(doc_id, 0) + 1

        # Sort by relevance (number of matching terms)
        sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)

        return [(doc_id, self.documents[doc_id]) for doc_id, score in sorted_matches]

    def get_answer(self, question):
        """Get answer to a specific question."""
        results = self.query(question)

        if not results:
            return "❌ No relevant documentation found."

        # Return most relevant document
        doc_id, doc = results[0]
        return f"📄 **{doc['name']}** ({doc_id})\n\n{doc['content'][:500]}..."


def test_queries():
    """Test common queries to validate RAG system."""

    kb = KnowledgeBase()
    kb.ingest_all()

    print("🧪 Testing Knowledge Base Queries\n")

    # Test 1: Directory paths question
    print("Q: Where are custom slash commands located?")
    results = kb.query("custom slash commands directory path")
    if results:
        doc_id, doc = results[0]
        print(f"A: Found in {doc_id}")
        # Extract relevant line
        for line in doc['content'].split('\n'):
            if 'custom slash commands' in line.lower() or '~/.claude/commands' in line.lower():
                print(f"   {line.strip()}")
    print()

    # Test 2: Session management
    print("Q: What does /end-session do?")
    results = kb.query("end-session cleanup")
    if results:
        doc_id, doc = results[0]
        print(f"A: Found in {doc_id}")
        print(f"   First match preview: {doc['content'][:200]}...")
    print()

    # Test 3: Audio knowledge
    print("Q: What are Librosa best practices?")
    results = kb.query("librosa parameters")
    if results:
        doc_id, doc = results[0]
        print(f"A: Found in {doc_id}")
        print(f"   Document: {doc['name']}")
    print()

    print("✅ Query tests complete!")


if __name__ == "__main__":
    test_queries()
