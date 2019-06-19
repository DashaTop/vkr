#!/usr/bin/env python
# coding: utf-8

import os
import hashlib

cache_path = 'cache_files'

if (not os.path.exists(cache_path)):
    os.mkdir(cache_path)

def getMD5(cache_name):
    return hashlib.md5(bytes(cache_name, 'utf-8')).hexdigest()

def get_cache(cache_name):
    md5 = getMD5(cache_name)
    path = '{0}/{1}.html'.format(cache_path, md5)

    if os.path.isfile(path):
        return open(path, 'r', encoding='utf-8').read()

    return None

def set_cache(cache_name, cache):
    md5 = getMD5(cache_name)
    path = '{0}/{1}.html'.format(cache_path, md5)

    open(path, 'w', encoding='utf-8').write(cache)