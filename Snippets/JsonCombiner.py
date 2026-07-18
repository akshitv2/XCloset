import json

file_path = "../media.json"
metadata_path = "../metadata.json"

# 1. Read the original data
with open(file_path, "r", encoding="utf-8") as f:
    cloth_data = json.load(f)

with open(metadata_path, "r", encoding="utf-8") as f:
    meta_data = json.load(f)

for i in cloth_data:
    cloth_data[i]["metadata"] = meta_data[i]
    del cloth_data[i]["color"]

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(cloth_data, f, indent=4, sort_keys=True)

print(cloth_data)

