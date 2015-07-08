# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import sys


DOMAIN = 'http://info.kingcounty.gov/'
PATH = 'health/ehs/foodsafety/inspections/Results.aspx'
PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'B'
}


def get_inspection_page(**kwargs):
    url = DOMAIN + PATH
    params = PARAMS.copy()
    for k, v in kwargs.items():
        if k in PARAMS:
            params[k] = v

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.content, response.encoding


def load_inspection_page():
    with open('inspection_page.html', 'rb') as data:
        encoded_data = data.read()
        return encoded_data, 'utf-8'


def parse_source(data, encoding='utf-8'):
    soup_data = BeautifulSoup(data, 'html5lib', from_encoding=encoding)
    return soup_data


def extract_data_listings(soup):
    import re
    id_info = re.compile(r'PR0.*~')
    divs = soup.find_all('div', id=id_info)
    return divs


def has_two_tds(element):
    tr = element.name == 'tr'
    tds = element.find_all('td', recursive=False)
    has_two = len(tds) == 2
    return tr and has_two


def clean_data(cell):
    data = cell.string
    try:
        return data.strip(' \n:-')
    except AttributeError:
        return u''


def extract_restaurant_metadata(element):
    metadata_rows = element.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key, val = row.find_all('td', recursive=False)
        new_label = clean_data(key)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val))
    return rdata


def is_inspection_row(element):
    tr = element.name == 'tr'
    if not tr:
        return False
    td_child = element.find_all('td', recursive=False)
    has_four = len(td_child) == 4
    this_text = clean_data(td_child[0]).lower()
    contains_word = 'inspection' in this_text
    does_not_start = not this_text.startswith('inspection')
    return tr and has_four and contains_word and does_not_start


def extract_score_data(element):
    inspected = element.find_all(is_inspection_row)
    samples = len(inspected)
    total = high_score = average = 0
    for row in inspected:
        strval = clean_data(row.find_all('td')[2])
        try:
            intval = int(strval)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += intval
            high_score = intval if intval > high_score else high_score
    if samples:
        average = total / float(samples)
    data = {
        u'Average Score': average,
        u'High Score': high_score,
        u'Total Inspections': samples
    }
    return data


def generate_results(test=False):
    if len(sys.argv) > 1 and sys.argv[1] == "Test":
        c, e = load_inspection_page()
    else:
        c, e = get_inspection_page(
            Zip_Code='98109',
            Inspection_Start='1/1/2015'
        )
    soup = parse_source(c, e)
    listings = extract_data_listings(soup)
    for listing in listings:
        meta_data = extract_restaurant_metadata(listing)
        score_data = extract_score_data(listing)
        meta_data.update(score_data)
        yield meta_data


if __name__ == '__main__':
    test = len(sys.argv) > 1 and sys.argv[1] == 'test'
    for result in generate_results(test):
        print result
