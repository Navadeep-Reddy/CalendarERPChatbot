# 📚 PDF Chunking & Vector Store Guide

## 🔍 Understanding Chunking

### What is Chunking?

Chunking is the process of:

1. **Loading** the PDF file
2. **Extracting** text from all pages
3. **Splitting** text into smaller pieces (chunks)
4. **Embedding** each chunk into vectors
5. **Storing** vectors in ChromaDB

**⏱️ Time:** Takes ~30-60 seconds for a typical PDF

---

## 🚀 When Does Chunking Happen?

### ✅ **Only When You Run:**

```bash
python scripts/initialize_db.py
```

This is the **ONLY** command that re-chunks the PDF.

**Or via API:**

```bash
curl -X POST http://localhost:8000/initialize \
  -H "Content-Type: application/json" \
  -d '{"file_path": "data/COE.pdf"}'
```

---

## 📦 What Gets Cached?

After running `initialize_db.py`, a vector store is saved to:

```
backend/data/vectorstore/
├── chroma.sqlite3      # Vector database
└── [other index files]
```

**This cache persists between runs!**

---

## 🏃 Fast Operations (Use Cache)

These commands **DO NOT** re-chunk - they load from cache:

### ✅ Start Server

```bash
./start.sh
# or
uvicorn app.main:app --reload
```

**Speed:** ~2-3 seconds (loads cached vectors)

### ✅ Run Tests

```bash
python test_quick.py
python test_interactive.py
python test_simple.py
```

**Speed:** ~2-3 seconds each (loads cached vectors)

### ✅ API Calls

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "When are exams?"}'
```

**Speed:** <1 second (uses already-loaded cache)

---

## 🔄 When to Re-Chunk

You **only** need to re-chunk when:

1. ✏️ **PDF content changes** - You updated COE.pdf
2. 🔧 **Chunk settings change** - Modified chunk_size or overlap
3. 🗑️ **Cache corrupted** - Deleted vectorstore folder
4. 🆕 **Different PDF** - Switching to new document

---

## 📊 Performance Comparison

| Operation             | Re-chunks? | Time | Uses Cache?       |
| --------------------- | ---------- | ---- | ----------------- |
| `initialize_db.py`    | ✅ YES     | ~60s | ❌ Creates new    |
| `./start.sh`          | ❌ NO      | ~3s  | ✅ Loads existing |
| `test_quick.py`       | ❌ NO      | ~3s  | ✅ Loads existing |
| `test_interactive.py` | ❌ NO      | ~3s  | ✅ Loads existing |
| `test_simple.py`      | ❌ NO      | ~3s  | ✅ Loads existing |
| API `/chat`           | ❌ NO      | <1s  | ✅ Uses loaded    |
| API `/initialize`     | ✅ YES     | ~60s | ❌ Creates new    |

---

## 🎯 Best Practices

### ✅ **DO:**

-   Run `initialize_db.py` once after getting new PDF
-   Use cached vector store for testing/queries
-   Keep `vectorstore/` folder in your `.gitignore`

### ❌ **DON'T:**

-   Re-run `initialize_db.py` unnecessarily
-   Delete `vectorstore/` folder unless needed
-   Call `/initialize` API endpoint repeatedly

---

## 🛠️ Optimized Workflow

### Initial Setup (One Time)

```bash
# 1. Place your PDF
cp ~/Downloads/COE.pdf backend/data/

# 2. Chunk it (ONLY ONCE)
cd backend
python scripts/initialize_db.py
```

### Daily Development (Fast)

```bash
# Start server (uses cache)
./start.sh

# Test interactively (uses cache)
python test_interactive.py

# API calls (uses cache)
curl -X POST http://localhost:8000/chat -d '{"query": "test"}'
```

### When PDF Updates (Rare)

```bash
# Re-chunk (only when PDF changes)
python scripts/initialize_db.py
```

---

## 🔍 How to Check Cache Status

### Check if cache exists:

```bash
ls -lh backend/data/vectorstore/
```

### Check cache size:

```bash
du -sh backend/data/vectorstore/
```

### Check cache stats via API:

```bash
curl http://localhost:8000/info
```

Response:

```json
{
    "app_name": "Calendar ERP Chatbot",
    "version": "1.0.0",
    "llm_model": "gemini-2.5-flash",
    "vector_db_path": "/path/to/vectorstore",
    "chatbot_initialized": true
}
```

---

## 🗑️ Clear Cache

If you need to force re-chunking:

```bash
# Delete cache
rm -rf backend/data/vectorstore/

# Re-chunk
cd backend
python scripts/initialize_db.py
```

---

## 🧪 Test Cache Performance

### Before Cache (First Time):

```bash
time python scripts/initialize_db.py
# Output: ~60 seconds
```

### With Cache (Subsequent Runs):

```bash
time python test_quick.py
# Output: ~3 seconds ⚡
```

---

## 💡 Summary

-   🎯 **Chunking = Slow** (~60 seconds)
-   ⚡ **Cache Loading = Fast** (~3 seconds)
-   📌 **Only chunk once** per PDF version
-   🚀 **Everything else uses cache**

**Your current setup is optimized** - chunking happens only when needed!

---

## 🔧 Customizing Chunk Settings

If you want to change how PDFs are chunked, edit `backend/app/document_processor.py`:

```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Increase for more context per chunk
    chunk_overlap=200,    # Overlap between chunks
    length_function=len,
)
```

**Note:** After changing these settings, you must re-run `initialize_db.py` to apply them.

---

## 📈 Cache Statistics

To see how many chunks are in your cache:

```python
# In Python
from app.document_processor import DocumentProcessor
from app.config import settings

dp = DocumentProcessor()
dp.load_vector_store()
count = dp.vector_store._collection.count()
print(f"Total chunks: {count}")
```

---

**For optimal performance, always use the cached vector store!** 🚀
