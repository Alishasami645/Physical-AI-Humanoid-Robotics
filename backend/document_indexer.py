import os
import re
from pathlib import Path
from typing import List, Dict, Any
from vector_store import vector_store
from database import db_manager
from config import settings


class DocumentIndexer:
    """Indexes markdown documents from the robotics book."""
    
    def __init__(self, docs_path: str):
        self.docs_path = docs_path
    
    def index_all_documents(self) -> Dict[str, Any]:
        """Index all markdown documents in the docs directory."""
        documents = []
        stats = {
            "total_files": 0,
            "indexed_files": 0,
            "total_chunks": 0,
            "errors": []
        }
        
        # Walk through docs directory
        for root, dirs, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith(".md"):
                    stats["total_files"] += 1
                    file_path = os.path.join(root, file)
                    
                    try:
                        docs = self._process_markdown_file(file_path, root)
                        documents.extend(docs)
                        stats["indexed_files"] += 1
                        stats["total_chunks"] += len(docs)
                    except Exception as e:
                        stats["errors"].append({
                            "file": file_path,
                            "error": str(e)
                        })
        
        # Add documents to vector store and database
        if documents:
            embedding_ids = vector_store.add_documents(documents)
            
            # Save to database with embedding IDs
            for doc, embedding_id in zip(documents, embedding_ids):
                db_manager.save_document(
                    title=doc["title"],
                    chapter=doc["chapter"],
                    content=doc["content"],
                    source_url=doc.get("source_url", ""),
                    embedding_id=embedding_id
                )
        
        stats["success"] = True
        return stats
    
    def _process_markdown_file(self, file_path: str, root_path: str) -> List[Dict[str, Any]]:
        """Process a single markdown file into chunks."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        title = self._extract_title(content, file_path)
        chapter = self._extract_chapter(root_path)
        
        # Split content into logical chunks
        chunks = self._chunk_content(content, title, chapter, file_path)
        
        return chunks
    
    def _extract_title(self, content: str, file_path: str) -> str:
        """Extract title from markdown file."""
        # Try to get from frontmatter
        match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        if match:
            return match.group(1)
        
        # Try to get from H1 header
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
        
        # Use filename
        return Path(file_path).stem.replace('-', ' ').title()
    
    def _extract_chapter(self, root_path: str) -> str:
        """Extract chapter name from directory path."""
        parts = root_path.split(os.sep)
        for part in parts:
            if part.startswith('chapter-'):
                return part.replace('-', ' ').title()
        return "General"
    
    def _chunk_content(self, content: str, title: str, chapter: str,
                      file_path: str) -> List[Dict[str, Any]]:
        """Split content into meaningful chunks."""
        chunks = []
        
        # Remove frontmatter
        content = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
        
        # Split by H2 headers for better chunking
        sections = re.split(r'\n## ', content)
        
        for section in sections:
            if section.strip():
                # Clean up section
                section = section.strip()
                
                # Skip very short sections
                if len(section) < 100:
                    continue
                
                # Create chunk
                chunk_title = section.split('\n')[0][:100]
                
                chunk = {
                    "title": f"{title} - {chunk_title}",
                    "chapter": chapter,
                    "content": section[:2000],  # Limit chunk size for embedding
                    "source_url": f"/docs/{file_path}",
                }
                chunks.append(chunk)
        
        # If no chunks were created (single section), use entire content
        if not chunks and content.strip():
            chunks.append({
                "title": title,
                "chapter": chapter,
                "content": content[:2000],
                "source_url": f"/docs/{file_path}",
            })
        
        return chunks


def index_robotics_book(docs_path: str = None) -> Dict[str, Any]:
    """Index the robotics book documents."""
    if docs_path is None:
        # Default path
        docs_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "docs"
        )
    
    indexer = DocumentIndexer(docs_path)
    return indexer.index_all_documents()
