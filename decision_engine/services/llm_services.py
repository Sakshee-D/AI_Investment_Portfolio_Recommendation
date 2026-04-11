import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def call_llm(data, context):

    # 🔥 STEP 1: Format context properly
    formatted_context = ""

    for c in context:
        if isinstance(c, dict):
            formatted_context += c.get("summary", str(c)) + "\n\n"
        else:
            formatted_context += str(c) + "\n\n"

    # 🔥 STEP 2: Better prompt (forces reasoning)
    prompt = f"""
You are an AI stock advisor.

STRICT RULES:
- Use ONLY the given context
- Do NOT invent stocks
- Match user's risk level
- Use both stock fundamentals AND recent news
- If news is negative → reduce allocation
- If positive → prefer that stock

User:
Risk: {data.risk}
Duration: {data.duration_years} years
Budget: {data.budget}

Context:
{formatted_context}

Task:
- Select 3–5 stocks from context
- Allocate full budget
- Give short reasoning based on context

Return ONLY valid JSON: (no backticks, no explanation)
[
  {{
    "stock": "name",
    "allocation": number,
    "reason": "based on context"
  }}
]
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    print("RAW LLM OUTPUT:", text)

    # 🔥 STEP 3: clean markdown
    if "```" in text:
        text = text.replace("```json", "").replace("```", "").strip()

    # 🔥 STEP 4: extract JSON safely
    try:
        json_match = re.search(r"\[.*\]", text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
    except:
        pass

    # 🔥 STEP 5: parse
    try:
        parsed = json.loads(text)
    except Exception as e:
        print("JSON parsing failed:", e)
        return []

    if not isinstance(parsed, list):
        return []

    # 🔥 STEP 6: sanitize
    clean_output = []
    for item in parsed:
        if not isinstance(item, dict):
            continue

        stock = item.get("stock")
        allocation = item.get("allocation") or item.get("amount")
        reason = item.get("reason", "")

        if not stock or not allocation:
            continue

        clean_output.append({
            "stock": stock,
            "allocation": int(allocation),
            "reason": reason
        })

    return clean_output