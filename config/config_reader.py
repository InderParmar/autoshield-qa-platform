"""
config_reader.py
Parses config/config.ini and exposes all settings as importable constants.
All other modules import from here - zero harcoded values anywhere else.
"""
import os
import configparser

# Initialize the parser
config = configparser.ConfigParser()

# Resolve config.ini path relative to this file - works regardless of working directory
current_dir = os.path.dirname(__file__) # project/config
ini_path = os.path.join(current_dir, 'config.ini')
config.read(ini_path)

#--PARABANK URL AND CREDENTIALS-----------------------------------------------------------------------------
BASE_URL = config.get('parabank','base_url')
API_BASE_URL = config.get('parabank','api_base_url')
USERNAME = config.get('parabank','username')
PASSWORD = config.get('parabank','password')
