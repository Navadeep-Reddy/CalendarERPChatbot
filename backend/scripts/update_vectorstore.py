#!/usr/bin/env python3
"""
Incremental Vector Store Update Script

This script allows you to:
1. Add new PDFs to existing vector store (incremental)
2. Replace entire vector store with new PDFs
3. List current documents in vector store

Usage:
    # Add new PDFs to existing store
    python update_vectorstore.py data/NewCalendar.pdf
    python update_vectorstore.py data/Fall2024.pdf data/Spring2025.pdf
    
    # Replace entire vector store
    python update_vectorstore.py --replace data/COE.pdf
    
    # List current documents
    python update_vectorstore.py --list
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.document_processor import DocumentProcessor
from app.config import settings
import shutil
from datetime import datetime


def list_vectorstore_contents():
    """List all documents currently in the vector store"""
    print("\n📊 Vector Store Contents")
    print("=" * 80)
    
    try:
        doc_processor = DocumentProcessor()
        doc_processor.load_vector_store()
        
        if doc_processor.vector_store is None:
            print("❌ No vector store found!")
            return
        
        # Get collection stats
        collection = doc_processor.vector_store._collection
        total_docs = collection.count()
        
        print(f"\n✅ Vector store loaded from: {settings.vector_db_path}")
        print(f"📦 Total chunks: {total_docs}")
        
        # Get sample documents to show sources
        if total_docs > 0:
            results = collection.get(limit=min(total_docs, 100))
            
            # Extract unique sources from metadata
            sources = set()
            pages = {}
            
            if results and 'metadatas' in results:
                for metadata in results['metadatas']:
                    if metadata and 'source' in metadata:
                        source = metadata['source']
                        sources.add(source)
                        
                        if source not in pages:
                            pages[source] = set()
                        if 'page' in metadata:
                            pages[source].add(metadata['page'])
            
            if sources:
                print("\n📚 Source Documents:")
                for i, source in enumerate(sorted(sources), 1):
                    source_name = Path(source).name
                    page_list = sorted(pages.get(source, []))
                    page_count = len(page_list)
                    
                    print(f"  {i}. {source_name}")
                    if page_count > 0:
                        if page_count <= 5:
                            print(f"     Pages: {page_list}")
                        else:
                            print(f"     Pages: {page_count} pages (from {min(page_list)} to {max(page_list)})")
            
            print("\n✅ Use --add to add more documents or --replace to start fresh")
        
    except FileNotFoundError:
        print("❌ No vector store found!")
        print(f"   Expected location: {settings.vector_db_path}")
        print("\n💡 Tip: Run 'python scripts/initialize_db.py' to create one")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def add_documents_to_vectorstore(pdf_paths: list, use_ocr: bool = False):
    """
    Add new PDFs to existing vector store
    
    Args:
        pdf_paths: List of PDF file paths to add
        use_ocr: If True, use OCR to extract text from image-based PDFs
    """
    print("\n🔄 Adding Documents to Vector Store")
    if use_ocr:
        print("🔍 OCR Mode: Enabled (will extract text from images)")
    print("=" * 80)
    
    doc_processor = DocumentProcessor()
    
    # Try to load existing vector store
    existing_store = False
    try:
        doc_processor.load_vector_store()
        existing_count = doc_processor.vector_store._collection.count()
        print(f"✅ Loaded existing vector store ({existing_count} chunks)")
        existing_store = True
    except FileNotFoundError:
        print("⚠️  No existing vector store found. Creating new one...")
        existing_store = False
    
    all_documents = []
    
    # Load all new PDFs
    print("\n📄 Loading PDF files...")
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            continue
        
        print(f"\n  Processing: {Path(pdf_path).name}")
        try:
            documents = doc_processor.load_pdf_documents(pdf_path, use_ocr=use_ocr)
            all_documents.extend(documents)
            print(f"  ✅ Loaded {len(documents)} chunks")
        except Exception as e:
            print(f"  ❌ Error loading {pdf_path}: {str(e)}")
            continue
    
    if not all_documents:
        print("\n❌ No documents to add!")
        return False
    
    # Add to vector store
    print(f"\n🔨 Processing {len(all_documents)} total chunks...")
    
    try:
        if not existing_store or doc_processor.vector_store is None:
            # Create new vector store
            print("  Creating new vector store...")
            doc_processor.create_vector_store(all_documents)
        else:
            # Add to existing vector store
            print("  Adding to existing vector store...")
            doc_processor.vector_store.add_documents(all_documents)
            doc_processor.vector_store.persist()
        
        # Get final count
        final_count = doc_processor.vector_store._collection.count()
        
        print("\n✅ Vector store updated successfully!")
        print(f"📊 Total chunks in database: {final_count}")
        
        if existing_store:
            print(f"📈 Added: {final_count - existing_count} new chunks")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error updating vector store: {str(e)}")
        return False


def replace_vectorstore(pdf_paths: list, use_ocr: bool = False):
    """
    Replace entire vector store with new PDFs
    
    Args:
        pdf_paths: List of PDF file paths
        use_ocr: If True, use OCR to extract text from image-based PDFs
    """
    print("\n🗑️  Replacing Vector Store")
    if use_ocr:
        print("🔍 OCR Mode: Enabled (will extract text from images)")
    print("=" * 80)
    
    # Backup old vector store
    if os.path.exists(settings.vector_db_path):
        backup_path = f"{settings.vector_db_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"💾 Creating backup: {Path(backup_path).name}")
        try:
            shutil.copytree(settings.vector_db_path, backup_path)
            print("✅ Backup created")
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {str(e)}")
        
        # Delete old vector store
        print(f"🗑️  Deleting old vector store...")
        try:
            shutil.rmtree(settings.vector_db_path)
            print("✅ Old vector store deleted")
        except Exception as e:
            print(f"❌ Error deleting old vector store: {str(e)}")
            return False
    
    # Create new vector store
    return add_documents_to_vectorstore(pdf_paths, use_ocr=use_ocr)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Manage vector store - add or replace PDF documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add new PDF to existing store
  python update_vectorstore.py data/NewCalendar.pdf
  
  # Add image-based PDF using OCR
  python update_vectorstore.py --ocr data/sat.pdf
  
  # Add multiple PDFs
  python update_vectorstore.py data/Fall2024.pdf data/Spring2025.pdf
  
  # Replace entire store with OCR
  python update_vectorstore.py --replace --ocr data/COE.pdf
  
  # List current contents
  python update_vectorstore.py --list
        """
    )
    
    parser.add_argument(
        'pdf_files',
        nargs='*',
        help='PDF files to add to vector store'
    )
    parser.add_argument(
        '--replace',
        action='store_true',
        help='Replace existing vector store instead of adding (creates backup)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List current documents in vector store'
    )
    parser.add_argument(
        '--ocr',
        action='store_true',
        help='Use OCR to extract text from image-based PDFs (requires tesseract-ocr and poppler-utils)'
    )
    
    args = parser.parse_args()
    
    # Handle list command
    if args.list:
        list_vectorstore_contents()
        return
    
    # Validate input
    if not args.pdf_files:
        parser.print_help()
        print("\n❌ Error: Please provide PDF files to process or use --list")
        sys.exit(1)
    
    # Validate all files exist
    missing_files = [f for f in args.pdf_files if not os.path.exists(f)]
    if missing_files:
        print("❌ Error: The following files do not exist:")
        for f in missing_files:
            print(f"  - {f}")
        sys.exit(1)
    
    # Process files
    print("\n" + "=" * 80)
    print("📦 Vector Store Update Tool")
    print("=" * 80)
    
    if args.replace:
        success = replace_vectorstore(args.pdf_files, use_ocr=args.ocr)
    else:
        success = add_documents_to_vectorstore(args.pdf_files, use_ocr=args.ocr)
    
    if success:
        print("\n" + "=" * 80)
        print("✅ Operation completed successfully!")
        print("=" * 80)
        print("\n💡 Next steps:")
        print("   1. Restart the server to load updated vector store")
        print("   2. Test with: python test_quick.py")
        print("   3. List contents: python scripts/update_vectorstore.py --list")
        print()
    else:
        print("\n" + "=" * 80)
        print("❌ Operation failed!")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
