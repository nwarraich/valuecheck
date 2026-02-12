import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_listing(listing_text: str):
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
