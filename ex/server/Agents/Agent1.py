# # Install required libraries
!pip install yfinance beautifulsoup4 requests pytesseract pillow pandas
!pip install -q google-generativeai
!pip install -q transformers

# Import libraries
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import pytesseract
from PIL import Image
import pandas as pd
import google.generativeai as genai
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set up Tesseract (for OCR)
!sudo apt install tesseract-ocr
!pip install pytesseract

# Set up Gemini API
genai.configure(api_key="AIzaSyBUKdeWnrwywPwGs3QqYPKfTkI61VvZ8e8")  # Replace with your Gemini API key
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# Set up Phi model (lightweight NLP)
phi_model_name = "microsoft/phi-2"
phi_tokenizer = AutoTokenizer.from_pretrained(phi_model_name, trust_remote_code=True)
phi_model = AutoModelForCausalLM.from_pretrained(phi_model_name, trust_remote_code=True)

# Function to fetch real-time stock data using Yahoo Finance
def fetch_stock_data(ticker, period="1d"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

# Function to scrape financial news headlines
def scrape_financial_news(query):
    url = f"https://www.reuters.com/site-search/?query={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find_all("h3", class_="search-result-title")
    return [headline.text.strip() for headline in headlines]

# Function to extract text from an image using OCR
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Function to analyze text using Gemini
def analyze_with_gemini(text):
    response = gemini_model.generate_content(f"Analyze this financial text and summarize key insights: {text}")
    return response.text

# Function to process text using Phi
def process_with_phi(text):
    inputs = phi_tokenizer(text, return_tensors="pt", max_length=1000, truncation=True)
    outputs = phi_model.generate(**inputs, max_length=1000)
    return phi_tokenizer.decode(outputs[0], skip_special_tokens=True)

# Main function to execute the pipeline
def analyze_company(company_name):
    # Fetch stock data
    ticker = company_name.upper()  # Convert to uppercase for Yahoo Finance
    stock_data = fetch_stock_data(ticker)
    print(f"Stock Data for {ticker}:\n{stock_data}\n")

    # Scrape financial news
    headlines = scrape_financial_news(company_name)
    print("Financial News Headlines:")
    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")

    # Extract text from an image (e.g., financial statement)
    image_path = "/content/financial.png"  # Upload an image to Colab
    extracted_text = extract_text_from_image(image_path)
    print(f"\nExtracted Text from Image:\n{extracted_text}\n")

    # Analyze extracted text using Gemini
    gemini_analysis = analyze_with_gemini(extracted_text)
    print(f"Gemini Analysis:\n{gemini_analysis}\n")

    # Process text using Phi
    phi_analysis = process_with_phi(extracted_text)
    print(f"Phi Analysis:\n{phi_analysis}\n")

# Take company name as input
company_name = input("Enter the company name (e.g., Apple, Tesla): ")
analyze_company(company_name)