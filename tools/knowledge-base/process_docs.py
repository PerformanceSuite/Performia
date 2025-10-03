#!/usr/bin/env python3
"""
Docling Document Processing Pipeline for Performia Knowledge Base

This script processes technical documentation (PDFs, HTML, etc.) into a RAG-ready
vector database using Docling for document parsing and ChromaDB for storage.

Architecture:
    PDF/HTML → Docling → Markdown → Text Chunks → Embeddings → ChromaDB

Usage:
    python process_docs.py --input docs/knowledge-base/supercollider/ --category supercollider
    python process_docs.py --url https://juce.com/learn/documentation --category juce
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from docling.document_converter import DocumentConverter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma


class PerformiaKnowledgeProcessor:
    """Process documentation into ChromaDB vector database"""

    def __init__(self, db_path: str = "docs/knowledge-base/chromadb"):
        self.db_path = db_path
        self.converter = DocumentConverter()

        # Initialize embeddings (local model - no API costs)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize vector store
        self.vectorstore = Chroma(
            collection_name="performia_docs",
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )

        # Text splitter configuration
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_file(self, file_path: str, category: str, metadata: Dict[str, Any] = None) -> int:
        """
        Process a single document file

        Args:
            file_path: Path to document (PDF, HTML, DOCX, etc.)
            category: Document category (supercollider, juce, audio-dsp, etc.)
            metadata: Additional metadata to attach

        Returns:
            Number of chunks added to vector store
        """
        print(f"Processing: {file_path}")

        # Convert document to markdown using Docling
        result = self.converter.convert(file_path)
        markdown_text = result.document.export_to_markdown()

        # Save processed markdown
        output_dir = Path("docs/knowledge-base/processed") / category
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{Path(file_path).stem}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        print(f"  → Saved markdown: {output_file}")

        # Split into chunks
        chunks = self.text_splitter.split_text(markdown_text)
        print(f"  → Split into {len(chunks)} chunks")

        # Prepare metadata
        base_metadata = {
            "source": file_path,
            "category": category,
            "processed_file": str(output_file)
        }
        if metadata:
            base_metadata.update(metadata)

        # Add to vector store
        metadatas = [base_metadata.copy() for _ in chunks]
        self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)
        print(f"  → Added to vector store\n")

        return len(chunks)

    def process_directory(self, directory: str, category: str) -> int:
        """
        Process all documents in a directory

        Args:
            directory: Directory containing documents
            category: Document category

        Returns:
            Total number of chunks added
        """
        total_chunks = 0
        dir_path = Path(directory)

        # Supported file types
        extensions = ['.pdf', '.html', '.docx', '.md', '.txt']

        for ext in extensions:
            for file_path in dir_path.glob(f"**/*{ext}"):
                try:
                    chunks = self.process_file(str(file_path), category)
                    total_chunks += chunks
                except Exception as e:
                    print(f"ERROR processing {file_path}: {e}\n")

        return total_chunks

    def query(self, question: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the knowledge base

        Args:
            question: Natural language question
            k: Number of results to return

        Returns:
            List of relevant document chunks with metadata
        """
        results = self.vectorstore.similarity_search_with_score(question, k=k)

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in results
        ]


def main():
    parser = argparse.ArgumentParser(
        description="Process documentation into Performia knowledge base"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input file or directory to process"
    )
    parser.add_argument(
        "--category",
        required=True,
        choices=["supercollider", "juce", "audio-dsp", "music-theory", "research"],
        help="Documentation category"
    )
    parser.add_argument(
        "--query",
        help="Query the knowledge base instead of processing"
    )
    parser.add_argument(
        "--db-path",
        default="docs/knowledge-base/chromadb",
        help="Path to ChromaDB database"
    )

    args = parser.parse_args()

    # Initialize processor
    processor = PerformiaKnowledgeProcessor(db_path=args.db_path)

    # Query mode
    if args.query:
        print(f"Querying: {args.query}\n")
        results = processor.query(args.query)

        for i, result in enumerate(results, 1):
            print(f"Result {i} (score: {result['score']:.4f})")
            print(f"Category: {result['metadata']['category']}")
            print(f"Source: {result['metadata']['source']}")
            print(f"Content:\n{result['content'][:500]}...\n")

        return

    # Processing mode
    input_path = Path(args.input)

    if input_path.is_file():
        chunks = processor.process_file(str(input_path), args.category)
        print(f"\n✅ Processed 1 file, {chunks} chunks added")
    elif input_path.is_dir():
        chunks = processor.process_directory(str(input_path), args.category)
        print(f"\n✅ Processed directory, {chunks} total chunks added")
    else:
        print(f"ERROR: {args.input} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
