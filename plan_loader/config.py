"""
Simple config for useful constants
"""

import pathlib

HSE_BASIC_URL = 'https://asav.hse.ru/basicplans.html?faculty=&regdepartment='
HSE_ANNUAL_URL = 'https://asav.hse.ru/plans.html?login=web&password=web'

ITMO_PLANS_URL = 'https://abitlk.itmo.ru/api/v1/programs/short?limit=300'
ITMO_PROGRAM_URL = 'https://abit.itmo.ru/_next/data/PyEfeC8TAzZTl_mT-rjFm/ru/program/%s/%s.json'

DEFAULT_DOWNLOAD_PATH = str(pathlib.Path.home() / 'Desktop' / 'Plans')