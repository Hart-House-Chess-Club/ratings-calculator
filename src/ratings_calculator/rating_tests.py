import unittest

from src.ratings_calculator.main import RatingsCalculator


class TestBasicFunctionalities(unittest.TestCase):
    def test_default_CFC_ratings(self) -> None:
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(1450, 1450, 4, [1237, 1511, 1214, 1441, 1579, 2133])
        print("New Rating is: ", new_rating)
        self.assertEqual(new_rating, 1516.12)  # add assertion here

    def test_null_values(self) -> None:
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(0, 0, 0, [])
        print("New Rating is: ", new_rating)
        self.assertEqual(new_rating, 0)  # add assertion here

    def test_one_game(self) -> None:
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(1000, 1000, 1, [1200])
        print("New Rating is: ", new_rating)
        self.assertEqual(new_rating, 1200)  # add assertion here


if __name__ == '__main__':
    unittest.main()
