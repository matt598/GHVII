import unittest

from data import country_for_code


class DataTest(unittest.TestCase):
    def test_country_for_code(self):
        country = country_for_code(93)
        self.assertEqual(country['name'], 'Afghanistan')


if __name__ == '__main__':
    unittest.main()
