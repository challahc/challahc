import unittest
from datetime import datetime
from happy_birthday import calculate_age, get_age_range

class TestHappyBirthday(unittest.TestCase):
    def test_calculate_age(self):
        # Test with a birthdate in the past
        birthdate = "2000-03-27"
        expected_age = datetime.today().year - 2000
        if (datetime.today().month, datetime.today().day) < (3, 27):
            expected_age -= 1
        self.assertEqual(calculate_age(birthdate), expected_age)

        # Test with today's date as birthdate
        today = datetime.today().strftime("%Y-%m-%d")
        self.assertEqual(calculate_age(today), 0)

        # Test with a future date (should raise an exception)
        future_date = "3000-01-01"
        with self.assertRaises(ValueError):
            calculate_age(future_date)

    def test_get_age_range(self):
        # Test various age ranges
        self.assertEqual(get_age_range(1), "Baby")
        self.assertEqual(get_age_range(3), "Preschool")
        self.assertEqual(get_age_range(7), "Elementary School")
        self.assertEqual(get_age_range(12), "Middle School")
        self.assertEqual(get_age_range(16), "High School")
        self.assertEqual(get_age_range(25), "Adult(25)")

if __name__ == "__main__":
    unittest.main()