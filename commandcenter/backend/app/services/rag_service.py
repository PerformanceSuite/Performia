"""
RAG (Retrieval-Augmented Generation) service for knowledge base
Wrapper around the existing process_docs.py knowledge base processor

Note: RAG dependencies are optional and imported lazily.
Install with: pip install langchain langchain-community langchain-chroma chromadb sentence-transformers
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.config import settings

# Lazy imports - only import when RAGService is instantiated
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    HuggingFaceEmbeddings = None
    Chroma = None


class RAGService:
    """Service for knowledge base RAG operations"""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize RAG service

        Args:
            db_path: Path to ChromaDB database (uses config default if not provided)

        Raises:
            ImportError: If RAG dependencies are not installed
        """
        if not RAG_AVAILABLE:
            raise ImportError(
                "RAG dependencies not installed. "
                "Install with: pip install langchain langchain-community langchain-chroma chromadb sentence-transformers"
            )

        self.db_path = db_path or settings.knowledge_base_path
        self.embedding_model_name = settings.embedding_model

        # Initialize embeddings (local model - no API costs)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name
        )

        # Initialize vector store
        self.vectorstore = Chroma(
            collection_name="performia_docs",
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )

    async def query(
        self,
        question: str,
        category: Optional[str] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query the knowledge base

        Args:
            question: Natural language question
            category: Filter by category (optional)
            k: Number of results to return

        Returns:
            List of relevant document chunks with metadata
        """
        # Build filter if category is provided
        filter_dict = {"category": category} if category else None

        # Search with similarity scores
        results = self.vectorstore.similarity_search_with_score(
            question,
            k=k,
            filter=filter_dict
        )

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score),
                "category": doc.metadata.get("category", "unknown"),
                "source": doc.metadata.get("source", "unknown"),
            }
            for doc, score in results
        ]

    async def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        chunk_size: int = 1000
    ) -> int:
        """
        Add a document to the knowledge base

        Args:
            content: Document content
            metadata: Document metadata
            chunk_size: Size of text chunks

        Returns:
            Number of chunks added
        """
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = text_splitter.split_text(content)

        # Prepare metadata for each chunk
        metadatas = [metadata.copy() for _ in chunks]

        # Add to vector store
        self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)

        return len(chunks)

    async def delete_by_source(self, source: str) -> bool:
        """
        Delete documents by source file

        Args:
            source: Source file path

        Returns:
            True if successful
        """
        # Note: ChromaDB delete by metadata filter
        # This requires the collection to support metadata filtering
        try:
            # Get all documents with this source
            results = self.vectorstore.get(
                where={"source": source}
            )

            if results and results.get("ids"):
                self.vectorstore.delete(ids=results["ids"])
                return True

            return False

        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False

    async def get_categories(self) -> List[str]:
        """
        Get list of all categories in the knowledge base

        Returns:
            List of category names
        """
        # This is a simplified implementation
        # In production, you might want to maintain a separate categories table
        try:
            # Get all documents and extract unique categories
            # Note: This might be expensive for large databases
            results = self.vectorstore.get()

            categories = set()
            if results and results.get("metadatas"):
                for metadata in results["metadatas"]:
                    if "category" in metadata:
                        categories.add(metadata["category"])

            return sorted(list(categories))

        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics

        Returns:
            Statistics dictionary
        """
        try:
            results = self.vectorstore.get()

            total_chunks = len(results.get("ids", []))

            # Count by category
            categories = {}
            if results.get("metadatas"):
                for metadata in results["metadatas"]:
                    category = metadata.get("category", "unknown")
                    categories[category] = categories.get(category, 0) + 1

            return {
                "total_chunks": total_chunks,
                "categories": categories,
                "embedding_model": self.embedding_model_name,
                "db_path": self.db_path,
            }

        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                "total_chunks": 0,
                "categories": {},
                "error": str(e)
            }

    def process_directory(
        self,
        directory: str,
        category: str,
        file_extensions: Optional[List[str]] = None
    ) -> int:
        """
        Process all documents in a directory
        This wraps the existing process_docs.py functionality

        Args:
            directory: Directory path
            category: Document category
            file_extensions: List of file extensions to process

        Returns:
            Total number of chunks added
        """
        # Import the existing processor
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "tools" / "knowledge-base"))

        try:
            from process_docs import PerformiaKnowledgeProcessor

            processor = PerformiaKnowledgeProcessor(db_path=self.db_path)
            return processor.process_directory(directory, category)

        except ImportError as e:
            print(f"Error importing process_docs: {e}")
            return 0
