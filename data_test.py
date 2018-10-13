import unittest

from data import country_for_code


class DataTest(unittest.TestCase):
    def test_country_for_code(self):
        countries = country_for_code(93)
        self.assertEqual(len(countries), 1)
        self.assertEqual(countries[0]['name'], 'Afghanistan')

        countries = country_for_code(1)
        self.assertEqual(len(countries), 2)


if __name__ == '__main__':
    unittest.main()
