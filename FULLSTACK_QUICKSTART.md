# 🚀 Full-Stack ERP Calendar Chatbot - Quick Start

## 🎯 What We Built

A complete **RAG-powered chatbot** for the ERP Calendar system with:

-   ✅ **Backend**: FastAPI + Google Gemini 2.5 Flash + ChromaDB
-   ✅ **Frontend**: React 19 + Vite + Shadcn/UI + Tailwind CSS v4
-   ✅ **Professional UI**: Modern chat interface with source document display
-   ✅ **Optimized Performance**: Cached vector store (3s startup)

---

## ⚡ Quick Start (Both Services)

### Option 1: Automated Start

```bash
# From project root
./quick_start.sh
```

This will:

1. Start the backend on `http://localhost:8000`
2. Start the frontend on `http://localhost:5173` (or 5174 if 5173 is busy)

### Option 2: Manual Start

#### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # or: conda activate <your-env>
python -m uvicorn app.main:app --reload
```

Backend will be at: `http://localhost:8000`

#### Terminal 2 - Frontend

```bash
cd frontend
pnpm dev
```

Frontend will be at: `http://localhost:5174`

---

## 🌐 Access the Application

**Open your browser and go to:**

```
http://localhost:5174
```

You should see the **ERP Calendar Assistant** interface!

---

## 🎨 Using the Chatbot

### Example Queries

Try asking:

-   "What events are happening this week?"
-   "Tell me about upcoming workshops"
-   "What activities are available for students?"
-   "When is the next cultural event?"
-   "Show me sports events"

### Features to Explore

1. **Chat Interface**

    - Type your question in the input box
    - Press Enter or click Send
    - See bot response with source documents

2. **Source Documents**

    - Each bot response shows sources from the PDF
    - Click to see page numbers and content snippets

3. **Connection Status**

    - Green badge = Connected to backend
    - Red badge = Disconnected (check if backend is running)

4. **Clear Chat**
    - Click "Clear" button in header to start fresh

---

## 🔧 Project Structure

```
CalendarERPChatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── rag_chain.py         # RAG implementation
│   │   ├── document_processor.py # PDF & vector store
│   │   └── config.py            # Settings
│   ├── data/
│   │   ├── COE.pdf              # Source document
│   │   └── vectorstore/         # Cached embeddings
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatMessage.jsx
    │   │   ├── ChatInput.jsx
    │   │   ├── ChatContainer.jsx
    │   │   ├── Header.jsx
    │   │   └── SourceDocument.jsx
    │   ├── hooks/
    │   │   └── useChat.js
    │   ├── services/
    │   │   └── api.js
    │   └── App.jsx
    └── package.json
```

---

## 🛠️ Tech Stack

### Backend

-   **Framework**: FastAPI 0.119.0
-   **LLM**: Google Gemini 2.5 Flash (free tier)
-   **Vector DB**: ChromaDB 1.1.1
-   **Embeddings**: HuggingFace all-MiniLM-L6-v2
-   **PDF Processing**: PyPDF 6.1.1
-   **Python**: 3.13

### Frontend

-   **Framework**: React 19.0.0
-   **Build Tool**: Vite 6.1.0
-   **UI Library**: Shadcn/UI
-   **Styling**: Tailwind CSS v4.0.6
-   **Icons**: Lucide React 0.475.0
-   **Package Manager**: pnpm

---

## 📊 API Endpoints

| Endpoint      | Method | Description               |
| ------------- | ------ | ------------------------- |
| `/health`     | GET    | Health check              |
| `/info`       | GET    | System information        |
| `/chat`       | POST   | Send message to chatbot   |
| `/initialize` | POST   | Reinitialize vector store |
| `/docs`       | GET    | Interactive API docs      |

**Access API Docs**: `http://localhost:8000/docs`

---

## ⚙️ Configuration

### Backend (.env)

