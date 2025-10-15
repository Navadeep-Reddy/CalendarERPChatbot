#!/usr/bin/env python3
"""
Quick test script to verify the chatbot works with PDF data
Uses cached vector store - no re-chunking needed!
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.rag_chain import RAGChatbot

def main():
    print("\n" + "="*70)
    print("🧪 Testing RAG Chatbot with PDF Data")
    print("="*70)
    
    try:
        print("\n⏳ Loading chatbot from cache...")
        chatbot = RAGChatbot()
        
        # Load existing vector store instead of re-chunking
        chatbot.doc_processor.load_vector_store()
        chatbot.retriever = chatbot.doc_processor.get_retriever(k=4)
        print("✅ Chatbot ready! (using cached vector store)")
        
        # Test queries
        test_queries = [
            "What is this document about?",
            "When does the fall semester start?",
            "Are there any exams mentioned?",
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*70}")
            print(f"📝 Test Query {i}: {query}")
            print("-"*70)
            
            response = chatbot.query(query)
            
            print(f"\n🤖 Answer:")
            print(response['answer'])
            
            print(f"\n📚 Sources: {len(response.get('sources', []))} documents")
            
        print(f"\n{'='*70}")
        print("✅ All tests completed successfully!")
        print("="*70)
        
        print(f"\n💡 To test interactively, run:")
        print(f"   python test_interactive.py")
        
        print(f"\n📌 Note: Vector store loaded from cache (fast!)")
        print(f"   To re-chunk PDF, run: python scripts/initialize_db.py")
        
    except FileNotFoundError as e:
        print(f"\n❌ Vector store not found!")
        print(f"   Run this first: python scripts/initialize_db.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
