"""
Utility script to initialize the vector store with calendar data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag_chain import RAGChatbot


def main():
    """Initialize vector store with calendar data"""
    print("🚀 Initializing vector store with calendar data...")
    
    # Path to COE.pdf (or fallback to JSON)
    pdf_path = os.path.join(
        os.path.dirname(__file__),
        '../data/COE.pdf'
    )
    
    json_path = os.path.join(
        os.path.dirname(__file__),
        '../data/calendar_events.json'
    )
    
    # Use PDF if it exists, otherwise fallback to JSON
    if os.path.exists(pdf_path):
        data_path = pdf_path
        print(f"📄 Using PDF file: {pdf_path}")
    elif os.path.exists(json_path):
        data_path = json_path
        print(f"📋 Using JSON file: {json_path}")
    else:
        print(f"❌ Error: No data file found!")
        print(f"   Expected PDF at: {pdf_path}")
        print(f"   Or JSON at: {json_path}")
        sys.exit(1)
    
    try:
        chatbot = RAGChatbot()
        chatbot.initialize_vector_store(data_path)
        print("✅ Vector store initialized successfully!")
        print(f"   Data loaded from: {data_path}")
        print(f"   Vector store location: {chatbot.doc_processor.vector_store._persist_directory}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
