# 📋 Quick Reference Card - Calendar ERP Chatbot

## 🚀 Start Both Services

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
pnpm dev
```

**Frontend**: `http://localhost:5174` (or 5173)  
**Backend**: `http://localhost:8000`

---

## 🌐 URLs

| Service  | URL                          | Purpose      |
| -------- | ---------------------------- | ------------ |
| Frontend | http://localhost:5174        | Chat UI      |
| Backend  | http://localhost:8000        | API Server   |
| API Docs | http://localhost:8000/docs   | Swagger UI   |
| Health   | http://localhost:8000/health | Status check |

---

## 📁 Key Files

### Frontend

```
src/
├── App.jsx                    # Main app
├── hooks/useChat.js           # Chat logic
├── services/api.js            # Backend calls
└── components/
    ├── ChatMessage.jsx        # Message display
    ├── ChatInput.jsx          # Input field
    ├── ChatContainer.jsx      # Message list
    ├── Header.jsx             # Top bar
    └── SourceDocument.jsx     # RAG sources
```

### Backend

```
app/
├── main.py                    # FastAPI app
├── rag_chain.py              # RAG implementation
└── document_processor.py     # Vector store
```

---

## 🧪 Testing

### Backend

```bash
cd backend
python test_quick.py          # Quick test
python test_interactive.py    # Interactive CLI
```

### Frontend

1. Open `http://localhost:5174`
2. Check green "Connected" badge
3. Send: "What events are happening?"
4. Verify response with sources

---

## 🔧 Environment Variables

### Backend (.env)

```env
GOOGLE_API_KEY=AIzaSyCDQ6-nXWTEz155oL5Ys04n3pKc4Mt52Vc
LLM_MODEL=gemini-2.5-flash
VECTOR_DB_PATH=/absolute/path/to/vectorstore
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## 🔌 API Endpoints

| Endpoint  | Method | Body               | Response                |
| --------- | ------ | ------------------ | ----------------------- |
| `/health` | GET    | -                  | `{"status": "healthy"}` |
| `/info`   | GET    | -                  | System info             |
| `/chat`   | POST   | `{"query": "..."}` | Answer + sources        |

---

## 📦 Tech Stack

**Frontend**: React 19, Vite 6, Tailwind CSS v4, Shadcn/UI  
**Backend**: FastAPI, Google Gemini 2.5 Flash, ChromaDB, PyPDF

---

## 🐛 Common Issues

### "Disconnected" Badge

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Port in Use

Frontend auto-switches to 5174 if 5173 is busy

### Module Not Found

```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && pnpm install
```

---

## 🔑 Commands Cheat Sheet

```bash
# Frontend
pnpm dev              # Start dev server
pnpm build            # Production build

# Backend
python -m uvicorn app.main:app --reload    # Dev server
python test_quick.py                        # Quick test
python scripts/initialize_db.py             # Reset DB
```

---

## 📚 Documentation

-   `FULLSTACK_QUICKSTART.md` - Complete setup guide
-   `FRONTEND_COMPLETE.md` - Project summary
-   `ARCHITECTURE.md` - Technical details
-   `frontend/FRONTEND_README.md` - Frontend docs

---

## 🎊 Status: ✅ COMPLETE

**Frontend**: Running ✅  
**Backend**: Running ✅  
**Integration**: Connected ✅

**Access**: `http://localhost:5174` 🚀
