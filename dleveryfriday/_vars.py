#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'Set variables for the module like folder, files and botlines'

from pathlib import Path

# Folders
ROOT_DIR = Path(__file__).resolve().parent
STATIC_DIR = ROOT_DIR / 'static'
JSON_DIR = ROOT_DIR / 'json'
LOGS_DIR = ROOT_DIR / 'logs'

# Files
env_file = ROOT_DIR / '.env'
friday_vid = STATIC_DIR / 'dleveryfriday.mp4'
post_log = JSON_DIR / 'post_log.json'


# Template content
post_log_template = '''{
    "last_post_date": false,
    "last_post_epoch": false
}'''


if __name__ == "__main__":
    pass
