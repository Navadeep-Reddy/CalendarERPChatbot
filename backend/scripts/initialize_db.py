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
    
    data_path = os.path.join(
        os.path.dirname(__file__),
        '../data/calendar_events.json'
    )
    
    try:
        chatbot = RAGChatbot()
        chatbot.initialize_vector_store(data_path)
        print("✅ Vector store initialized successfully!")
        print(f"   Data loaded from: {data_path}")
        print(f"   Vector store location: {chatbot.doc_processor.vector_store._persist_directory}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
