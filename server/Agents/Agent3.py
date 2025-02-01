# Install required packages (note: pypdf is required by the PDF loader)
!pip install pypdf yfinance beautifulsoup4 pytesseract pdf2image google-generativeai langchain-community

import requests
import yfinance as yf
from bs4 import BeautifulSoup
import pytesseract
import json
import os

# Import pypdf indirectly via the loader (ensure that the package is installed)
from langchain_community.document_loaders import PyPDFLoader
from pdf2image import convert_from_path
import google.generativeai as genai

# Configure Gemini (ensure you replace with your actual API key)
GEMINI_API_KEY = "AIzaSyBUKdeWnrwywPwGs3QqYPKfTkI61VvZ8e8"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def get_stock_data(ticker):
    """Fetch stock data with error handling."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return data.iloc[-1].to_dict() if not data.empty else {}
    except Exception as e:
        print(f"Stock data error: {e}")
        return {}

def scrape_financial_news(url):
    """Scrape news with improved parsing and headers to reduce 401 errors."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Updated selector based on the site’s current HTML structure.
        # You might need to further adjust the selector if the structure changes.
        headlines = [tag.get_text(strip=True) for tag in soup.select('h3.article__headline')][:5]
        return headlines
    except Exception as e:
        print(f"News scraping error: {e}")
        return []

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using a text-based method and fallback to OCR."""
    try:
        # First try text extraction using PyPDFLoader (which uses pypdf internally)
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        text = "\n".join([p.page_content for p in pages])
        if text.strip():
            return text
        else:
            raise ValueError("Extracted text is empty; falling back to OCR.")
    except Exception as e:
        print(f"PDF text extraction failed, trying OCR: {e}")
        try:
            # Convert PDF pages to images using pdf2image (requires poppler installed and in PATH)
            images = convert_from_path(pdf_path)
            ocr_text = "\n".join([pytesseract.image_to_string(img) for img in images])
            return ocr_text
        except Exception as ocr_e:
            print(f"OCR failed: {ocr_e}")
            return ""

def process_financial_text(text):
    """Process the financial text with structured output using Gemini."""
    if not text:
        return {}
    
    prompt = f"""Analyze this financial document and return JSON with:
- balance_sheet: key figures
- income_statement: key figures
- cash_flow_statement: key figures
- assets_liabilities: analysis
- shareholder_equity: analysis
- profitability: metrics
- revenue: breakdown
- expenses: breakdown
- financial_trends: notable trends

Text: {text[:15000]}  # Truncate for token limits
Respond ONLY with valid JSON, no markdown formatting."""
    
    try:
        response = gemini_model.generate_content(prompt)
        # Clean up any markdown formatting if present
        json_str = response.text.replace('json', '').replace('', '').strip()
        return json.loads(json_str)
    except Exception as e:
        print(f"AI processing error: {e}")
        return {}

def generate_financial_report(ticker, news_url, pdf_path):
    """Generate a comprehensive financial report."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    return json.dumps({
        "stock_data": get_stock_data(ticker),
        "financial_analysis": process_financial_text(extract_text_from_pdf(pdf_path)),
        "market_news": scrape_financial_news(news_url)
    }, indent=2)

# Example usage
if _name_ == "_main_":
    try:
        report = generate_financial_report(
            ticker="AAPL",
            news_url="https://www.marketwatch.com/latest-news",
            pdf_path="/content/financials.pdf"  # Update the path to your PDF file
        )
        print(report)
    except Exception as e:
        print(f"Error generating report: {e}")