# 📚 Vector Store Update Guide

## Overview

The `update_vectorstore.py` script allows you to manage your vector database without losing existing data.

## Features

✅ **Incremental Updates** - Add new PDFs without deleting old ones  
✅ **Full Replacement** - Replace entire vector store with backup  
✅ **OCR Support** - Extract text from image-based/scanned PDFs  
✅ **List Contents** - View all documents currently indexed  
✅ **Automatic Backups** - Creates timestamped backups before replacement  
✅ **Multi-file Support** - Process multiple PDFs in one command

---

## Installation

No additional dependencies needed - uses existing backend setup.

```bash
cd backend/scripts
chmod +x update_vectorstore.py
```

---

## Usage

### 1. List Current Contents 📋

See what's currently in your vector store:

```bash
python scripts/update_vectorstore.py --list
```

**Output:**

```
📊 Vector Store Contents
================================================================================

✅ Vector store loaded from: /path/to/vectorstore
📦 Total chunks: 85

📚 Source Documents:
  1. COE.pdf
     Pages: 17 pages (from 0 to 16)

✅ Use --add to add more documents or --replace to start fresh
```

---

### 2. Add New Documents (Incremental) ➕

Add new PDFs to existing vector store **without** deleting old data:

```bash
# Add single PDF
python scripts/update_vectorstore.py data/NewCalendar.pdf

# Add multiple PDFs
python scripts/update_vectorstore.py data/Fall2024.pdf data/Spring2025.pdf data/Summer2025.pdf
```

**Output:**

```
🔄 Adding Documents to Vector Store
================================================================================
✅ Loaded existing vector store (85 chunks)

📄 Loading PDF files...

  Processing: NewCalendar.pdf
  ✅ Loaded 42 chunks

🔨 Processing 42 total chunks...
  Adding to existing vector store...

✅ Vector store updated successfully!
📊 Total chunks in database: 127
📈 Added: 42 new chunks
```

**What happens:**

-   Existing data is **preserved**
-   New documents are **added**
-   Queries will search across **all documents**

---

### 3. Use OCR for Image-based PDFs 🔍

Extract text from scanned documents or images using OCR:

```bash
# Add scanned PDF with OCR
python scripts/update_vectorstore.py --ocr data/scanned_exam_schedule.pdf

# Replace with OCR
python scripts/update_vectorstore.py --replace --ocr data/scanned_calendar.pdf
```

**Output:**

```
🔍 Using OCR to extract text from: data/sat.pdf
  📸 Converting PDF pages to images...
  ✅ Converted 3 pages to images
  🔤 Extracting text with OCR...
     Page 1: Extracted 839 characters
     Page 2: Extracted 567 characters
     Page 3: Extracted 593 characters
✅ OCR completed: 3 pages with text
```

**When to use OCR:**
- PDF is scanned from a physical document
- Text extraction returns empty or minimal results  
- PDF contains images with embedded text
- Screenshots or photos of documents

**See [OCR_GUIDE.md](OCR_GUIDE.md) for detailed instructions and troubleshooting.**

---

### 4. Replace Entire Vector Store 🔄

Replace all existing data with new PDFs (creates automatic backup):

```bash
# Replace with single PDF
python scripts/update_vectorstore.py --replace data/COE_Updated.pdf

# Replace with multiple PDFs
python scripts/update_vectorstore.py --replace data/Fall2024.pdf data/Spring2025.pdf
```

**Output:**

```
🗑️  Replacing Vector Store
================================================================================
💾 Creating backup: vectorstore_backup_20251016_120530
✅ Backup created
🗑️  Deleting old vector store...
✅ Old vector store deleted

📄 Loading PDF files...

  Processing: COE_Updated.pdf
  ✅ Loaded 95 chunks

🔨 Processing 95 total chunks...
  Creating new vector store...

✅ Vector store updated successfully!
📊 Total chunks in database: 95
```

**What happens:**

-   Old vector store is **backed up** to `vectorstore_backup_TIMESTAMP`
-   Old data is **deleted**
-   New vector store is **created** from scratch

---

## Common Workflows

### Workflow 1: Add Supplementary Documents

You have the main calendar (COE.pdf) and want to add department-specific calendars:

```bash
# Current: COE.pdf (main calendar)
python scripts/update_vectorstore.py --list

# Add department calendars
python scripts/update_vectorstore.py \
  data/CS_Department_Calendar.pdf \
  data/EE_Department_Calendar.pdf \
  data/ME_Department_Calendar.pdf

# Now queries search across all 4 documents!
```

---

### Workflow 2: Quarterly Updates

You receive updated calendar every quarter:

```bash
# Q1: Initial setup
python scripts/initialize_db.py

# Q2: Add new quarter
python scripts/update_vectorstore.py data/Q2_Updates.pdf

# Q3: Replace with consolidated version
python scripts/update_vectorstore.py --replace data/Annual_Calendar_Updated.pdf
```

---

### Workflow 3: Multi-Source Knowledge Base

Build a comprehensive knowledge base from multiple sources:

```bash
# Start with main calendar
python scripts/initialize_db.py

# Add academic policies
python scripts/update_vectorstore.py data/Academic_Policies.pdf

# Add student handbook
python scripts/update_vectorstore.py data/Student_Handbook.pdf

# Add course catalog
python scripts/update_vectorstore.py data/Course_Catalog.pdf

# List everything
python scripts/update_vectorstore.py --list
```

