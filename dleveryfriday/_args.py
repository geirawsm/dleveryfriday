#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()

handling_args = parser.add_argument_group('Handling')
handling_args.add_argument('--delete-scheduled', '-ds',
                           help='Delete all scheduled posts',
                           action='store_true',
                           default=False,
                           dest='delete_scheduled')
handling_args.add_argument('--list-scheduled', '-ls',
                           help='List all scheduled posts',
                           action='store_true',
                           default=False,
                           dest='list_scheduled')
handling_args.add_argument('--reschedule', '-r',
                           help='Reschedule a post: 1st param is post_id, '
                                '2nd param is new_date (dd.mm.yyyy), 3rd '
                                'param is new_time (hh.mm)',
                           nargs=3,
                           default=None,
                           dest='reschedule')

logging_args = parser.add_argument_group('Logging')
logging_args.add_argument('--log', '-l',
                          help='Log important messages',
                          action='store_true',
                          default=False,
                          dest='log')
logging_args.add_argument('--log-more', '-lm',
                          help='Log absolutely everything',
                          action='store_true',
                          default=False,
                          dest='log_more')
logging_args.add_argument('--log-print', '-lp',
                          help='Print logging instead of writing to file',
                          action='store_true',
                          default=False,
                          dest='log_print')
logging_args.add_argument('--debug', '-d',
                          help='Log debug info',
                          action='store_true',
                          default=False,
                          dest='debug')
logging_args.add_argument('--highlight', '-hl',
                          help='Highlight chosen text in logging function naming',
                          action='store',
                          default=None,
                          dest='log_highlight')

testing_args = parser.add_argument_group('Testing')
testing_args.add_argument('--test', '-t',
                          help='Post messages as unlisted',
                          action='store_true',
                          default=False,
                          dest='test')
testing_args.add_argument('--dry-run', '-dr',
                          help='Only print what the action is doing',
                          action='store_true',
                          default=False,
                          dest='dryrun')
testing_args.add_argument('--force-friday', '-ff',
                          help='Force the script to believe it\'s a Friday',
                          action='store_true',
                          default=False,
                          dest='forcefriday')
args, unknown = parser.parse_known_args()


if __name__ == "__main__":
    pass
