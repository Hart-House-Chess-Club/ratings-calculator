import unittest

from src.ratings_calculator.main import RatingsCalculator


class TestBasicFunctionalities(unittest.TestCase):
    def test_default_CFC_ratings_without_bonus(self) -> None:
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(1600, 1450, 4, [1237, 1511, 1214, 1441, 1579, 2133])
        print("New Rating is: ", new_rating)
        self.assertEqual(int(new_rating), 1496)  # this is from the handbook

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

    def test_victor_october_open(self) -> None:
        # test the calc against perf at october open for 150532
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(2160, 2014, 3, [2276, 2151, 1972, 2155, 2100])
        print("New Rating is: ", new_rating)
        self.assertEqual(round(new_rating), 2073)  # add assertion here

    def test_victor_can_junior_open(self) -> None:
        # test the calc against perf at october open for 150532
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(2160, 2068, 2.5, [1949, 1982, 1892, 1843, 1898, 1936])
        print("New Rating is: ", new_rating)
        self.assertEqual(round(new_rating), 2014)  # add assertion here

    def test_victor(self) -> None:
        # test the calc against perf at october open for 150532
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(2160, 2068, 2.5, [1949, 1982, 1892, 1843, 1898, 1936])
        print("New Rating is: ", new_rating)
        self.assertEqual(round(new_rating), 2014)  # add assertion here


if __name__ == '__main__':
    unittest.main()
