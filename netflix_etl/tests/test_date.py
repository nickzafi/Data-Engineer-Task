import unittest
import datetime

from datetime import date


def date_transform(date):
    date = date.strip(" ")
    if not date:
        return
    return datetime.strptime(date, "%B %d, %Y").date()


class TestDate_transform(unittest.TestCase):
    def test_date_transform(self):
        date = "August 14, 2020"
        result = date_transform(date)
        expected_result = date(2020, 8, 14)

        self.assertEqual(result, expected_result)


# if __name__ == "__main__":
#     unittest.main()