```env
GOOGLE_API_KEY=AIzaSyCDQ6-nXWTEz155oL5Ys04n3pKc4Mt52Vc
LLM_MODEL=gemini-2.5-flash
VECTOR_DB_PATH=/home/navadeep/Documents/Projects/CalendarERPChatbot/backend/data/vectorstore
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Frontend Can't Connect to Backend

**Symptom**: Red "Disconnected" badge in header

**Solutions**:

1. Check if backend is running:

    ```bash
    curl http://localhost:8000/health
    ```

2. Start backend if not running:

    ```bash
    cd backend
    python -m uvicorn app.main:app --reload
    ```

3. Check CORS settings in `backend/app/main.py`

### Backend Errors

**Symptom**: 500 errors or crashes

**Solutions**:

1. Check if vector store exists:

    ```bash
    ls backend/data/vectorstore/
    ```

2. Reinitialize if needed:

    ```bash
    cd backend
    python scripts/initialize_db.py
    ```

3. Check logs in terminal

### Frontend Build Errors

**Solutions**:

1. Clear node_modules:

    ```bash
    cd frontend
    rm -rf node_modules pnpm-lock.yaml
    pnpm install
    ```

2. Check Node.js version (needs 18+):
    ```bash
    node --version
    ```

---

## 🧪 Testing

### Test Backend

```bash
cd backend

# Quick automated test
python test_quick.py

# Interactive CLI
python test_interactive.py
```

### Test Frontend

1. Open `http://localhost:5174` in browser
2. Check browser console for errors (F12)
3. Try sending a test message

---

## 📈 Performance

-   **Backend startup**: ~3 seconds (with cached vector store)
-   **First message**: ~2-5 seconds (model inference)
-   **Subsequent messages**: ~2-3 seconds
-   **Frontend load**: <1 second

---

## 🎯 Development Workflow

### Backend Changes

1. Edit files in `backend/app/`
2. FastAPI auto-reloads (with `--reload` flag)
3. Test with `curl` or frontend

### Frontend Changes

1. Edit files in `frontend/src/`
2. Vite HMR updates browser instantly
3. Check browser console for errors

---

## 📦 Adding Features

### Add New Shadcn Component

```bash
cd frontend
pnpm dlx shadcn@latest add <component>
```

### Add New Backend Endpoint

1. Add route in `backend/app/main.py`
2. Add function in `backend/app/api.js` (frontend)
3. Use in React components

---

## 🚀 Deployment

### Backend

-   Deploy to: Railway, Render, or DigitalOcean
-   Set environment variables
-   Use production ASGI server (uvicorn workers)

### Frontend

-   Deploy to: Vercel, Netlify, or Cloudflare Pages
-   Set `VITE_API_URL` to production backend
-   Run `pnpm build` to create `dist/`

---

## 📚 Documentation

-   **Backend Setup**: `backend/SETUP_COMPLETE.md`
-   **Performance Guide**: `OPTIMIZATION_COMPLETE.md`
-   **Chunking Guide**: `CHUNKING_GUIDE.md`
-   **Frontend Docs**: `frontend/FRONTEND_README.md`
-   **Git Guide**: `GITIGNORE_GUIDE.md`

---

## ✅ System Status Check

Run these commands to verify everything is working:

```bash
# Backend health
curl http://localhost:8000/health

# Backend info
curl http://localhost:8000/info

# Frontend accessible
curl http://localhost:5174

# Test chat (from backend)
cd backend && python test_quick.py
```

Expected outputs:

-   Backend health: `{"status": "healthy"}`
-   Backend info: JSON with model and DB info
-   Frontend: HTML response
-   Test chat: 3 successful Q&A pairs

---

## 🎉 You're Ready!

The ERP Calendar Chatbot is now fully operational with:

-   ✅ Professional React frontend
-   ✅ Optimized FastAPI backend
-   ✅ RAG-powered responses
-   ✅ Source document display
-   ✅ Real-time connection status
-   ✅ Modern UI/UX

**Next Steps**:

1. Open `http://localhost:5174` in your browser
2. Start chatting with the assistant
3. Explore the source documents
4. Customize the UI to your needs
5. Deploy to production!

---

**Need Help?** Check the documentation files or review the backend logs and browser console for detailed error messages.
