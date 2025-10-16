# Quick Start Guide

## 🎯 What You Have

A complete RAG-based chatbot backend that can answer questions about your academic calendar using:

-   **FastAPI** for the REST API
-   **LangChain** for RAG implementation
-   **ChromaDB** for vector storage
-   **Google Gemini 2.0 Flash** for answer generation (FREE!)
-   **Docker** for containerization

## 🚀 Getting Started (Choose One Method)

### Method 1: Local Development (Recommended for Development)

```bash
cd backend

# 1. Run the setup script (only once)
./setup.sh

# 2. Add your Google Gemini API key to .env file
# Edit .env and replace: GOOGLE_API_KEY=your_google_api_key_here
# Get free API key from: https://aistudio.google.com/app/apikey

# 3. Start the server
./run.sh
```

### Method 2: Docker (Recommended for Production)

```bash
cd backend

# 1. Create .env file
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
# Get free API key from: https://aistudio.google.com/app/apikey

# 2. Start with Docker Compose
docker-compose up -d

# 3. Initialize the database (first time only)
docker-compose exec calendar-chatbot python scripts/initialize_db.py

# Check logs
docker-compose logs -f
```

## 📝 Testing the API

Once running, visit: http://localhost:8000/docs

### Test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "When are the mid-term exams?"}'
```

### Example Response:

```json
{
    "answer": "The mid-term examinations are scheduled from October 14-18, 2024 for Fall semester.",
    "sources": [
        {
            "content": "Event: Mid-term Examinations\nType: examination\nDate: 2024-10-14\nEnd Date: 2024-10-18...",
            "metadata": {
                "event_id": "evt_003",
                "title": "Mid-term Examinations",
                "event_type": "examination"
            }
        }
    ],
    "session_id": null
}
```

## 🎓 Sample Questions to Try

-   "When does the Fall semester begin?"
-   "What holidays are scheduled?"
-   "When are the final exams?"
-   "Tell me about Spring break"
-   "What events are in November?"
-   "When is graduation?"

## 📂 Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app & endpoints
│   ├── models.py         # Request/response models
│   ├── config.py         # Configuration
│   ├── document_processor.py  # Vector store management
│   └── rag_chain.py      # RAG implementation
├── data/
│   ├── calendar_events.json  # Your calendar data
│   └── vectorstore/      # Generated embeddings
├── scripts/
│   └── initialize_db.py  # DB initialization
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env                  # Your API keys (create this!)
```

## 🔧 Customization

### Add Your Own Calendar Data

Edit `data/calendar_events.json`:

```json
{
    "events": [
        {
            "event_id": "evt_001",
            "title": "Your Event",
            "description": "Event description",
            "start_date": "2024-09-01",
            "end_date": null,
            "event_type": "examination",
            "semester": "Fall",
            "year": "2024-2025"
        }
    ]
}
```

Then re-initialize:

```bash
python scripts/initialize_db.py
```

### Change LLM Model

Edit `.env`:

```env
LLM_MODEL=gemini-2.0-flash-exp  # Default free model
# Other options: gemini-1.5-flash, gemini-1.5-pro
```

## 🐛 Troubleshooting

### "Import could not be resolved" errors

These are just linting warnings. Run `pip install -r requirements.txt` to install packages.

### "Vector store not initialized"

Run: `python scripts/initialize_db.py`

### "Google API key not found"

Make sure you've created `.env` and added your API key.
Get your free key from: https://aistudio.google.com/app/apikey

### Permission errors in Docker

Run: `chmod -R 755 data/vectorstore`

## 📊 API Endpoints

| Endpoint      | Method | Description             |
| ------------- | ------ | ----------------------- |
| `/`           | GET    | Health check            |
| `/health`     | GET    | Detailed health status  |
| `/chat`       | POST   | Ask questions           |
| `/initialize` | POST   | Initialize vector store |
| `/info`       | GET    | Get app info            |
| `/docs`       | GET    | Interactive API docs    |

## 🔐 Environment Variables

Required:

-   `GOOGLE_API_KEY` - Your Google Gemini API key (FREE from https://aistudio.google.com/app/apikey)

Optional:

-   `LLM_MODEL` - Model to use (default: gemini-2.0-flash-exp)
-   `LLM_TEMPERATURE` - Response randomness (default: 0.7)
-   `MAX_TOKENS` - Max response length (default: 500)
-   `VECTOR_DB_PATH` - Storage location (default: ./data/vectorstore)

## 📚 Next Steps

1. ✅ Test the API with sample queries
2. ✅ Add your institution's calendar data
3. ✅ Customize the prompt template if needed
4. 🔲 Add authentication for production
5. 🔲 Create a frontend interface
6. 🔲 Deploy to production

## 🎉 You're All Set!

Your chatbot is ready to answer calendar questions. Happy coding! 🚀
