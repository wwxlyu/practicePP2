# config.py
import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    # Helper to find the file in the same folder as this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    parser = ConfigParser()
    parser.read(file_path)

    config_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            config_params[p[0]] = p[1]
    else:
        print(f"File {filename} or section {section} not found!")
        
    return config_params