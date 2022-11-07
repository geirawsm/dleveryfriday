#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import stat
import json

from difflib import SequenceMatcher

from dleveryfriday.log import log
import pathlib


def write_file(filename, content_to_write):
    'Write `content_to_write` to the file `filename`'
    if not isinstance(filename, str):
        filename = str(filename)
    ensure_file(filename)
    with open(filename, 'w') as fout:
        fout.write(str(content_to_write))
        return True


def import_file_as_list(file_in):
    '''
    Open `file_in`, import it as a list and return ut.
    If this fails, return None.
    '''
    file_in = str(file_in)
    ensure_file(file_in, '[]')
    try:
        with open(file_in, 'r', encoding='utf-8') as f:
            list_out = eval(str(f.read()))
        return list_out
    except:
        log.log(f"Couldn't open file `{file_in}`")
        return None


def add_to_list(list_file_in, item_add):
    'Add `item_add` to a list in file `list_file_in`'
    list_file_in = str(list_file_in)
    if not isinstance(item_add, (str, float, int)):
        return None
    ensure_file(list_file_in, '[]')
    opened_list = import_file_as_list(list_file_in)
    opened_list.append(item_add)
    write_file(list_file_in, str(opened_list))
    return opened_list


def read_json(json_file):
    '''
    Open `json_file` as a JSON and convert to as a dict.
    Returns _file as a dict or an empty dict.
    '''
    ensure_file(json_file, '{}')
    try: 
        with open(json_file) as f:
            return dict(json.load(f))
    except json.JSONDecodeError as e:
        log.log(f"Error when reading json from {json_file}:\n{e}")
    except OSError as e:
        log.log(f"File can't be read {json_file}:\n{e}")
    return None


def write_json(json_file, json_out):
    'Write `json_out` to `json file`'
    with open(json_file, 'w') as write_file:
        json.dump(json_out, write_file)


def file_size(filename):
    '''
    Checks the file size of a file. If it can't find the file it will
    return False
    '''
    try:
        _stats = os.stat(filename, follow_symlinks=True)
        return _stats[stat.ST_SIZE]
    except(FileNotFoundError):
        return False


def ensure_file(file_path: str, file_template=False):
    '''
    Create file `file_path` if it doesn't exist and include the
    `file_template` if provided.
    '''
    file_path = str(file_path)
    # Make the folders if necessary
    if not os.path.exists(file_path):
        try:
            _dirs = str(file_path).split(os.sep)[0:-1]
            _path = ''
            for _dir in _dirs:
                _path += '{}/'.format(_dir)
            pathlib.Path(_path).mkdir(parents=True, exist_ok=True)
        except:
            pass
    # Ooooh, this is a scary one. Don't overwrite the file unless it's empty
    log.log_more('{} size: {}'.format(file_path, file_size(file_path)))
    # Create the file if it doesn't exist
    if not file_size(file_path):
        log.log_more('File not found, creating: {}'.format(file_path))
        with open(file_path, 'w+') as fout:
            if file_template:
                fout.write(file_template)
            else:
                fout.write('')


def check_similarity(text1: str, text2: str) -> bool:
    '''
    Check how similar `text1` and `text2` is and represent it with a ratio.
    If neither `text1` nor `text2` is a string, it will return None.
    '''
    # Stop function if input is not str
    if type(text1) is not str or type(text2) is not str:
        return None
    ratio = float(SequenceMatcher(a=text1,b=text2).ratio())
    return ratio


if __name__ == "__main__":
    pass