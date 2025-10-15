# Data Directory

## 📄 COE.pdf

Place your **COE.pdf** (College of Engineering calendar or any academic calendar PDF) in this directory.

### How to Add Your PDF:

1. Copy your PDF file to this directory: `backend/data/`
2. Name it `COE.pdf` (or update the path in `scripts/initialize_db.py`)
3. Run the initialization script:

```bash
cd backend
python scripts/initialize_db.py
```

### Supported PDF Formats:

-   ✅ Text-based PDFs (searchable text)
-   ✅ Multi-page documents
-   ✅ Academic calendars, schedules, event lists
-   ⚠️ Scanned PDFs may require OCR preprocessing

### What Happens During Initialization:

1. PDF is loaded and parsed page by page
2. Text is split into chunks (1000 chars with 200 overlap)
3. Chunks are embedded using sentence transformers
4. Embeddings are stored in ChromaDB vector database
5. Database is saved to `vectorstore/` directory

### File Structure After Initialization:

```
data/
├── COE.pdf                    # Your source PDF
├── calendar_events.json       # Fallback JSON data (optional)
├── vectorstore/               # Generated vector database
│   ├── chroma.sqlite3        # Vector store database
│   └── ...                   # Index files
└── README.md                 # This file
```

### Fallback to JSON:

If `COE.pdf` is not found, the system will automatically use `calendar_events.json` as a fallback. This allows you to test the system with sample data before adding your actual PDF.

### Updating the Data:

After updating `COE.pdf`, re-run the initialization:

```bash
cd backend
python scripts/initialize_db.py
```

This will recreate the vector store with the new data.

### Troubleshooting:

**Error: "PDF file not found"**

-   Ensure `COE.pdf` is in `backend/data/` directory
-   Check file name is exactly `COE.pdf` (case-sensitive)

**Error: "Could not parse PDF"**

-   Ensure PDF contains searchable text (not just images)
-   Try using a different PDF parser if needed

**Empty results after initialization:**

-   Check if PDF has extractable text
-   Verify PDF is not corrupted
-   Try opening PDF in a reader to confirm it's valid
