import base64
import os

from Crypto.Util.Padding import pad


config = {
    'original_folder': "./Closet",  # Change this to your path
    'output_folder': "./Encrypted",  # Change this to your path
    'log_level': 'INFO',
    'media_json_input': 'original/media.json',
    'media_json_output': 'pages/media.json',
    'process_md': True
}

def change_dir_to_current_file():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
change_dir_to_current_file()
print(os.getcwd())

import os
import json
import base64


def encode_json_folder(folder_path, output_file):
    combined_data = {}

    # Iterate through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Load JSON to ensure it is valid
                    json_data = json.load(f)

                    # Convert JSON object back to a compact string and encode to base64
                    json_string = json.dumps(json_data, separators=(',', ':'))
                    encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
                    encoded_string = encoded_bytes.decode('utf-8')

                    # Store using the filename as the key
                    combined_data[filename] = encoded_string
            except (json.JSONDecodeError, IOError) as e:
                print(f"Skipping {filename}: {e}")

    # Write the combined dictionary to the output file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(combined_data, out_f, indent=4)

encode_json_folder(config['original_folder'], os.path.join(config['output_folder'], "media.json"))