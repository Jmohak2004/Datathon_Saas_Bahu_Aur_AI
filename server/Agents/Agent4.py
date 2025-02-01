!pip install google-auth google-auth-oauthlib google-auth-httplib2 chromadb neo4j requests faiss-cpu

import requests
import chromadb
from neo4j import GraphDatabase
import os
from datetime import datetime

# Define your API key and configurations (use environment variables for security)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBUKdeWnrwywPwGs3QqYPKfTkI61VvZ8e8')  # Use environment variable for API key
neo4j_uri = "neo4j://localhost:7687"  # Neo4j instance info (update accordingly)
neo4j_username = "mohak3345@gmail.com"  # Replace with your Neo4j username
neo4j_password = "Uday@2004"  # Replace with your Neo4j password

# Initialize ChromaDB for RAG (Retrieval-Augmented Generation)
client = chromadb.Client()
collection = client.create_collection(name="financial_reports")

# Neo4j setup for historical data retrieval
graph = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

# Initialize FAISS index (assuming embeddings are pre-generated for financial documents)
import faiss
index = faiss.IndexFlatL2(512)  # Replace 512 with your embedding size

# Function to query Google Gemini API
def query_gemini(query):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "contents": [{
            "parts": [{
                "text": query
            }]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error querying Gemini API: {response.status_code}, {response.text}")

# Function to fetch historical financial data from Neo4j knowledge graph
def get_financial_data_from_neo4j(fact):
    with graph.session() as session:
        query = """
        MATCH (n:FinancialFact {name: $fact})
        RETURN n.value AS value
        """
        result = session.run(query, fact=fact)
        data = result.single()
        return data['value'] if data else None

# Function to validate the inflation rate consistency
def validate_inflation_rate(report_inflation_rate):
    historical_inflation_rate = get_financial_data_from_neo4j("inflation_rate")
    if historical_inflation_rate:
        if abs(report_inflation_rate - historical_inflation_rate) > 5:
            return False  # flag if it deviates too much
    return True

# Function to extract and validate facts using Google Gemini API
def fact_check(report):
    # Extract facts from report using Google Gemini
    gemini_response = query_gemini(f"Extract key financial facts from the following report: {report}")
    
    # Extracted facts from the response
    extracted_facts = gemini_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').split('\n')
    
    verified_facts = []
    for fact in extracted_facts:
        if not fact.strip():
            continue
        # Cross-check extracted fact with live data using Google Gemini API
        gemini_validity = query_gemini(f"Is the following statement true? {fact}")
        if "true" in gemini_validity.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').lower():
            verified_facts.append((fact, 'Valid'))
        else:
            # Check the fact in the Neo4j knowledge graph for historical consistency
            historical_data = get_financial_data_from_neo4j(fact)
            if historical_data:
                verified_facts.append((fact, 'Valid'))
            else:
                verified_facts.append((fact, 'Invalid'))
    
    return verified_facts

# Function to generate a report summary after validation
def generate_valid_report(report):
    validation_result = fact_check(report)
    invalid_facts = [fact for fact, status in validation_result if status == 'Invalid']
    
    if invalid_facts:
        invalid_facts_text = "\n".join(invalid_facts)
        return f"Report contains invalid facts:\n{invalid_facts_text}"
    else:
        return "Report is validated and consistent with external data sources."

# Example usage in Colab:
financial_report = """
The inflation rate for 2025 is projected to be 3.5%, based on current economic trends. 
Historical data suggests an inflation rate of 3.2% for the past decade.
"""
validated_report = generate_valid_report(financial_report)
print(validated_report)