#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'Custom logging for the module'
import sys
import os
from colorama import init, Fore, Style
from pathlib import Path
from dleveryfriday import _vars, datetimefuncs
from dleveryfriday._args import args

# colorama specific reset routine
init(autoreset=True)


def log_function(log_in, color=None, sameline=False):
    '''
    Include the name of the function in logging.

    If no `color` is specified, it will highlight in green.
    '''
    get_dt = datetimefuncs.get_dt
    log_out = '[{}] '.format(get_dt(format='datetimefull'))
    if color is None:
        color = Fore.GREEN
    else:
        color = eval('Fore.{}'.format(color.upper()))
    function_name = log_func_name()
    if args.log_highlight is not None:
        if str(args.log_highlight) in function_name:
            color = Fore.RED
    if args.log_print:
        log_out += '{color}{style}[ {function_name} ]{reset} '.format(
            color=color,
            style=Style.BRIGHT,
            reset=Style.RESET_ALL,
            function_name=function_name)
    else:
        log_out += '[ {} ] '.format(log_func_name())
    log_out += log_in
    if args.log_print:
        if sameline:
            try:
                max_cols, max_rows = os.get_terminal_size(0)
            except (OSError):
                max_cols = 0
            msg_len = len(str(log_out))
            rem_len = max_cols - msg_len - 2
            print('{}{}'.format(
                log_out, ' ' * rem_len
            ), end='\r')
        else:
            print(log_out)
    else:
        log_out += '\n'
        _logfilename = _vars.LOGS_DIR / \
            '{}.log'.format(get_dt('revdate', sep='-'))
        write_log = open(_logfilename, 'a+', encoding="utf-8")
        write_log.write(log_out)
        write_log.close()


def log(log_in, color=None, sameline=False):
    '''
    Log the input `log_in`

    Optional: Specify the color for highlighting the function name.

    Available colors: black, red, green, yellow, blue, magenta, cyan, white.
    '''
    if args.log:
        if sameline:
            log_function(log_in, color, sameline=True)
        else:
            log_function(log_in, color, sameline=False)


def log_more(log_in, color=None, sameline=False):
    '''Log the input `log_in`. Used as more verbose than `log`'''
    if args.log_more:
        if sameline:
            log_function(log_in, color, sameline=True)
        else:
            log_function(log_in, color, sameline=False)


def debug(log_in, sameline=False):
    '''Log debugging info. Debug is always yellow'''
    if args.debug:
        if sameline:
            log_function(log_in, 'yellow', sameline=sameline)
        else:
            log_function(log_in, 'yellow')


def log_func_name():
    'Get the function name that the `log`-function is used within'
    frame_file = sys._getframe(2)
    frame_func = sys._getframe(3)
    func_name = frame_func.f_code.co_name
    func_file = frame_file.f_back.f_code.co_filename
    func_file = Path(func_file).stem
    if func_name == '<module>':
        return func_file
    else:
        return '{}.{}'.format(func_file, func_name)
