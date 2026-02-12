import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def fetch_url_content(url: str) -> str:
    """Fetch text content from a URL"""
    try:
        if not url.startswith(('http://', 'https://')):
            return url  # Not a URL, return as is
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Return basic text from HTML
        return response.text[:5000]  # Limit to first 5000 chars
    except Exception as e:
        return f"Could not fetch URL: {str(e)}"

def analyze_listing(listing_text: str):
    if not client:
        return {
            "verdict": "Error",
            "estimated_range": "N/A",
            "listed_price": "N/A",
            "explanation": "OpenAI API key not configured. Add OPENAI_API_KEY to .env file."
        }
    
    # If it's a URL, fetch the content
    if listing_text.startswith(('http://', 'https://')):
        listing_text = fetch_url_content(listing_text)
    
    prompt = f"""
You are a real estate valuation assistant.

Given the following property listing, determine:
1. Whether the property is Underpriced, Fairly Priced, or Overpriced
2. An estimated fair price range
3. A short explanation

Listing:
{listing_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert real estate analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    ai_text = response.choices[0].message.content

    return {
        "verdict": "AI Analysis",
        "estimated_range": "See explanation",
        "listed_price": "Extracted from listing",
        "explanation": ai_text
    }
