#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from mastodon import Mastodon
from time import sleep

from dleveryfriday._args import args
from dleveryfriday import _config, rss, _vars, file_io, datetimefuncs
from dleveryfriday.log import log

import sys


# Ensure that the log files exist
log.log(f'Ensuring file `{_vars.yt_log}`')
file_io.ensure_file(_vars.yt_log, file_template=_vars.yt_log_template)
log.log(f'Ensuring file `{_vars.post_log}`')
file_io.ensure_file(_vars.post_log, file_template=_vars.post_log_template)

m_auth = Mastodon(
    access_token=_config.config['token'],
    api_base_url=_config.config['base_url']
)


def post(text, media_ids=None):
    if args.test:
        post = m_auth.status_post(text, visibility='unlisted')
    elif args.dryrun:
        print(f'Posting: `{text}`')
        post = None
    else:
        if media_ids is not None:
            post = m_auth.status_post(
                text, media_ids=media_ids
            )
        else:
            post = m_auth.status_post(text)
    return post


def get_media(file):
    post = m_auth.media_post(str(file), mime_type='video/mp4')
    return post


def reply(post_reply, text):
    if args.test:
        reply = m_auth.status_post(
            text, in_reply_to_id=post_reply['id'], visibility='unlisted'
        )
    elif args.dryrun:
        print(f'Replying: `{text}`')
        reply = None
    else:
        reply = m_auth.status_post(text, in_reply_to_id=post_reply['id'])
    return reply


def log_posted_date_now():
    post_log = file_io.read_json(_vars.post_log)
    date_now = datetimefuncs.get_dt('date')
    date_now_epoch = datetimefuncs.get_dt()
    post_log['last_post_date'] = date_now
    post_log['last_post_epoch'] = date_now_epoch
    file_io.write_json(_vars.post_log, post_log)


if __name__ == "__main__":
    post_log = file_io.read_json(_vars.post_log)
    date_now = datetimefuncs.get_dt()
    if post_log['last_post_epoch'] is False:
        log_posted_date_now()
        post_log = file_io.read_json(_vars.post_log)
    # If today is friday and there already is a post with the video,
    # skip posting
    if date_now > post_log['last_post_epoch']:
        log_posted_date_now()
        req = rss.get_link(_vars.dlt_rss)
        video_link = rss.get_videos(req)
        if video_link is not None:
            first_post = post('', media_ids=_vars.friday_vid)
            sleep(2)
            second_post = reply(first_post, f'Catch David Lynch\'s Weather Reports: {video_link}')
            log_posted_date_now()
