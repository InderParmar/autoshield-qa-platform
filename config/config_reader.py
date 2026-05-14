"""
config_reader.py
Parses config/config.ini and exposes all settings as importable constants.
All other modules import from here — zero hardcoded values anywhere else.
"""
import os
import configparser

# Initialise the parser
config = configparser.ConfigParser()

# Resolve config.ini path relative to this file — works regardless of working directory
current_dir = os.path.dirname(__file__)
ini_path = os.path.join(current_dir, 'config.ini')
config.read(ini_path)

# ── ParaBank URLs ──────────────────────────────────────────────────────────────
BASE_URL     = config.get('settings', 'base_url')
API_BASE_URL = config.get('settings', 'api_base_url')

# ── Test credentials ───────────────────────────────────────────────────────────
# USERNAME/PASSWORD are the base values used when generating the session user
# WRONG_* values are used exclusively in negative login test cases
USERNAME       = config.get('credentials', 'username')
PASSWORD       = config.get('credentials', 'password')
WRONG_USERNAME = config.get('credentials', 'wrong_username')
WRONG_PASSWORD = config.get('credentials', 'wrong_password')

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL       = config.get('logging', 'log_level')
LOG_FORMAT      = config.get('logging', 'log_format', raw=True)
LOG_DATE_FORMAT = config.get('logging', 'log_datefmt', raw=True)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCREENSHOT_DIR = config.get('paths', 'screenshot_dir')
LOGS_DIR       = config.get('paths', 'log_dir')
REPORTS_DIR    = config.get('paths', 'report_dir')