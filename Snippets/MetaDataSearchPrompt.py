import json
import pyperclip

file_path = "wardrobe.json"
prompt_path = "snippets/ClothMetaDataPrompt.txt"

# 1. Read the original data
with open(file_path, "r", encoding="utf-8") as f:
    wardrobe = json.load(f)

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

for item in sorted(wardrobe):
    clothing = wardrobe[item]
    if "color" not in wardrobe[item]["metadata"]:
        print(item)
        prompt = prompt.replace("{CLOTHTYPE}", clothing["type"]).replace("{BRANDNAME}", clothing["brand"])
        pyperclip.copy(prompt)
        print("Text copied to clipboard!")
        # print(prompt)
        break
