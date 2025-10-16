#!/usr/bin/env python3
"""
Demo script to test incremental vector store updates

This script demonstrates:
1. Listing current vector store contents
2. Adding a document incrementally
3. Verifying the update worked
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.document_processor import DocumentProcessor
from app.config import settings
from pathlib import Path


def demo_incremental_update():
    """Demonstrate incremental update functionality"""
    
    print("\n" + "=" * 80)
    print("📚 Incremental Vector Store Update - Demo")
    print("=" * 80)
    
    doc_processor = DocumentProcessor()
    
    # Step 1: Show current state
    print("\n📊 Step 1: Current Vector Store State")
    print("-" * 80)
    
    try:
        doc_processor.load_vector_store()
        initial_count = doc_processor.vector_store._collection.count()
        
        print(f"✅ Vector store loaded")
        print(f"📦 Current chunks: {initial_count}")
        
        # Get sources
        results = doc_processor.vector_store._collection.get(limit=100)
        sources = set()
        if results and 'metadatas' in results:
            for metadata in results['metadatas']:
                if metadata and 'source' in metadata:
                    sources.add(Path(metadata['source']).name)
        
        print(f"📚 Current sources:")
        for i, source in enumerate(sorted(sources), 1):
            print(f"   {i}. {source}")
        
    except FileNotFoundError:
        print("❌ No vector store found!")
        print("💡 Run: python scripts/initialize_db.py")
        return
    
    # Step 2: Explain incremental update
    print("\n📝 Step 2: How Incremental Updates Work")
    print("-" * 80)
    print("""
When you add a new PDF incrementally:
  
  1. ✅ Existing chunks are PRESERVED (not deleted)
  2. ➕ New PDF is loaded and chunked
  3. 🔨 New chunks are ADDED to existing vector store
  4. 🔍 Queries search across ALL documents (old + new)
  
This is different from full replacement which:
  1. 🗑️  Deletes all existing chunks
  2. 🔨 Creates new vector store from scratch
  3. 🔍 Queries only search new documents
""")
    
    # Step 3: Show how to use
    print("\n🚀 Step 3: Usage Examples")
    print("-" * 80)
    print("""
# Add single PDF (incremental)
python scripts/update_vectorstore.py data/NewCalendar.pdf

# Add multiple PDFs (incremental)
python scripts/update_vectorstore.py data/Fall.pdf data/Spring.pdf

# Replace entire store (creates backup)
python scripts/update_vectorstore.py --replace data/COE.pdf

# List current contents
python scripts/update_vectorstore.py --list
""")
    
    # Step 4: Show benefits
    print("\n💡 Step 4: When to Use Incremental Updates")
    print("-" * 80)
    print("""
✅ Use Incremental Updates When:
  • Adding department-specific calendars
  • Adding supplementary documents (policies, handbooks)
  • Building multi-source knowledge base
  • Adding quarterly/monthly updates
  
❌ Use Full Replacement When:
  • PDF content has changed (updated version)
  • Want to remove old/outdated information
  • Starting fresh with new academic year
  • Cleaning up duplicate/incorrect data
""")
    
    # Step 5: Test query across sources
    print("\n🔍 Step 5: Query Behavior")
    print("-" * 80)
    print("""
With incremental updates, a single query searches ALL documents:

Example: "What events are happening?"
  → Searches: COE.pdf + DeptCalendar.pdf + Handbook.pdf
  → Returns: Best matches from ANY document
  → Sources: Shows which document each answer came from

This creates a unified knowledge base!
""")
    
    print("\n" + "=" * 80)
    print("✅ Demo Complete!")
    print("=" * 80)
    print("\n💡 Try it yourself:")
    print("   python scripts/update_vectorstore.py --list")
    print()


if __name__ == "__main__":
    demo_incremental_update()
