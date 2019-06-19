#!/usr/bin/env python
# coding: utf-8

import csv
from network import get_houses, get_wall_type

field_header = ['address', 'year', 'type']
houses = get_houses()

with open('houses.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_header, delimiter=';')
    writer.writeheader()

    for house in houses:
        address = house['address']['formattedAddress']
        addressId = house['guid']
        year = house['buildingYear']

        if (year is not None):
            writer.writerow({
                'address': address,
                'year': year,
                'type': get_wall_type(addressId)
            })
