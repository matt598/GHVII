from typing import Union, List
import requests
from werkzeug.contrib.cache import SimpleCache


c = SimpleCache()

COUNTRY_ENDPOINT = 'https://restcountries.eu/rest/v2/all'


def get_countries() -> List[dict]:
    cached = c.get('countries')
    if cached:
        return cached
    countries = requests.get(COUNTRY_ENDPOINT).json()
    c.set('countries', countries)
    return countries


def country_for_code(code: Union[int, str]) -> List[dict]:
    if isinstance(code, int):
        code = str(code)

    countries = []

    for country in get_countries():
        callingCodes = country.get('callingCodes')
        if not callingCodes:
            continue

        if code in callingCodes:
            countries.append(country)

    return countries
