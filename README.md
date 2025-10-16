# Calendar ERP Chatbot

A RAG (Retrieval-Augmented Generation) based chatbot backend for answering queries about academic calendar events using FastAPI and LangChain.

## Features

-   🤖 **RAG-based AI Chatbot** - Uses retrieval-augmented generation for accurate calendar information
-   📅 **Academic Calendar Management** - Handles events, exams, holidays, and important dates
-   ⚡ **FastAPI Backend** - High-performance async API
-   🔍 **Vector Search** - ChromaDB for efficient semantic search
-   🐳 **Docker Support** - Easy containerized deployment
-   📝 **OpenAPI Documentation** - Auto-generated API docs

## Architecture

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       v
┌─────────────────────────────────┐
│      FastAPI Endpoint           │
│      /chat                      │
└──────────┬──────────────────────┘
           │
           v
┌─────────────────────────────────┐
│     RAG Chain (LangChain)       │
│  ┌────────────────────────┐    │
│  │  1. Query Embedding    │    │
│  └────────────────────────┘    │
│  ┌────────────────────────┐    │
│  │  2. Vector Search      │    │
│  │     (ChromaDB)         │    │
│  └────────────────────────┘    │
│  ┌────────────────────────┐    │
│  │  3. Context Retrieval  │    │
│  └────────────────────────┘    │
│  ┌────────────────────────┐    │
│  │  4. LLM Generation     │    │
│  │     (Google Gemini)    │    │
│  └────────────────────────┘    │
└──────────┬──────────────────────┘
           │
           v
┌─────────────────────────────────┐
│   Response with Sources         │
└─────────────────────────────────┘
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration management
│   ├── document_processor.py # Document loading & vector store
│   └── rag_chain.py         # RAG chain implementation
├── data/
│   ├── calendar_events.json # Sample calendar data
│   └── vectorstore/         # ChromaDB storage (generated)
├── scripts/
│   └── initialize_db.py     # Vector store initialization
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Quick Start

### Local Development Setup

#### 1. Prerequisites

-   Python 3.11+
-   pip
-   Google Gemini API key (free from Google AI Studio)

#### 2. Clone and Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Google Gemini API key
nano .env  # or use your preferred editor
```

Update `.env`:

```env
GOOGLE_API_KEY=your-actual-api-key-here
```

Get your free API key from: https://aistudio.google.com/app/apikey

#### 4. Initialize Vector Store

```bash
# Initialize the vector database with calendar data
python scripts/initialize_db.py
```

#### 5. Run the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

-   **API**: http://localhost:8000
-   **Interactive Docs**: http://localhost:8000/docs
-   **Alternative Docs**: http://localhost:8000/redoc

### Docker Setup

#### Option 1: Docker Compose (Recommended)

```bash
# Create .env file with your API key
cp .env.example .env
# Edit .env to add your GOOGLE_API_KEY

# Build and run
docker-compose up -d

# Initialize vector store (first time only)
docker-compose exec calendar-chatbot python scripts/initialize_db.py

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

#### Option 2: Docker Only

```bash
# Build image
docker build -t calendar-chatbot .

# Run container
docker run -d \
  --name calendar-chatbot \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your-api-key-here \
  -v $(pwd)/data/vectorstore:/app/data/vectorstore \
  calendar-chatbot

# Initialize vector store
docker exec calendar-chatbot python scripts/initialize_db.py
```

## API Usage

### 1. Health Check

```bash
curl http://localhost:8000/health
```

### 2. Initialize Vector Store (via API)

```bash
curl -X POST "http://localhost:8000/initialize" \
  -H "Content-Type: application/json" \
  -d '{"data_path": "./data/calendar_events.json"}'
```

### 3. Chat Query

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "When are the mid-term exams scheduled?",
    "session_id": "user123"
  }'
