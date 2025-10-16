# 🎮 Interactive Testing Guide

## Quick Start

### Step 1: Prepare Your Data

Place your `COE.pdf` in the `backend/data/` folder:

```bash
# Example
cp /path/to/your/COE.pdf backend/data/COE.pdf
```

**Note:** If you don't have a PDF yet, the system will use the sample `calendar_events.json` as a fallback.

### Step 2: Initialize the Vector Store

```bash
cd backend
python scripts/initialize_db.py
```

This will:

-   ✅ Load your PDF (or JSON fallback)
-   ✅ Split it into chunks
-   ✅ Create embeddings
-   ✅ Store in ChromaDB

### Step 3: Start Interactive Testing

**Option 1: Colorful Interactive Mode (Recommended)**

```bash
python test_interactive.py
```

Features:

-   ✅ Colored output for better readability
-   ✅ Clear visual separation
-   ✅ Source document viewer
-   ✅ Query counter
-   ✅ Help command

**Option 2: Simple Mode (No Colors)**

```bash
python test_simple.py
```

Features:

-   ✅ Works without colorama
-   ✅ Clean text-based interface
-   ✅ All functionality of colorful mode

---

## How to Use the Interactive Mode

### Starting a Session

```bash
cd backend
python test_interactive.py
```

You'll see:

```
======================================================================
🤖  Calendar ERP Chatbot - Interactive Mode
======================================================================
Powered by: Google Gemini 2.5 Flash + RAG
Type your questions about the academic calendar
Commands: 'quit', 'exit', 'q' to stop | 'help' for examples

⏳ Initializing chatbot...
✅ Chatbot ready!

💡 Type 'help' to see example questions
```

### Asking Questions

Simply type your question and press Enter:

```
----------------------------------------------------------------------
💬 You: When does the fall semester start?

🤔 Thinking...

🤖 Assistant:
The fall semester starts on August 26, 2024.

📚 Answer based on 3 source document(s)
Show source details? (y/n):
```

### Viewing Sources

Type `y` to see the source documents that were used to answer your question:

```
Show source details? (y/n): y

📚 Sources (3 documents):

[Source 1] Page 2:
Event: Fall Semester Begins
Type: semester_start
Date: 2024-08-26
Description: First day of Fall semester classes...

[Source 2] Page 5:
...
```

### Getting Help

Type `help` to see example questions:

```
💬 You: help

📚 Example Questions You Can Ask:
  • When does the fall semester start?
  • When are the midterm exams?
  • What holidays are in November?
  • Tell me about spring break
  • When is the last day to drop classes?
  • When does registration open?
  • What's the academic calendar for Fall 2024?
```

### Exiting

Type `quit`, `exit`, `q`, or press `Ctrl+C`:

```
💬 You: quit

👋 Goodbye! Thanks for using the chatbot.
📊 Total queries answered: 5
```

---

## Example Questions to Try

### Dates & Schedules

-   "When does the fall semester start?"
-   "When does the spring semester end?"
-   "What's the academic calendar for 2024-2025?"

### Exams

-   "When are the midterm exams?"
-   "When is the final exam period?"
-   "When are finals for spring semester?"

### Holidays & Breaks

-   "What holidays are in November?"
-   "Tell me about spring break"
-   "When is Thanksgiving break?"
-   "Are there any holidays in December?"

### Registration & Deadlines

-   "When does registration open?"
-   "When is the last day to drop classes?"
-   "When can I register for spring courses?"
-   "What's the add/drop deadline?"

### Complex Queries

-   "Give me a timeline of all important dates for Fall 2024"
-   "What events are happening in October?"
-   "List all the breaks during the academic year"

---

## Tips for Best Results

### 🎯 Be Specific

-   ✅ "When are midterm exams for Fall 2024?"
-   ❌ "When are exams?"

### 📅 Include Semester/Year

-   ✅ "When does Spring 2025 semester start?"
-   ❌ "When does semester start?"

