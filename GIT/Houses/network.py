#!/usr/bin/env python
# coding: utf-8

import json
import requests

search_api_url = 'https://dom.gosuslugi.ru/homemanagement/api/rest/services/houses/public/searchByAddress'
wall_api_url = 'https://dom.gosuslugi.ru/homemanagement/api/rest/services/houses/public/1/'

request_headers = {
    'content-type': 'application/json; charset=utf8'
}

request_params = {
    'pageIndex': '1',
    'elementsPerPage': '1'
}

request_body = json.dumps({
    'regionCode': 'a84b2ef4-db03-474b-b552-6229e801ae9b',
    'cityCode': '6b1bab7d-ee45-4168-a2a6-4ce2880d90d3',
    'fiasHouseCodeList': None,
    'estStatus': None,
    'strStatus': None,
    'calcCount': True,
    'houseConditionRefList': None,
    'houseTypeRefList': [
        '1'
    ],
    'houseManagementTypeRefList': None,
    'cadastreNumber': None,
    'oktmo': None,
    'onlyDemolishedHouses': False
})

def request_with_params(params):
    return requests.post(
        search_api_url,
        headers=request_headers,
        data=request_body,
        params=params
    ).json()

def get_houses():
    total = request_with_params(request_params)['total']
    items = []
    page = 1
    housesPerPage = 1000

    while (total > page * housesPerPage):
        request_params['pageIndex'] = str(page)
        request_params['elementsPerPage'] = str(housesPerPage)

        items += request_with_params(request_params)['items']

        page += 1
    
    return items

def get_wall_type(house_guid):
    return requests \
        .get(wall_api_url + house_guid) \
        .json()['intWallMaterialList']
