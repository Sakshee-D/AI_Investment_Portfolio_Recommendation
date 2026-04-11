import requests
import json

# API endpoint
url = "http://localhost:8000/retrieve"

# Query parameters
params = {
    "query": "low risk long term"
}

try:
    # Send request
    response = requests.get(url, params=params)

    # Convert response to JSON
    data = response.json()

    # Pretty print output
    print("\n📊 Retrieved Stock Data:\n")
    print(json.dumps(data, indent=4))

except Exception as e:
    print("❌ Error:", e)