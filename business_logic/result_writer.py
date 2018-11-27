import json

def create_json(output_path, data):
    with open(output_path, 'w') as file:
        json.dump(data, file)