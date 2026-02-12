import os
import re
import requests
from openai import OpenAI
from dotenv import load_dotenv
from html.parser import HTMLParser

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_content = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'meta', 'link'):
            self.skip_content = True
    
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'meta', 'link'):
            self.skip_content = False
    
    def handle_data(self, data):
        if not self.skip_content:
            self.text.append(data)
    
    def get_text(self):
        return ' '.join(self.text).strip()

def fetch_url_content(url: str) -> str:
    """Fetch and extract text content from a URL"""
    try:
        if not url.startswith(('http://', 'https://')):
            return url  # Not a URL, return as is
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        # Extract text from HTML
        parser = HTMLTextExtractor()
        parser.feed(response.text)
        text = parser.get_text()
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Return first 3000 characters of meaningful content
        return text[:3000] if text else "Could not extract text from URL"
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
