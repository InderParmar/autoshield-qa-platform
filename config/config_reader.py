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

# ── PARABANK URL ───────────────────────────────────────────────────────────────
BASE_URL = config.get('settings','base_url')
API_BASE_URL = config.get('settings','api_base_url')

# ── PARABANK URL AND CREDENTIALS ───────────────────────────────────────────────

USERNAME = config.get('credentials','username')
PASSWORD = config.get('credentials','password')

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL       = config.get('logging', 'log_level')
LOG_FORMAT      = config.get('logging', 'log_format',  raw=True)
LOG_DATE_FORMAT = config.get('logging', 'log_datefmt', raw=True)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCREENSHOT_DIR = config.get('paths', 'screenshot_dir')
LOGS_DIR       = config.get('paths', 'log_dir')
REPORTS_DIR    = config.get('paths', 'report_dir')

