import base64
import json

import requests
LOG_LEVEL = "INFO"


def get_media(buffer = 5):
    media_json_path = "../media.json"
    with open(media_json_path, "r", encoding="utf-8") as f:
        media_json_data = json.load(f)
    if LOG_LEVEL == "DEBUG":
        print(len(media_json_data))

    metadata_json_path = "../metadata.json"
    with open(metadata_json_path, "r", encoding="utf-8") as f:
        metadata_json_data = json.load(f)

    cloth_array = []

    for item in media_json_data:
        if item not in metadata_json_data:
            cloth_array.append([item, media_json_data[item]["type"]])
            if len(cloth_array) == buffer:
                break
    return cloth_array

def get_clothing_encoded(clothing_item_id, clothing_item_type):
    # 1. Grab your API key and set the endpoint

    # os.environ.get("GEMINI_API_KEY")
    # api_key = ""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
    # 2. Convert your local image file to a base64 string
    image_path = "F:/Git/XCloset/media/clothes/" + clothing_item_id + ".png"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    payload_text = '''
    You are an expert fashion data-entry assistant. Your job is to analyze an image of a clothing item and convert it into a strictly structured JSON object based on the provided schema.
    
    ### User Context Indicator:
    The user says: The clothing in question is the {USER_CONTEXT}
    Use this statement to isolate the correct clothing item if the image contains multiple items, background clutter, or if the user is wearing the outfit. Focus ONLY on the item they specify.
    
    ### JSON Schema:
    Output MUST be a single, raw JSON object matching this exact format. Do not include markdown code blocks, do not include explanations. Only return the JSON.
    
    {
      "id": "Generate a unique short string ID, e.g., top_01, bottom_12, shoe_03",
      "category": "Must be exactly one of: top, bottom, outerwear, footwear, accessory",
      "sub_category": "e.g., t-shirt, button-down, jeans, chinos, boots, sneakers, blazer",
      "color": "Primary dominant color name in lowercase (e.g., navy_blue, olive_green, white, charcoal)",
      "pattern": "Must be exactly one of: solid, striped, plaid, graphic, floral, textured, distressed",
      "fabric": "Estimate the fabric type based on texture (e.g., denim, cotton_jersey, linen, wool, leather, canvas, knit). If impossible to tell, use 'unknown'",
      "fit": "Must be exactly one of: skinny, slim, straight, relaxed, oversized, cropped",
      "formality": 1, // Integer from 1 to 5: 1 (Athletic/Sleepwear), 2 (Casual/Streetwear), 3 (Smart Casual), 4 (Business Casual), 5 (Formal/Black Tie)
      "tags": ["A list of 2 to 4 lowercase descriptive tags, e.g., 'summer', 'breathable', 'streetwear', 'cozy', 'minimalist'"],
      "description": "A one to two line description giving more context and details missed in the schema fields"
    }
    
    ### Extraction Rules:
    1. Objectiveness: Base your categorization on visual evidence. If a shirt looks loose and baggy, the fit is "oversized" or "relaxed".
    2. Formality Guide: Be consistent. Standard blue jeans are a 2. Dark crisp chinos are a 3. A wool blazer is a 4. A graphic t-shirt is a 2.
    3. Strictness: Do not add any keys to the JSON that are not defined in the schema above.
    '''

    payload_text = payload_text.replace("{USER_CONTEXT}", clothing_item_type)

    # 3. Construct the standard JSON payload
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": payload_text},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }

    # 4. Make the raw POST call
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    # 5. Parse out the text result
    if response.status_code == 200:
        result = response.json()
        text_response = result["candidates"][0]["content"]["parts"][0]["text"]
        print('"' + clothing_item_id + '"' + " : " + text_response)
    else:
        print(f"Error {response.status_code}: {response.text}")

clothing = get_media(15)
for clothing_item in clothing:
    clothing_item_id = clothing_item[0]
    clothing_item_type = clothing_item[1]
    get_clothing_encoded(clothing_item_id, clothing_item_type)
    print(",")

