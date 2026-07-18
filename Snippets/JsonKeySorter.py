import json

file_path = "wardrobe.json"

# 1. Read the original data
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Overwrite the original file with sorted keys
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, sort_keys=True)