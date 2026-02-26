import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def analyze_listing(listing_text: str):
    """
    NEW BEHAVIOUR:
    listing_text is now a USER PROFILE text, e.g.
    "age: 22, income: 85000, savings: 30000, goal: buy, notes: prefer sydney, near train"
    """
    if not client:
        return {
            "verdict": "Error",
            "estimated_range": "N/A",
            "listed_price": "N/A",
            "explanation": "OpenAI API key not configured. Add OPENAI_API_KEY to .env file."
        }

    user_input = (listing_text or "").strip()

    prompt = f"""
You are ValueCheck's Australian suburb recommendation assistant.

The user will provide:
- Age
- Income (AUD per year)
- Savings (AUD)
- Goal: rent OR buy OR invest
- Optional notes (location preference, commute, family size, lifestyle)

Your tasks:
1) Extract these fields from the user's input.
2) If any of age/income/savings/goal are missing, ask short follow-up questions.
3) If all are present, recommend 5–8 suburbs (prefer Sydney/NSW unless the user specifies another city/state),
   explain why each suburb suits them, and suggest 2–3 suitable property sizes (apartment/townhouse/house).
4) Mention tradeoffs briefly (distance, competition, strata, older stock etc).
5) Do NOT invent exact prices, and do NOT promise guaranteed returns.

Return ONLY valid JSON. No markdown. Use one of these formats:

IF MISSING REQUIRED INFO:
{{
  "mode": "needs_more_info",
  "missing_fields": ["age", "income", "savings", "goal"],
  "questions": ["...", "...", "..."]
}}

IF ENOUGH INFO:
{{
  "mode": "recommendations",
  "summary": {{
    "profile_fit": "string",
    "key_assumptions": ["string", "..."]
  }},
  "property_size_suggestions": ["string", "string", "string"],
  "suburb_recommendations": [
    {{
      "suburb": "string",
      "state": "string",
      "best_for": "string",
      "why_good": ["string", "string", "string"],
      "watch_out_for": ["string", "string"]
    }}
  ],
  "next_questions": ["string", "string", "string"]
}}

User input:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You recommend Australian suburbs based on a user's finances and goal."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    ai_text = response.choices[0].message.content

    # Parse JSON (so your frontend gets structured data)
    try:
        data = json.loads(ai_text)
    except json.JSONDecodeError:
        # fallback: still return something usable
        return {
            "verdict": "AI Recommendations",
            "estimated_range": "N/A",
            "listed_price": "N/A",
            "explanation": ai_text
        }

    # Keep your old return keys so your UI doesn't break
    if data.get("mode") == "needs_more_info":
        return {
            "verdict": "Need more info",
            "estimated_range": "N/A",
            "listed_price": "N/A",
            "explanation": data
        }

    return {
        "verdict": "AI Recommendations",
        "estimated_range": "N/A",
        "listed_price": "N/A",
        "explanation": data
    }