```

Response:

```json
{
    "answer": "The mid-term examinations are scheduled from October 14-18, 2024 for Fall semester and March 17-21, 2025 for Spring semester.",
    "sources": [
        {
            "content": "Event: Mid-term Examinations\nType: examination\nDate: 2024-10-14...",
            "metadata": {
                "event_id": "evt_003",
                "title": "Mid-term Examinations",
                "event_type": "examination",
                "semester": "Fall"
            }
        }
    ],
    "session_id": "user123"
}
```

### 4. Get Application Info

```bash
curl http://localhost:8000/info
```

## Example Queries

Try these sample questions:

-   "When does the Fall semester begin?"
-   "What holidays are in the Spring semester?"
-   "When are the final exams?"
-   "Tell me about the Spring break"
-   "When is the registration deadline?"
-   "What events are scheduled in November?"

## Customization

### Adding Your Own Calendar Data

1. Edit `data/calendar_events.json` with your institution's calendar
2. Follow the JSON structure for events
3. Re-initialize the vector store:

```bash
python scripts/initialize_db.py
# Or via API: POST /initialize
```

### Using Different LLM Providers

The chatbot uses Google Gemini by default. You can switch to other providers:

```python
# For OpenAI GPT
from langchain_openai import ChatOpenAI

# For Azure OpenAI
from langchain_openai import AzureChatOpenAI

# For Anthropic Claude
from langchain_anthropic import ChatAnthropic

# For local models (Ollama)
from langchain_community.llms import Ollama
```

### Customizing the Prompt

Edit the prompt template in `app/rag_chain.py`:

```python
template = """Your custom system prompt here...

Context:
{context}

Question: {question}

Answer:"""
```

## Configuration Options

All settings can be configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | (required) |
| `LLM_MODEL` | LLM model to use | `gemini-2.0-flash-exp` |
| `LLM_TEMPERATURE` | Generation temperature | `0.7` |
| `MAX_TOKENS`      | Max tokens in response | `500`                |
| `VECTOR_DB_PATH`  | Vector store location  | `./data/vectorstore` |
| `CHUNK_SIZE`      | Document chunk size    | `1000`               |
| `CHUNK_OVERLAP`   | Chunk overlap          | `200`                |
| `API_HOST`        | API host               | `0.0.0.0`            |
| `API_PORT`        | API port               | `8000`               |

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov httpx

# Run tests (when implemented)
pytest tests/
```

### Code Formatting

```bash
# Install formatters
pip install black isort

# Format code
black app/
isort app/
```

## Troubleshooting

### Vector Store Not Initialized

**Error**: "Vector store not initialized"

**Solution**: Run the initialization script:

```bash
python scripts/initialize_db.py
```

### Import Errors

**Error**: "Import 'langchain' could not be resolved"

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

### OpenAI API Errors

**Error**: "OpenAI API key not found"

**Solution**: Set your API key in `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
```

### Docker Volume Permission Issues

**Error**: Permission denied on vector store

**Solution**: Ensure proper permissions:

```bash
chmod -R 755 data/vectorstore
```

## Performance Optimization

-   **Caching**: Enable response caching for common queries
-   **Batch Processing**: Process multiple queries in parallel
-   **Vector Store**: Use FAISS for larger datasets
-   **Model Selection**: Use `gpt-3.5-turbo` for faster responses, `gpt-4` for accuracy

## Security Considerations

-   Keep your `.env` file secure and never commit it
-   Use environment-specific API keys
-   Implement rate limiting in production
-   Add authentication middleware for production deployments
-   Validate and sanitize all user inputs

## Production Deployment

### Recommended Setup

1. Use a reverse proxy (nginx)
2. Enable HTTPS/TLS
3. Implement authentication (JWT, OAuth)
4. Add rate limiting
5. Set up monitoring and logging
6. Use managed vector store (Pinecone, Weaviate)
7. Configure CORS properly

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - feel free to use this project for your institution.

## Support

For issues and questions:

-   Open an issue on GitHub
-   Check the `/docs` endpoint for API documentation

## Roadmap

-   [ ] Add conversation history support
-   [ ] Implement user authentication
-   [ ] Add support for multiple file formats (PDF, Excel)
-   [ ] Create a frontend interface
-   [ ] Add analytics and usage tracking
-   [ ] Support for multiple languages
-   [ ] Integration with ERP systems

---

Built with ❤️ using FastAPI and LangChain
