#!/usr/bin/env python
# coding: utf-8

import requests
from time import sleep
from helpers.cache import set_cache, get_cache

flats_url = 'https://www.avito.ru/yaroslavl/kvartiry/prodam'

page = 0

params = {
    'p': '1'
}

def get_next_page(): # Запрос следующей страницы с списком квартир 
    global page
    page += 1
    url = flats_url.format(page)

    params['p'] = str(page)

    if page >= 100:
        return None

    if get_cache(url + '?p={}'.format(page)) is not None:
        return get_cache(url + '?p={}'.format(page))

    response = request(url, params=params)

    set_cache(url + '?p={}'.format(page), response)

    sleep(3)
    return response

def get_flat(url): # Запрос отдельной квартиры
    if get_cache(url) is not None:
        return get_cache(url)

    response = request(url)

    set_cache(url, response)

    sleep(3)
    return response

def request(url, params=None):
    return requests.get(url, params=params).content.decode('utf-8')