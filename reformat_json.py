import json
import os

# fixing bad formatting after generating summaries

folder_path = "data"
files = [file for file in os.listdir(folder_path)]

for file in files:
    file_path = os.path.join(folder_path, file)

    with open(file_path, "r") as f:
        nested_data = json.load(f)

    flattened_data = [obj for array in nested_data for obj in array]

    file = file[:-5]
    output_file = f"{file}_ref.json"
    output_file_path = os.path.join(folder_path, output_file)

    with open(output_file_path, "w") as f:
        json.dump(flattened_data, f, indent=4)
