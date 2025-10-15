"""
FastAPI application main file
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from app.models import ChatRequest, ChatResponse, HealthResponse, SourceDocument
from app.config import settings
from app.rag_chain import RAGChatbot
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="RAG-based chatbot for academic calendar queries"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG chatbot
chatbot = None

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot on startup using cached vector store"""
    global chatbot
    try:
        print("🚀 Initializing RAG Chatbot...")
        chatbot = RAGChatbot()
        
        # Check if vector store cache exists
        if os.path.exists(settings.vector_db_path):
            print(f"📂 Loading cached vector store from: {settings.vector_db_path}")
            chatbot.doc_processor.load_vector_store()
            chatbot.retriever = chatbot.doc_processor.get_retriever(k=4)
            print("✅ RAG Chatbot initialized successfully (from cache)")
        else:
            print(f"⚠️  Vector store not found at: {settings.vector_db_path}")
            print("⚠️  Please run: python scripts/initialize_db.py")
            print("⚠️  Chatbot will not be available until initialized")
            chatbot = None
            
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize chatbot - {str(e)}")
        print("   Vector store may need to be initialized. Use /initialize endpoint.")
        chatbot = None


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    # return HealthResponse(
    #     status="healthy",
    #     version=settings.app_version,
    #     timestamp=datetime.now().isoformat()
    # )

    return FileResponse("static/chatbot.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.now().isoformat()
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat query about the academic calendar
    
    Args:
        request: ChatRequest with user query
        
    Returns:
        ChatResponse with answer and source documents
    """
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot not initialized. Please initialize the vector store first."
        )
    
    try:
        # Process query
        result = chatbot.query(request.query)
        
        # Format sources
        sources = [
            SourceDocument(
                content=src['content'],
                metadata=src['metadata']
            )
            for src in result.get('sources', [])
        ]
        
        return ChatResponse(
            answer=result.get('answer', 'Unable to generate answer'),
            sources=sources,
            session_id=request.session_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.post("/initialize")
async def initialize_vector_store(data_path: str = "./data/calendar_events.json"):
    """
    Initialize the vector store with calendar data
    
    Args:
        data_path: Path to the calendar events JSON file
        
    Returns:
        Success message
    """
    global chatbot
    
    try:
        if chatbot is None:
            chatbot = RAGChatbot()
        
        chatbot.initialize_vector_store(data_path)
        chatbot.initialize_chain()
        
        return {
            "status": "success",
            "message": f"Vector store initialized successfully from {data_path}"
        }
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error initializing vector store: {str(e)}"
        )


@app.get("/info")
async def get_info():
    """Get information about the chatbot configuration"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "llm_model": settings.llm_model,
        "vector_db_path": settings.vector_db_path,
        "chatbot_initialized": chatbot is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
