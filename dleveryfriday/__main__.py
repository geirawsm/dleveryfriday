#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from mastodon import Mastodon
from time import sleep

from dleveryfriday._args import args
from dleveryfriday import _config, _vars, file_io, datetimefuncs
from dleveryfriday.log import log

import sys

# Ensure that the log files exist
log.log(f'Ensuring file `{_vars.post_log}`')
file_io.ensure_file(_vars.post_log, file_template=_vars.post_log_template)

m_auth = Mastodon(
    access_token=_config.config['token'],
    api_base_url=_config.config['base_url']
)

def post(text, media_ids=None):
    if args.test:
        post = m_auth.status_post(text, visibility='direct')
    elif args.dryrun:
        print(f'Posting: `{text}`')
        post = None
    else:
        if media_ids is not None:
            if args.test:
                post = m_auth.status_post(
                    text, media_ids=media_ids, visibility='direct'
                )
            else:
                post = m_auth.status_post(
                    text, media_ids=media_ids
                )
        else:
            post = m_auth.status_post(text)
    return post

def get_media(file):
    log.log('Uploading media...')
    post = m_auth.media_post(str(file), mime_type='video/mp4')
    log.log(f'Done: {post}')
    return post

def log_posted_date_now():
    post_log = file_io.read_json(_vars.post_log)
    date_now = datetimefuncs.get_dt('date')
    date_now_epoch = datetimefuncs.get_dt()
    post_log['last_post_date'] = date_now
    post_log['last_post_epoch'] = date_now_epoch
    if not args.dryrun:
        file_io.write_json(_vars.post_log, post_log)
    else:
        log.log('Dry run: writing `post_log` to `_vars.post_log`')


if __name__ == "__main__":
    post_log = file_io.read_json(_vars.post_log)
    date_now = datetimefuncs.get_dt()
    if not args.dryrunforce:
        dow = datetimefuncs.get_dt('dayofweek')
        log.debug(f'Got day of week: {dow}')
    else:
        dow = 5
        log.debug('`dryrunforce`: Forced a friday')
    if post_log['last_post_epoch'] is False:
        log_posted_date_now()
        post_log = file_io.read_json(_vars.post_log)
    # If today is friday and there already is a post with the video,
    # skip posting
    # It's friday, my dudes
    if int(dow) != 5:
        log.log('Today is not a friday')
    elif int(dow) == 5:
        log.debug('Today is a new friday! Posting video')
        _media = get_media(_vars.friday_vid)
        print(f'_media: {_media}')
        sleep(5)
        _post = post(
            'It\'s friday!',
            media_ids=_media.id
        )
        print(f'_post: {_post}')
        log_posted_date_now()
