"""
Document processing and vector store management
"""
import json
import os
from typing import List
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from app.config import settings

# Optional OCR dependencies
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class DocumentProcessor:
    """Handles document loading, chunking, and embedding"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
        )
        # Using open-source embeddings (no API key needed)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
    
    def load_pdf_documents(self, pdf_path: str, use_ocr: bool = False) -> List[Document]:
        """
        Load and process PDF document
        
        Args:
            pdf_path: Path to the PDF file
            use_ocr: If True, use OCR to extract text from images in PDF
            
        Returns:
            List of processed documents
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"📄 Loading PDF from: {pdf_path}")
        
        if use_ocr:
            return self._load_pdf_with_ocr(pdf_path)
        else:
            # Load PDF using PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            print(f"✅ Loaded {len(documents)} pages from PDF")
            
            return documents
    
    def _load_pdf_with_ocr(self, pdf_path: str) -> List[Document]:
        """
        Load PDF using OCR for image-based PDFs
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of Document objects with OCR-extracted text
        """
        if not OCR_AVAILABLE:
            raise ImportError(
                "OCR dependencies not installed. "
                "Install with: pip install pdf2image pytesseract pillow\n"
                "Also install system dependency: sudo apt-get install tesseract-ocr poppler-utils"
            )
        
        print(f"🔍 Using OCR to extract text from: {pdf_path}")
        
        try:
            # Convert PDF pages to images
            print("  📸 Converting PDF pages to images...")
            images = convert_from_path(pdf_path)
            print(f"  ✅ Converted {len(images)} pages to images")
            
            documents = []
            
            # Process each page with OCR
            print("  🔤 Extracting text with OCR...")
            for page_num, image in enumerate(images):
                # Extract text using Tesseract
                text = pytesseract.image_to_string(image, lang='eng')
                
                # Clean up extracted text
                text = text.strip()
                
                if text:  # Only add non-empty pages
                    # Create metadata
                    metadata = {
                        'source': pdf_path,
                        'page': page_num,
                        'extraction_method': 'ocr'
                    }
                    
                    # Create document
                    doc = Document(page_content=text, metadata=metadata)
                    documents.append(doc)
                    
                    print(f"     Page {page_num + 1}: Extracted {len(text)} characters")
                else:
                    print(f"     Page {page_num + 1}: No text found")
            
            print(f"✅ OCR completed: {len(documents)} pages with text")
            
            return documents
            
        except Exception as e:
            print(f"❌ OCR Error: {str(e)}")
            print("\n💡 Make sure you have installed:")
            print("   - pip install pdf2image pytesseract pillow")
            print("   - sudo apt-get install tesseract-ocr poppler-utils")
            raise
    
    def load_calendar_data(self, data_path: str) -> List[Document]:
        """Load calendar events from JSON file and convert to documents"""
        documents = []
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Calendar data file not found: {data_path}")
        
        with open(data_path, 'r') as f:
            calendar_data = json.load(f)
        
        for event in calendar_data.get('events', []):
            # Create a rich text representation of the event
            content = self._format_event_content(event)
            
            # Create metadata
            metadata = {
                'event_id': event.get('event_id', ''),
                'title': event.get('title', ''),
                'event_type': event.get('event_type', ''),
                'start_date': event.get('start_date', ''),
                'end_date': event.get('end_date', ''),
                'semester': event.get('semester', ''),
                'year': event.get('year', ''),
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
    
    def _format_event_content(self, event: dict) -> str:
        """Format event data into a readable text format"""
        parts = [
            f"Event: {event.get('title', 'Untitled Event')}",
            f"Type: {event.get('event_type', 'N/A')}",
            f"Date: {event.get('start_date', 'N/A')}",
        ]
        
        if event.get('end_date'):
            parts.append(f"End Date: {event.get('end_date')}")
        
        if event.get('description'):
            parts.append(f"Description: {event.get('description')}")
        
        if event.get('semester'):
            parts.append(f"Semester: {event.get('semester')}")
        
        if event.get('year'):
            parts.append(f"Academic Year: {event.get('year')}")
        
        return "\n".join(parts)
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create and persist vector store from documents"""
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create vector store
        os.makedirs(settings.vector_db_path, exist_ok=True)
        
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=settings.vector_db_path
        )
        
        return self.vector_store
    
    def load_vector_store(self) -> Chroma:
        """Load existing vector store"""
        if not os.path.exists(settings.vector_db_path):
            raise FileNotFoundError(
                f"Vector store not found at {settings.vector_db_path}. "
                "Please initialize the vector store first."
            )
        
        self.vector_store = Chroma(
            persist_directory=settings.vector_db_path,
            embedding_function=self.embeddings
        )
        
        return self.vector_store
    
    def get_retriever(self, k: int = 4):
        """Get a retriever from the vector store"""
        if self.vector_store is None:
            try:
                self.load_vector_store()
            except FileNotFoundError:
                raise ValueError("Vector store not initialized. Please load calendar data first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
