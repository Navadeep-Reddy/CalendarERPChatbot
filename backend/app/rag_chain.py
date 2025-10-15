"""
RAG chain implementation using Google GenAI SDK
"""
from typing import Dict, List
from google import genai
from app.config import settings
from app.document_processor import DocumentProcessor


class RAGChatbot:
    """RAG-based chatbot for calendar queries"""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.client = None
        self.retriever = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Google GenAI client"""
        if not settings.google_api_key:
            raise ValueError(
                "Google API key not found. Please set GOOGLE_API_KEY in your .env file"
            )
        
        self.client = genai.Client(api_key=settings.google_api_key)
    
    def initialize_chain(self):
        """Initialize the RAG retriever"""
        # Get retriever
        self.retriever = self.doc_processor.get_retriever(k=4)
        return self.retriever
    
    def query(self, question: str) -> Dict:
        """
        Process a user query and return the answer with sources
        
        Args:
            question: User's question about the calendar
            
        Returns:
            Dictionary with 'answer' and 'source_documents'
        """
        if self.retriever is None:
            self.initialize_chain()
        
        try:
            # Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(question)
            
            # Build context from retrieved documents
            context_parts = []
            for i, doc in enumerate(docs, 1):
                context_parts.append(f"Document {i}:\n{doc.page_content}")
            
            context = "\n\n".join(context_parts)
            
            # Create the prompt
            prompt = f"""You are a helpful assistant for an academic institution's ERP system. 
Your role is to answer questions about the academic calendar, including events, examinations, 
holidays, and important dates.

Use the following pieces of context to answer the question at the end. If you don't know the 
answer based on the context provided, just say that you don't have that information in the 
calendar. Don't try to make up an answer.

Context:
{context}

Question: {question}

Helpful Answer:"""
            
            # Generate response using Google GenAI
            response = self.client.models.generate_content(
                model=settings.llm_model,
                contents=prompt
            )
            
            # Format source documents
            sources = []
            for doc in docs:
                sources.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata
                })
            
            return {
                'answer': response.text,
                'sources': sources
            }
        except Exception as e:
            return {
                'answer': f"Error processing query: {str(e)}",
                'sources': []
            }
    
    def initialize_vector_store(self, data_path: str):
        """Initialize vector store with calendar data"""
        # Check if it's a PDF or JSON file
        if data_path.endswith('.pdf'):
            documents = self.doc_processor.load_pdf_documents(data_path)
        else:
            documents = self.doc_processor.load_calendar_data(data_path)
        
        self.doc_processor.create_vector_store(documents)
        print(f"Vector store initialized with {len(documents)} documents")
