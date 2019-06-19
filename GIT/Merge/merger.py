#!/usr/bin/env python
# coding: utf-8

import csv

header = [
    'id',
    'price',
    'area',
    'floor',
    'max_floor',
    'address',
    'type',
    'wall_type',
    'rooms',
    'region',
    'year'
]

flats_csv = open('flat.csv', 'r', newline='', encoding='utf-8')
houses_csv = open('houses.csv', 'r', newline='', encoding='utf-8')

flats_reader = csv.DictReader(flats_csv, delimiter=';')
houses_reader = csv.DictReader(houses_csv, delimiter=';')

addresses_dict = [{ 'address': house['address'][38:], 'year': house['year'] } for house in houses_reader]

def search_year(address):
    address = address.lower()
    number = address.split(', ')[-1] \
        .replace('д.', '') \
        .strip() \
        .lower()

    for item in addresses_dict:
        street = item['address'] \
            .split('д.')[0] \
            .strip()[:-1] \
            .replace('п ', '') \
            .replace('пер ', '') \
            .replace('ул ', '') \
            .replace('проезд ', '') \
            .lower()
        
        house_number = item['address'].split('д.')[1].strip()
        
        if street in address and house_number == number:
            return item['year']

    return None

with open('output.csv', 'w', newline='', encoding='utf-8') as output:
    writer = csv.DictWriter(output, delimiter=';', fieldnames=header)
    writer.writeheader()

    for flat in flats_reader:
        address = flat['address']
        year = search_year(address)

        writer.writerow({
            'id': int(flat['id']) - 1,
            'price': flat['price'],
            'area': flat['area'],
            'floor': flat['floor'],
            'max_floor': flat['max_floor'],
            'address': flat['address'],
            'type': flat['type'],
            'wall_type': flat['wall_type'],
            'rooms': flat['rooms'],
            'region': flat['region'],
            'year': year
        })
