import os
from dotenv import load_dotenv
import json

load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
import re

def call_llm(data, context):
    prompt = f"""
    User:
    Risk: {data.risk}
    Duration: {data.duration_years} years
    Budget: {data.budget}

    Context:
    {context}

    Return ONLY valid JSON (no backticks, no explanation):
    [
      {{
        "stock": "name",
        "allocation": number,
        "reason": "short reason"
      }}
    ]
    """

    response = model.generate_content(prompt)
    text = response.text.strip()

    print("RAW LLM OUTPUT:", text)  # 🔍 debug

    # 🔥 STEP 1: remove markdown if present
    if "```" in text:
        text = text.replace("```json", "").replace("```", "").strip()

    # 🔥 STEP 2: extract JSON if extra text exists
    try:
        json_match = re.search(r"\[.*\]", text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
    except:
        pass

    # 🔥 STEP 3: parse safely
    try:
        parsed = json.loads(text)
    except Exception as e:
        print("JSON parsing failed:", e)
        return []   # 🚨 NEVER return None

    # 🔥 STEP 4: validate structure
    if not isinstance(parsed, list):
        return []

    # 🔥 STEP 5: fix keys + sanitize
    clean_output = []
    for item in parsed:
        if not isinstance(item, dict):
            continue

        stock = item.get("stock")
        allocation = item.get("allocation") or item.get("amount")
        reason = item.get("reason", "")

        # skip invalid entries
        if not stock or not allocation:
            continue

        clean_output.append({
            "stock": stock,
            "allocation": int(allocation),
            "reason": reason
        })

    return clean_output