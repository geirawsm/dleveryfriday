#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'Set variables for the module like folder, files and botlines'

from pathlib import Path

# Folders
ROOT_DIR = Path(__file__).resolve().parent
STATIC_DIR = ROOT_DIR / 'static'
JSON_DIR = ROOT_DIR / 'json'

# Files
env_file = ROOT_DIR / '.env'
friday_vid = STATIC_DIR / 'friday.mp4'
yt_log = JSON_DIR / 'yt_log.json'
post_log = JSON_DIR / 'post_log.json'

# URLs
dlt_rss = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCDLD_zxiuyh1IMasq9nbjrA'

# Template content
yt_log_template = '''{
    "ids": [],
    "last_search": {
        "date": false,
        "epoch": false
    }
}'''
post_log_template = '''{
    "last_post_date": false,
    "last_post_epoch": false
}'''


if __name__ == "__main__":
    pass
