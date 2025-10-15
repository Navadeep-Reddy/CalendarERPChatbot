#!/usr/bin/env python3
"""
Interactive CLI tool to test the RAG chatbot
Type your queries and get answers in real-time!
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.rag_chain import RAGChatbot

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Define dummy color codes if colorama not available
    class Fore:
        CYAN = RED = GREEN = YELLOW = MAGENTA = WHITE = ''
    class Style:
        RESET_ALL = ''


def print_header():
    """Print welcome header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}🤖  Calendar ERP Chatbot - Interactive Mode")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.YELLOW}Powered by: Google Gemini 2.5 Flash + RAG")
    print(f"{Fore.GREEN}Type your questions about the academic calendar")
    print(f"{Fore.RED}Commands: 'quit', 'exit', 'q' to stop | 'help' for examples\n")


def print_separator():
    """Print a separator line"""
    print(f"{Fore.CYAN}{'-'*70}")


def print_help():
    """Print example queries"""
    print(f"\n{Fore.YELLOW}📚 Example Questions You Can Ask:")
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
        print(f"{Fore.WHITE}  • {ex}")
    print()


def format_sources(source_docs):
    """Format source documents for display"""
    if not source_docs:
        return f"{Fore.RED}No sources found"
    
    sources_text = f"\n{Fore.MAGENTA}📚 Sources ({len(source_docs)} documents):\n"
    for i, doc in enumerate(source_docs, 1):
        content = doc['content'][:250] + "..." if len(doc['content']) > 250 else doc['content']
        metadata = doc.get('metadata', {})
        page = metadata.get('page', 'N/A')
        
        sources_text += f"\n{Fore.YELLOW}[Source {i}] Page {page}:\n"
        sources_text += f"{Fore.WHITE}{content}\n"
    
    return sources_text


def main():
    """Main interactive loop"""
    print_header()
    
    # Initialize chatbot
    try:
        print(f"{Fore.YELLOW}⏳ Loading chatbot from cache...")
        chatbot = RAGChatbot()
        
        # Load from cached vector store (fast!)
        chatbot.doc_processor.load_vector_store()
        chatbot.retriever = chatbot.doc_processor.get_retriever(k=4)
        
        print(f"{Fore.GREEN}✅ Chatbot ready! (using cached vector store)\n")
        print(f"{Fore.CYAN}💡 Type 'help' to see example questions\n")
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Vector store not found!")
        print(f"{Fore.YELLOW}💡 Run this first: python scripts/initialize_db.py")
        print(f"{Fore.YELLOW}💡 Place your COE.pdf in backend/data/ folder")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}❌ Error initializing chatbot: {str(e)}")
        print(f"{Fore.YELLOW}💡 Make sure you've run: python scripts/initialize_db.py")
        sys.exit(1)
    
    # Main loop
    query_count = 0
    while True:
        try:
            # Get user input
            print_separator()
            user_query = input(f"{Fore.CYAN}💬 You: {Style.RESET_ALL}").strip()
            
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'q', 'bye']:
                print(f"\n{Fore.GREEN}👋 Goodbye! Thanks for using the chatbot.")
                print(f"{Fore.CYAN}📊 Total queries answered: {query_count}\n")
                break
            
            # Check for help command
            if user_query.lower() == 'help':
                print_help()
                continue
            
            # Skip empty queries
            if not user_query:
                continue
            
            query_count += 1
            
            # Process query
            print(f"\n{Fore.YELLOW}🤔 Thinking...")
            response = chatbot.query(user_query)
            
            # Display answer
            print(f"\n{Fore.GREEN}🤖 Assistant:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{response['answer']}\n")
            
            # Display source count
            num_sources = len(response.get('sources', []))
            print(f"{Fore.MAGENTA}📚 Answer based on {num_sources} source document(s)")
            
            # Ask if user wants to see sources
            show_sources = input(f"{Fore.CYAN}Show source details? (y/n): {Style.RESET_ALL}").strip().lower()
            if show_sources in ['y', 'yes']:
                print(format_sources(response.get('sources', [])))
            
            print(f"\n{Fore.GREEN}✅ Query #{query_count} completed")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.GREEN}👋 Goodbye! (Interrupted by user)")
            print(f"{Fore.CYAN}📊 Total queries answered: {query_count}\n")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}")
            import traceback
            if '--debug' in sys.argv:
                traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
