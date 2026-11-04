import json
import os

# Carga la configuracion
def load_config():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "config.json")
    
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)