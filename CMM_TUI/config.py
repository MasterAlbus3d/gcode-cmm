"""
Configuration Module

This module loads and validates settings from settings.json.
"""

import json
import os

CONFIG_FILE = "settings.json"

def load_settings():
    """
    Loads settings from settings.json and returns them as a dictionary.
    
    Raises:
        FileNotFoundError: If the settings.json file does not exist.
        json.JSONDecodeError: If the file contents are not valid JSON.
        
    Returns:
        dict: Dictionary of configuration settings.
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found.")
    with open(CONFIG_FILE, 'r') as f:
        settings = json.load(f)
    return settings