---

## After Updating

### 1. Restart Server

The server needs to reload the vector store:

```bash
# Kill current server (Ctrl+C in terminal)

# Restart
cd backend
./start.sh
```

### 2. Test Updates

Verify new content is searchable:

```bash
# Quick test
python test_quick.py

# Interactive test
python test_interactive.py

# API test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What information is new in the updated calendar?"}'
```

---

## Advanced Features

### Backup Management

Backups are created automatically when using `--replace`:

```bash
# List backups
ls -lh backend/data/ | grep vectorstore_backup

# Restore from backup
rm -rf backend/data/vectorstore
mv backend/data/vectorstore_backup_20251016_120530 backend/data/vectorstore
```

### Custom Backup Location

Before replacing, manually backup to specific location:

```bash
# Manual backup
cp -r backend/data/vectorstore backend/backups/vectorstore_before_update

# Then replace
python scripts/update_vectorstore.py --replace data/new.pdf

# Restore if needed
rm -rf backend/data/vectorstore
cp -r backend/backups/vectorstore_before_update backend/data/vectorstore
```

---

## Troubleshooting

### Error: "No vector store found"

**Problem:** First time use or vector store deleted  
**Solution:** Create initial vector store first

```bash
python scripts/initialize_db.py
```

### Error: "File not found"

**Problem:** PDF path is incorrect  
**Solution:** Use absolute path or check file exists

```bash
# Check file exists
ls -lh data/COE.pdf

# Use absolute path
python scripts/update_vectorstore.py /full/path/to/file.pdf
```

### Large PDFs Taking Too Long

**Problem:** Processing 100+ page PDF is slow  
**Solution:** This is normal - embedding generation takes time

```bash
# Approximate times:
# 10 pages  → ~10 seconds
# 50 pages  → ~30 seconds
# 100 pages → ~60 seconds
```

### Duplicate Documents

**Problem:** Same PDF added twice  
**Solution:** ChromaDB will index it twice - use `--replace` to start fresh

```bash
python scripts/update_vectorstore.py --replace data/COE.pdf
```

---

## Technical Details

### What Gets Stored

For each PDF chunk, the vector store saves:

```python
{
  "content": "Fall Semester begins on August 26, 2024...",
  "metadata": {
    "source": "data/COE.pdf",
    "page": 5
  },
  "embedding": [0.123, -0.456, ...]  # 384-dimensional vector
}
```

### Chunking Strategy

-   **Chunk Size**: 1000 characters
-   **Overlap**: 200 characters
-   **Why?** Balances context preservation with search precision

### Storage Location

```
backend/data/
├── COE.pdf                          # Source document
├── vectorstore/                     # Active vector store
│   ├── chroma.sqlite3              # Vector database
│   └── [uuid]/                     # Collection data
└── vectorstore_backup_TIMESTAMP/   # Automatic backups
```

---

## Performance Comparison

| Operation             | Time | Documents After |
| --------------------- | ---- | --------------- |
| Initial creation      | ~60s | 85 chunks       |
| Add 1 PDF (20 pages)  | ~20s | 127 chunks      |
| Add 3 PDFs (60 pages) | ~60s | 250 chunks      |
| Replace with 1 PDF    | ~60s | 85 chunks       |
| List contents         | <1s  | -               |

---

## Command Reference

```bash
# List contents
python scripts/update_vectorstore.py --list

# Add single PDF
python scripts/update_vectorstore.py data/file.pdf

# Add multiple PDFs
python scripts/update_vectorstore.py data/file1.pdf data/file2.pdf data/file3.pdf

# Replace entire store
python scripts/update_vectorstore.py --replace data/new.pdf

# Help
python scripts/update_vectorstore.py --help
```

---

## Integration with API

You can also trigger updates via the API endpoint:

```bash
# Reinitialize from default PDF
curl -X POST http://localhost:8000/initialize

# The API endpoint uses initialize_db.py logic
# For incremental updates, use the script directly
```

---

## Best Practices

✅ **Backup before major updates** - Use `--replace` for automatic backups  
✅ **Test after updates** - Always run test_quick.py  
✅ **Restart server** - Required for changes to take effect  
✅ **Use incremental for additions** - Preserve existing data  
✅ **Use replace for new versions** - Clean slate for updated documents  
✅ **List contents regularly** - Know what's in your database

---

## Example Session

```bash
# Check current state
$ python scripts/update_vectorstore.py --list
📊 Total chunks: 85
📚 Source: COE.pdf (17 pages)

# Add department calendar
$ python scripts/update_vectorstore.py data/CS_Calendar.pdf
✅ Added: 42 new chunks
📊 Total: 127 chunks

# Check updated state
$ python scripts/update_vectorstore.py --list
📊 Total chunks: 127
📚 Sources:
  1. COE.pdf (17 pages)
  2. CS_Calendar.pdf (10 pages)

# Restart server
$ cd backend && ./start.sh

# Test new content
$ python test_quick.py
✅ All tests passed!
```

---

## Summary

The incremental update model gives you flexibility:

-   **Add** new documents without losing old ones
-   **Replace** everything when you need a fresh start
-   **List** contents to see what's indexed
-   **Backup** automatically before replacements

**Use incremental updates** when building a knowledge base from multiple sources.  
**Use full replacement** when you have an updated version of the same document.

---

**Questions?** Check the main documentation or run:

```bash
python scripts/update_vectorstore.py --help
```
