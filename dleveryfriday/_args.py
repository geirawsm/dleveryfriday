#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()

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
logging_args.add_argument('--log-slow', '-ls',
                          help='Wait 3 seconds after each logging',
                          action='store_true',
                          default=False,
                          dest='log_slow')
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
args, unknown = parser.parse_known_args()


if __name__ == "__main__":
    pass
