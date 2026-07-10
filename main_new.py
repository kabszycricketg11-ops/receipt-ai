import streamlit as st
import pytesseract
from PIL import Image
import io
import re

# Set up the ChatGPT style clean page config
st.set_page_config(page_title="FinAI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 FinAI Receipt Assistant")
st.write("Upload a receipt or invoice, and I will analyze the financial data for you instantly.")

def extract_financial_data(text: str):
    total_matches = re.findall(r'(?:total|grand total|amount due)[:\s]*\$?\s*([0-9]+\.[0-9]{2})', text, re.IGNORECASE)
    tax_matches = re.findall(r'(?:tax|sales tax|vat)[:\s]*\$?\s*([0-9]+\.[0-9]{2})', text, re.IGNORECASE)
    date_matches = re.findall(r'\b(\d{1,2}[/\.-]\d{1,2}[/\.-]\d{2,4})\b', text)

    return {
        "Total": f"${total_matches[0]}" if total_matches else "Not Detected",
        "Tax": f"${tax_matches[0]}" if tax_matches else "Not Detected",
        "Date": date_matches[0] if date_matches else "Not Detected"
    }

uploaded_file = st.file_uploader("📸 Drop an image or snap a photo of a receipt...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.chat_message("user"):
        st.write("Analyzing this receipt...")
        st.image(uploaded_file, width=250)
    
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    with st.spinner("🤖 Scanning ledger data..."):
        raw_text = pytesseract.image_to_string(image)
        data = extract_financial_data(raw_text)
        
    with st.chat_message("assistant"):
        st.write("### Here is the financial breakdown I extracted:")
        st.markdown(f"**💰 Estimated Total:** {data['Total']}")
        st.markdown(f"**🧾 Tax/VAT Amount:** {data['Tax']}")
        st.markdown(f"**📅 Transaction Date:** {data['Date']}")
        
        with st.expander("View Raw Scanned Text"):
            st.text(raw_text[:800])
