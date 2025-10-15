#!/usr/bin/env python3
"""
Simple interactive CLI tool to test the RAG chatbot (no dependencies)
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.rag_chain import RAGChatbot


def main():
    """Main interactive loop"""
    print("\n" + "="*70)
    print("🤖  Calendar ERP Chatbot - Interactive Mode")
    print("="*70)
    print("Powered by: Google Gemini 2.5 Flash + RAG")
    print("Type your questions about the academic calendar")
    print("Commands: 'quit', 'exit', 'q' to stop | 'help' for examples\n")
    
    # Initialize chatbot
    try:
        print("⏳ Loading chatbot from cache...")
        chatbot = RAGChatbot()
        
        # Load from cached vector store (fast!)
        chatbot.doc_processor.load_vector_store()
        chatbot.retriever = chatbot.doc_processor.get_retriever(k=4)
        
        print("✅ Chatbot ready! (using cached vector store)\n")
        print("💡 Type 'help' to see example questions\n")
    except FileNotFoundError:
        print("❌ Vector store not found!")
        print("💡 Run this first: python scripts/initialize_db.py")
        print("💡 Place your COE.pdf in backend/data/ folder")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error initializing chatbot: {str(e)}")
        print("💡 Make sure you've run: python scripts/initialize_db.py")
        sys.exit(1)
    
    # Main loop
    query_count = 0
    while True:
        try:
            # Get user input
            print("-"*70)
            user_query = input("💬 You: ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'q', 'bye']:
                print(f"\n👋 Goodbye! Thanks for using the chatbot.")
                print(f"📊 Total queries answered: {query_count}\n")
                break
            
            # Check for help command
            if user_query.lower() == 'help':
                print("\n📚 Example Questions You Can Ask:")
                examples = [
                    "When does the fall semester start?",
                    "When are the midterm exams?",
                    "What holidays are in November?",
                    "Tell me about spring break",
                    "When is the last day to drop classes?",
                    "When does registration open?",
                    "What's the academic calendar for Fall 2024?",
                ]
                for ex in examples:
                    print(f"  • {ex}")
                print()
                continue
            
            # Skip empty queries
            if not user_query:
                continue
            
            query_count += 1
            
            # Process query
            print("\n🤔 Thinking...")
            response = chatbot.query(user_query)
            
            # Display answer
            print(f"\n🤖 Assistant:")
            print(response['answer'])
            print()
            
            # Display sources summary
            num_sources = len(response.get('sources', []))
            print(f"📚 Answer based on {num_sources} source document(s)")
            
            # Ask if user wants to see sources
            show_sources = input("\nShow source details? (y/n): ").strip().lower()
            if show_sources in ['y', 'yes']:
                print(f"\n📄 Source Documents:\n")
                for i, doc in enumerate(response.get('sources', []), 1):
                    print(f"[Source {i}]")
                    metadata = doc.get('metadata', {})
                    print(f"Page: {metadata.get('page', 'N/A')}")
                    content = doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content']
                    print(f"Content: {content}")
                    print()
            
            print(f"✅ Query #{query_count} completed")
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye! (Interrupted by user)")
            print(f"📊 Total queries answered: {query_count}\n")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            if '--debug' in sys.argv:
                traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