### 🔍 Ask Follow-up Questions

After getting an answer, you can ask for more details:

```
You: When is spring break?
Assistant: Spring break is March 10-14, 2025.

You: Are there any events before spring break?
```

### 📚 Check Sources

Always review sources to verify important dates!

---

## Troubleshooting

### "Vector store not found"

**Solution:**

```bash
cd backend
python scripts/initialize_db.py
```

### "GOOGLE_API_KEY not found"

**Solution:** Check your `.env` file has:

```
GOOGLE_API_KEY=your-api-key-here
```

### "COE.pdf not found"

**Solution:** Either:

1. Place `COE.pdf` in `backend/data/` directory, OR
2. Use the JSON fallback (it will auto-detect)

### "Import colorama could not be resolved"

**Solution:**

```bash
pip install colorama
# OR use the simple version:
python test_simple.py
```

### No relevant answers

**Possible causes:**

-   PDF doesn't contain the information
-   Query too vague
-   Vector store needs reinitializing

**Solution:**

1. Check if your PDF has the information
2. Make your query more specific
3. Reinitialize: `python scripts/initialize_db.py`

---

## Advanced Usage

### Debug Mode

Run with `--debug` flag to see full error traces:

```bash
python test_interactive.py --debug
```

### Always Show Sources

Edit `test_interactive.py` and change line ~95:

```python
show_sources = input(...).strip().lower()
```

to:

```python
show_sources = 'y'  # Always show sources
```

### Change Number of Retrieved Documents

Edit `backend/app/document_processor.py` line ~114:

```python
search_kwargs={"k": 4}  # Change 4 to desired number
```

More sources = more context but slower responses.

### Customize Chunk Size

Edit `backend/app/document_processor.py` line ~17-18:

```python
chunk_size=1000,      # Increase for more context per chunk
chunk_overlap=200,    # Overlap between chunks
```

---

## Testing Workflow

### 1. Initial Setup

```bash
cd backend
# Place COE.pdf in data/
python scripts/initialize_db.py
```

### 2. Interactive Testing

```bash
python test_interactive.py
# Ask questions, verify answers
```

### 3. Update Data

```bash
# Update COE.pdf or add new content
python scripts/initialize_db.py  # Reinitialize
python test_interactive.py       # Test again
```

### 4. API Testing (Alternative)

```bash
# Start server in another terminal
./start.sh

# Test with API
python test_api.py
```

---

## Comparison: Interactive vs API Testing

| Feature             | Interactive Mode | API Mode   |
| ------------------- | ---------------- | ---------- |
| Ease of Use         | ⭐⭐⭐⭐⭐       | ⭐⭐⭐     |
| Quick Testing       | ⭐⭐⭐⭐⭐       | ⭐⭐⭐     |
| Source Viewing      | ⭐⭐⭐⭐⭐       | ⭐⭐⭐⭐   |
| Multiple Queries    | ⭐⭐⭐⭐⭐       | ⭐⭐⭐     |
| Integration Testing | ⭐⭐             | ⭐⭐⭐⭐⭐ |
| Automation          | ⭐               | ⭐⭐⭐⭐⭐ |

**Use Interactive Mode for:**

-   Quick manual testing
-   Exploring capabilities
-   Verifying answers
-   Development/debugging

**Use API Mode for:**

-   Integration testing
-   Automated tests
-   Frontend integration
-   Performance testing

---

## Next Steps

1. ✅ Test with sample data (JSON fallback)
2. ✅ Add your actual COE.pdf
3. ✅ Reinitialize vector store
4. ✅ Test queries interactively
5. ✅ Verify answers and sources
6. ✅ Integrate with frontend (if needed)
7. ✅ Deploy to production

---

**Happy Testing! 🚀**

For more information, see:

-   `SETUP_COMPLETE.md` - Full setup documentation
-   `QUICK_REFERENCE.md` - Quick commands reference
-   `backend/data/README.md` - Data folder guide
