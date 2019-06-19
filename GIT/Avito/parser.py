#!/usr/bin/env python
# coding: utf-8

import csv
import helpers
from tqdm import tqdm
from helpers import network
from pyquery import PyQuery as pq

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
    'region'
]

pbar = tqdm(total=5000)

with open('flat.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';')
    writer.writeheader()

    id = 1
    page = network.get_next_page()

    while (page is not None):
        d = pq(page)

        links = d('.item-description-title-link')
        prices = d('span.price')
        regions = d('p.address')

        for i in range(links.length):
            link = d(links[i]).attr('href')
            price = int(d(prices[i]).attr('content'))
            region = ' '.join(d(regions[i]).text().split(',')[0].split(' ')[1:])

            flat = d(network.get_flat('https://avito.ru' + link))

            area = helpers.extract_number(flat, 'Общая площадь')
            floor = int(helpers.extract_number(flat, 'Этаж'))
            max_floor = int(helpers.extract_number(flat, 'Этажей в доме'))

            address = flat('span[itemprop="streetAddress"]').text()
            build_type = flat('a.js-breadcrumbs-link.js-breadcrumbs-link-interaction').contents()[-1]

            rooms = helpers.extract_string(flat, 'Количество комнат: ').strip().split('-')[0]

            wall_type = helpers.extract_string(flat, 'Тип дома: ')

            id += 1
            pbar.update()

            writer.writerow({
                'id': id,
                'price': price,
                'area': area,
                'floor': floor,
                'max_floor': max_floor,
                'address': address,
                'type': build_type,
                'wall_type': wall_type,
                'rooms': rooms,
                'region': region
            })

        page = network.get_next_page()

pbar.close()