import json
import requests

# 1. User Context (Occasion, Weather, etc.)
user_context = (
    "Occasion: Smart-casual evening dinner. "
    "Weather: Slightly chilly spring evening, around 15°C. "
    "Preferences: Professional but relaxed."
)

with open("wardrobe.json", "r", encoding="utf-8") as f:
    wardrobe_data = json.load(f)

# 3. API Configuration
# Replace with your actual Gemini API key
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"

# 4. Construct the Prompt
prompt = f"""
You are a personalized AI fashion stylist.
Analyze the following user context (occasion, weather, preferences) and the provided wardrobe JSON dataset.

User Context:
{user_context}

Wardrobe Dataset:
{json.dumps(wardrobe_data, indent=2)}

Instructions:
1. Read through the wardrobe JSON. For any brand (e.g., "Snitch") or product descriptions that lack detail, USE the Google Search tool during your thinking process to find the brand's aesthetic, typical sizing/fit, and style rules to gain deeper insight.
2. Formulate outfit recommendations that strictly match the user context.
3. Use layering if the weather or occasion calls for it.
4. Return the recommendations strictly matching the requested JSON schema.
"""

# 5. Define Payload with Structured Outputs Schema (Forces a 2D Array Output)
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    # ADD THE TOOLS OPTION HERE
    "tools": [],
    # "tools": [{"googleSearch": {}}],
    "generationConfig": {
        "responseMimeType": "application/json",
        "responseSchema": {
            "type": "OBJECT",
            "properties": {
                "outfits": {
                    "type": "ARRAY",
                    "description": "A 2D array of clothing IDs forming complete outfits.",
                    "items": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                    },
                }
            },
            "required": ["outfits"],
        },
    },
}

headers = {"Content-Type": "application/json"}

# 6. Execute Request
response = requests.post(URL, headers=headers, json=payload)

# 7. Output Result
if response.status_code == 200:
    result = response.json()
    # Extract the structured text response and parse it back to a Python dict
    text_response = result["candidates"][0]["content"]["parts"][0]["text"]
    structured_data = json.loads(text_response)

    # This contains the pure 2D array
    outfits_2d_array = structured_data["outfits"]

    print("Recommended Outfits (2D Array of IDs):")
    print(outfits_2d_array)
else:
    print(f"Error {response.status_code}: {response.text}")