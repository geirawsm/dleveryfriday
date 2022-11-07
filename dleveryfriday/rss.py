#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from dleveryfriday import file_io, _vars, datetimefuncs
from dleveryfriday.log import log

import sys


def get_link(url):
    'Get a requests object from a `url`'
    try:
        req = requests.get(url)
    except (requests.exceptions.InvalidSchema):
        log.log(f'URL has an invalid format: `{url}`')
        return None
    except (requests.exceptions.ConnectionError):
        log.log(f'Got connection error when trying to access `{url}`')
        return None
    return req


def get_videos(req_obj):
    '''
    it should post on a friday, but not before DL has posted a weather
    update on his YT.
    '''
    SHOULD_POST = False
    yt_log = file_io.read_json(_vars.yt_log)
    soup = BeautifulSoup(req_obj.content, features='xml')
    for entry in soup.findAll('entry')[0:10]:
        _title = entry.find('title').text
        _link = entry.find('link')['href']
        _id = entry.find('yt:videoId').text
        _date = entry.find('published').text
        log.log(f'Got video: `{_title}` ({_id})', color='magenta')
        # Check if already logged
        if _id not in yt_log['ids']:
            log.log(f'This is a new video ✅')
            SHOULD_POST = True
        else:
            log.log(f'Video already logged ❎')
            SHOULD_POST = False
            continue
        # Check if posting is on a friday
        date_day_in_week = datetimefuncs.get_dt(
            format='dayofweek', dt=_date
        )
        log.log(f'Date published is `{_date}` ({date_day_in_week})')
        if date_day_in_week == '5':
            log.log(f'Date is a friday ✅')
            SHOULD_POST = True
        else:
            log.log(f'Date is not a friday ❎')
            SHOULD_POST = False
            continue
        # Check if posting is today
        post_date = datetimefuncs.get_dt(format='date', dt=_date)
        now_date = datetimefuncs.get_dt(format='date')
        if post_date == now_date:
            log.log(f'The video is posted today ✅')
            SHOULD_POST = True
        else:
            log.log(f'The video is old ❎')
            SHOULD_POST = False
            continue
        # Check if it's a "weather report" video
        ratio = file_io.check_similarity(
            'David Lynch\'s Weather Report', _title
        )
        log.log(f'Video title has a {ratio} similarity ratio')
        if ratio > 0.8:
            log.log(f'Ratio is good ✅')
            SHOULD_POST = True
        else:
            log.log(f'Ratio is not good ❎')
            SHOULD_POST = False
            continue
        yt_log['ids'].append(_id)
        yt_log['last_search']['date'] = datetimefuncs.get_dt(format='date')
        yt_log['last_search']['epoch'] = datetimefuncs.get_dt()
        file_io.write_json(_vars.yt_log, yt_log)
    if SHOULD_POST:
        return _link
    else:
        return None


if __name__ == "__main__":
    req = get_link(_vars.dlt_rss)
    video = get_videos(req)
    print(video)
