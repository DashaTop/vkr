#!/usr/bin/env python
# coding: utf-8

import re

number_regex = re.compile(r'[\d\.]+')

def contains(d, value):
    return d('span:Contains("{0}")'.format(value))

def extract_number(d, value):
    global number_regex

    result = contains(d, value).parent()

    if len(result) == 0:
        return None

    return float(number_regex.findall(result.text())[0])

def extract_string(d, value):
    return contains(d, value).parent().text().replace(value, '')