# OCR Support for Image-based PDFs

## Overview

The vector store update script now supports **OCR (Optical Character Recognition)** for extracting text from image-based PDFs. This is useful when your PDF contains scanned documents, images with text, or screenshots.

## When to Use OCR

Use the `--ocr` flag when:
- Your PDF is scanned from a physical document
- Text extraction returns empty or minimal results
- The PDF contains images with embedded text
- You get very few chunks from a multi-page PDF

## Installation

### Python Dependencies

Already included in `requirements.txt`:
```bash
pip install pdf2image pytesseract Pillow
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

**Fedora/RHEL:**
```bash
sudo dnf install tesseract poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Verify installation:**
```bash
tesseract --version
pdftoppm -v
```

## Usage

### Basic OCR Usage

Add an image-based PDF with OCR:
```bash
python scripts/update_vectorstore.py --ocr data/scanned_document.pdf
```

### Replace with OCR

Replace entire vector store using OCR:
```bash
python scripts/update_vectorstore.py --replace --ocr data/scanned_document.pdf
```

### Mix OCR and Regular PDFs

You can mix both in a single command:
```bash
# Add regular PDF first
python scripts/update_vectorstore.py data/regular.pdf

# Then add image-based PDF with OCR
python scripts/update_vectorstore.py --ocr data/scanned.pdf
```

### Multiple PDFs with OCR

Process multiple image-based PDFs:
```bash
python scripts/update_vectorstore.py --ocr data/scan1.pdf data/scan2.pdf data/scan3.pdf
```

## How It Works

1. **PDF to Images**: Converts each PDF page to an image using `pdf2image`
2. **Text Extraction**: Uses Tesseract OCR to extract text from each image
3. **Document Creation**: Creates LangChain documents with extracted text
4. **Metadata**: Adds `extraction_method: 'ocr'` to metadata
5. **Chunking**: Chunks text normally and adds to vector store

## Example Output

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

## Comparison: Regular vs OCR

### Regular PDF Loading (PyPDF)
```bash
python scripts/update_vectorstore.py data/sat.pdf
```
Output:
- Fast processing
- Works for text-based PDFs
- May return empty results for image-based PDFs

### OCR-based Loading
```bash
python scripts/update_vectorstore.py --ocr data/sat.pdf
```
Output:
- Slower processing (converts to images first)
- Extracts text from images
- Works for scanned documents
- May have OCR errors in complex layouts

## Performance Comparison

**Regular PDF (text-based):**
- Speed: ~1-2 seconds per page
- Best for: Digital PDFs with selectable text

**OCR (image-based):**
- Speed: ~5-10 seconds per page
- Best for: Scanned documents, images, screenshots

## Troubleshooting

### Error: "OCR dependencies not installed"

Install the required packages:
```bash
pip install pdf2image pytesseract Pillow
sudo apt-get install tesseract-ocr poppler-utils
```

### Error: "tesseract is not installed"

Install Tesseract system dependency:
```bash
sudo apt-get install tesseract-ocr
```

### Error: "Unable to get page count"

Install Poppler utilities:
```bash
sudo apt-get install poppler-utils
```

### Poor OCR Results

Improve OCR accuracy:
1. **Higher Quality Scans**: Use 300 DPI or higher
2. **Better Image Quality**: Ensure good contrast and lighting
3. **Language Support**: Install additional Tesseract language packs
4. **Preprocessing**: Clean up images before creating PDFs

### Install Additional Languages

For non-English documents:
```bash
# Example: Install Hindi language pack
sudo apt-get install tesseract-ocr-hin

# Then specify language in code (future enhancement)
pytesseract.image_to_string(image, lang='hin')
```

## Advanced Usage

### Check What Extraction Method Was Used

The metadata includes `extraction_method`:
```python
# In vector store metadata
{
    'source': 'data/sat.pdf',
    'page': 0,
    'extraction_method': 'ocr'  # or 'regular' for PyPDF
}
```

### When to Use Which Method?

| PDF Type | Use Regular | Use OCR |
|----------|-------------|---------|
| Digital PDF with text | ✅ | ❌ |
| Scanned document | ❌ | ✅ |
| Mixed (text + images) | Try first | Fallback |
| Screenshots | ❌ | ✅ |
| Forms/Tables | ✅ | For images only |

## Your Example: sat.pdf

**Before (without OCR):**
```bash
python scripts/update_vectorstore.py data/sat.pdf
# Result: 3 chunks, minimal text extracted
```

**After (with OCR):**
```bash
python scripts/update_vectorstore.py --ocr data/sat.pdf
# Result: 3 chunks with full text extracted
# Page 1: 839 characters
# Page 2: 567 characters  
# Page 3: 593 characters
```

Now the chatbot can answer questions about your SAT exam schedule! 🎉

## Testing OCR Results

After adding with OCR, test the chatbot:

**Start backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Test query:**
```bash
python test_quick.py
# Ask: "When is my software engineering SAT exam?"
```

The chatbot should now be able to read and answer from the OCR-extracted text!

## Best Practices

1. **Try Regular First**: Always try without `--ocr` first
2. **Use OCR Only When Needed**: OCR is slower and may have errors
3. **Verify Extraction**: Check character counts to ensure text was extracted
4. **Test Queries**: Always test the chatbot after adding documents
5. **Keep Backups**: The script auto-creates backups when using `--replace`

## Future Enhancements

Potential improvements:
- [ ] Language detection and auto-selection
- [ ] Image preprocessing (deskew, denoise)
- [ ] Parallel OCR processing for multiple pages
- [ ] Confidence scores for OCR results
- [ ] Auto-detect if PDF needs OCR
- [ ] Support for other OCR engines (Google Vision, AWS Textract)

## Summary

The `--ocr` flag enables text extraction from image-based PDFs using Tesseract OCR. Use it when regular PDF loading fails to extract text from scanned documents or images.

**Quick Reference:**
```bash
# Regular PDF
python scripts/update_vectorstore.py data/document.pdf

# Image-based PDF (scanned/screenshots)
python scripts/update_vectorstore.py --ocr data/scanned.pdf

# Replace with OCR
python scripts/update_vectorstore.py --replace --ocr data/scanned.pdf

# List all documents
python scripts/update_vectorstore.py --list
```
