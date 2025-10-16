# 📝 .gitignore Setup Guide

## 🗂️ File Structure

The project now has `.gitignore` files at multiple levels:

```
CalendarERPChatbot/
├── .gitignore                 # Root - covers entire project
├── backend/
│   └── .gitignore            # Backend specific (Python/FastAPI)
└── frontend/
    └── .gitignore            # Frontend specific (React)
```

---

## 🎯 What Each File Covers

### 📦 Root `.gitignore`

**Location:** `/.gitignore`

**Covers:**

-   ✅ Python backend patterns
-   ✅ React frontend patterns
-   ✅ AI/ML specific (vector stores, models, PDFs)
-   ✅ Environment variables
-   ✅ Databases
-   ✅ Secrets/credentials
-   ✅ IDE files
-   ✅ OS artifacts
-   ✅ Docker files
-   ✅ Logs and temp files

**Best for:** Complete monorepo coverage

---

### 🐍 Backend `.gitignore`

**Location:** `/backend/.gitignore`

**Covers:**

-   ✅ Python bytecode
-   ✅ Virtual environments
-   ✅ Testing/coverage
-   ✅ Vector stores (ChromaDB)
-   ✅ Model caches
-   ✅ PDFs
-   ✅ Python-specific patterns
-   ✅ Node modules (if mixing)

**Best for:** Python/FastAPI development

---

### ⚛️ Frontend `.gitignore`

**Location:** `/frontend/.gitignore`

**Covers:**

-   ✅ node_modules
-   ✅ Build outputs (build/, dist/, .next/)
-   ✅ Environment files
-   ✅ Testing coverage
-   ✅ TypeScript build info
-   ✅ Vite/React specific
-   ✅ Package manager locks (optional)
-   ✅ IDE files

**Best for:** React/Vite/Next.js development

---

## 🚀 Usage

### For Full Stack Development

The **root `.gitignore`** handles everything automatically!

```bash
# From project root
git add .
git commit -m "Your message"
```

All ignored patterns work across the entire project.

---

### For Backend Only

```bash
cd backend
git add .
# Uses backend/.gitignore patterns
```

---

### For Frontend Only

```bash
cd frontend
git add .
# Uses frontend/.gitignore patterns
```

---

## 🔍 Key Patterns Ignored

### 🔐 Secrets (Never Commit!)

-   `.env` files (except `.env.example`)
-   `credentials.json`
-   `service_account.json`
-   API keys
-   `*.pem`, `*.key`

### 📦 Dependencies

-   `node_modules/`
-   `venv/`, `env/`
-   `__pycache__/`

### 🏗️ Build Artifacts

-   `build/`, `dist/`
-   `.next/`, `out/`
-   `*.pyc`, `*.pyo`

### 🧠 AI/ML Specific

-   `vectorstore/` - ChromaDB database
-   `*.pdf` - Large PDF files
-   `*.bin`, `*.pt` - Model weights
-   `.cache/huggingface/` - Model cache

### 💾 Databases

-   `*.sqlite3`
-   `*.db`
-   `chroma.sqlite3`

### 🛠️ IDE Files

-   `.vscode/`
-   `.idea/`
-   `*.swp`

---

## ⚠️ Important Files NOT Ignored

These are **tracked** by git:

### ✅ Committed Files

-   Source code (`.py`, `.js`, `.jsx`, `.ts`, `.tsx`)
-   Configuration (example files like `.env.example`)
-   Documentation (`*.md`)
-   Package configs (`package.json`, `requirements.txt`)
-   Docker files (`Dockerfile`, `docker-compose.yml`)
-   Lock files (optional - see below)

---

## 🔧 Customization

### Lock Files

By default, lock files are **tracked**. To ignore them, uncomment in `.gitignore`:

```gitignore
# Uncomment to ignore:
# package-lock.json
# yarn.lock
# pnpm-lock.yaml
```

**Recommendation:** Keep lock files for reproducible builds!

---

### Project Specific Patterns

Add to root `.gitignore`:

```gitignore
# ========================================
# PROJECT SPECIFIC
# ========================================

# Backend specific
backend/data/vectorstore/
backend/logs/
backend/*.sqlite3

# Frontend specific
frontend/build/
frontend/dist/
frontend/.next/

# Test data
test_data/
sample_data/
```

---

## 📊 What Gets Ignored in This Project

### Backend

```
backend/
├── __pycache__/          ❌ Ignored
├── venv/                 ❌ Ignored
├── .env                  ❌ Ignored
├── *.pyc                 ❌ Ignored
├── data/
│   ├── vectorstore/      ❌ Ignored (ChromaDB cache)
│   └── COE.pdf           ❌ Ignored (large PDF)
├── logs/                 ❌ Ignored
└── app/
    └── *.py              ✅ Tracked
```

### Frontend

```
frontend/
├── node_modules/         ❌ Ignored
├── build/                ❌ Ignored
├── dist/                 ❌ Ignored
├── .env.local            ❌ Ignored
├── .next/                ❌ Ignored
└── src/
    └── *.jsx             ✅ Tracked
```

---

## ✅ Best Practices

### 1. Never Commit Secrets

```bash
# Always check before committing
git status
git diff

# If you accidentally staged secrets:
git reset HEAD .env
```

### 2. Keep Vector Store Out

The vector store is **large and regeneratable**:

-   ❌ Don't commit `data/vectorstore/`
-   ✅ Regenerate with `python scripts/initialize_db.py`

### 3. Commit Example Files

```bash
# Good
git add .env.example
git add docker-compose.yml

# Bad
git add .env
git add credentials.json
```

### 4. Check .gitignore Works

```bash
# Test patterns
git check-ignore -v backend/data/vectorstore/

# See what would be committed
git add --dry-run .
```

---

## 🧪 Testing .gitignore

```bash
# Check if a file is ignored
git check-ignore backend/.env
# Output: backend/.env (means it's ignored)

# See why a file is ignored
git check-ignore -v backend/.env
# Shows which pattern matched

# List all ignored files
git status --ignored
```

---

## 🔄 After Adding React App

When you create the frontend:

```bash
# Create React app
cd frontend
npm create vite@latest . -- --template react

# The frontend/.gitignore is already there!
# Just start coding:
npm install
npm run dev
```

---

## 📚 Summary

| File                   | Purpose                 | Scope          |
| ---------------------- | ----------------------- | -------------- |
| `/.gitignore`          | Master ignore file      | Entire project |
| `/backend/.gitignore`  | Python/FastAPI specific | Backend only   |
| `/frontend/.gitignore` | React specific          | Frontend only  |

**All three work together** to keep your repo clean! 🎉

---

## 🆘 Troubleshooting

### File Still Being Tracked?

If a file was committed before adding to `.gitignore`:

```bash
# Remove from git but keep locally
git rm --cached backend/data/vectorstore/chroma.sqlite3

# Commit the removal
git commit -m "Remove vector store from tracking"
```

### Want to Ignore Entire Folder?

```bash
# Add to .gitignore
echo "my_folder/" >> .gitignore

# Remove from git
git rm -r --cached my_folder/

# Commit
git commit -m "Ignore my_folder"
```

---

**Your project is now ready for both Python backend and React frontend development!** 🚀
