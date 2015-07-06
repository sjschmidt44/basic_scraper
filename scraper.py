# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests


DOMAIN = 'http://info.kingcounty.gov/'
PATH = 'health/ehs/foodsafety/inspections/Results.aspx'
PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address'
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
    queryargs = {}
    for k, v in kwargs.iteritems():
        queryargs[k] = v
    for k, v in PARAMS.iteritems():
        queryargs.setdefault(k, v)

    

"""
It must accept keyword arguments for the possible query parameters
It will build a dictionary of request query parameters from incoming keywords
It will make a request to the King County server using this query
It will return the bytes content of the response and the encoding if there is
    no error
It will raise an error if there is a problem with the response
As you work on building this function, try out various approaches in your
    Python interpreter first. See what works and what fails before you try
    to write the function."""
