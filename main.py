from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import io
import re

app = FastAPI(title="FinData AI Extractor")

def extract_financial_data(text: str):
    """Uses Regex patterns to find prices and dates inside scanned text."""
    total_matches = re.findall(r'(?:total|grand total|amount due)[:\s]*\$?\s*([0-9]+\.[0-9]{2})', text, re.IGNORECASE)
    tax_matches = re.findall(r'(?:tax|sales tax|vat)[:\s]*\$?\s*([0-9]+\.[0-9]{2})', text, re.IGNORECASE)
    date_matches = re.findall(r'\b(\d{1,2}[/\.-]\d{1,2}[/\.-]\d{2,4})\b', text)

    return {
        "Estimated_Total": f"${total_matches[0]}" if total_matches else "Not Found",
        "Estimated_Tax": f"${tax_matches[0]}" if tax_matches else "Not Found",
        "Detected_Date": date_matches[0] if date_matches else "Not Found"
    }

@app.get("/")
def home():
    return {"status": "AI Engine is running. Go to /docs to test it!"}

@app.post("/extract-receipt/")
async def extract_receipt(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    raw_text = pytesseract.image_to_string(image)
    extracted_data = extract_financial_data(raw_text)
    
    return {
        "filename": file.filename,
        "extracted_data": extracted_data,
        "raw_text_preview": raw_text[:500]
    }
