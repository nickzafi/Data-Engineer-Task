import unittest
from datetime import datetime

from utilities.insert_to_db import date_transform


class TestDate_transform(unittest.TestCase):
    def test_date_transform(self):
        date = "August 14, 2020"
        result = date_transform(date)
        expected_result = datetime(2020, 8, 14)

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
