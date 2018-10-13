import requests
from werkzeug.contrib.cache import SimpleCache


c = SimpleCache()

COUNTRY_ENDPOINT = 'https://restcountries.eu/rest/v2/all'


def get_countries():
    cached = c.get('countries')
    if cached:
        return cached
    countries = requests.get(COUNTRY_ENDPOINT).json()
    c.set('countries', countries)
    return countries
