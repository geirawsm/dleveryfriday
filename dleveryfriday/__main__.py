#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from mastodon import Mastodon
from time import sleep
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random
from tabulate import tabulate

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


def update_scheduled_post(post_id, new_date, new_time):
    # TODO Denne må utbedres
    _sched = datetimefuncs.make_dt(f'{new_date} {new_time}')
    print(type(_sched))
    print(_sched)
    rescheduled = m_auth.scheduled_status_update(
        id=post_id, scheduled_at=_sched
    )
    print(rescheduled)


def list_scheduled_posts():
    scheduled_posts = m_auth.scheduled_statuses()
    if len(scheduled_posts) > 0:
        log.debug('Listing scheduled posts...')
        posts = {
            'id': [],
            'scheduled': [],
            'text': [],
            'attachment': []
        }
        for post in scheduled_posts:
            posts['id'].append(post['id'])
            posts['scheduled'].append(post['scheduled_at'])
            posts['text'].append(post['params']['text'])
            posts['attachment'].append(
                'Yes' if len(post['media_attachments']) > 0 else 'No'
            )
        print(
            tabulate(
                posts, headers=['ID', 'Scheduled at', 'Post', 'Attachment?'],
                numalign='center'
            )
        )
    else:
        print('No scheduled posts to list')


def delete_all_scheduled_posts():
    scheduled_posts = m_auth.scheduled_statuses()
    if len(scheduled_posts) > 0:
        for post in scheduled_posts:
            log.log(f'Deleting post {post.id}')
            m_auth.scheduled_status_delete(post.id)
        log.log('Done')


def post(text, media_ids=None, random_schedule=False):
    if args.test:
        if media_ids is not None:
            post = m_auth.status_post(
                text, media_ids=media_ids, visibility='direct',
            )
        else:
            post = m_auth.status_post(
                text, media_ids=media_ids, visibility='direct'
            )
    elif args.dryrun:
        print(f'Posting: `{text}`')
        post = None
    else:
        if random_schedule:
            random_hour = random.randrange(3)
            random_minute = random.randrange(60)
            schedule = datetime.now().replace(
                tzinfo=ZoneInfo('Europe/Oslo')
            ) + timedelta(
                hours=random_hour+2, minutes=random_minute
            )
            log.debug(f'Posting at {schedule}')
        if media_ids is not None:
            if args.test:
                post = m_auth.status_post(
                    text, media_ids=media_ids, visibility='direct',
                    scheduled_at=schedule if random_schedule else None
                )
            else:
                post = m_auth.status_post(
                    text, media_ids=media_ids,
                    scheduled_at=schedule if random_schedule else None
                )
        else:
            post = m_auth.status_post(text)
    return post


def get_media(file):
    log.log('Uploading media...')
    if args.dryrun:
        log.log('Dry run: Uploading media...')
        return None
    else:
        post = m_auth.media_post(str(file), mime_type='video/mp4')
        log.log(f'Done: {post}')
        return post['id']


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
    if args.delete_scheduled:
        delete_all_scheduled_posts()
        sys.exit()
    if args.list_scheduled:
        list_scheduled_posts()
        sys.exit()

    post_log = file_io.read_json(_vars.post_log)
    date_now = datetimefuncs.get_dt()
    if not args.forcefriday:
        dow = datetimefuncs.get_dt('dayofweek')
        log.debug(f'Got day of week: {dow}')
    else:
        dow = 5
        log.debug('`forcefriday`: Forced a friday')
    if post_log['last_post_epoch'] is False:
        log_posted_date_now()
        post_log = file_io.read_json(_vars.post_log)
    if int(dow) != 5:
        log.log('Today is not a Friday')
    elif int(dow) == 5 or args.post_now:
        # It's friday, my dudes
        log.debug('Today is a new Friday! Posting video')
        _media = get_media(_vars.friday_vid)
        log.debug(f'_media: {_media}')
        sleep(5)
        random_text = [
            "It's Friday!",
            "What do you know - it's Friday once again!",
            "You made it! It's Friday!",
            "Well, look at that - another Friday is here again!"
        ]
        if args.post_now:
            _post = post(
                random_text[random.randint(0, len(random_text)-1)],
                media_ids=_media,
                random_schedule=False
            )
        if not args.post_now:
            _post = post(
                random_text[random.randint(0, len(random_text)-1)],
                media_ids=_media,
                random_schedule=True
            )
        log.debug(f'_post: {_post}')
        log_posted_date_now()
