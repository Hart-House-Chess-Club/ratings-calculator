"""Unit tests for the application"""

import unittest

from Profile import CFCProfile
from RatingsCalculator import RatingsCalculator
from config import Config


class TestProfileFunctionality(unittest.TestCase):
    def test_name_input_correct_web(self) -> None:
        config = Config()

        profile = CFCProfile(150532, config)  # for now, input int
        profile_dict = profile.get_profile()
        self.assertEqual(profile_dict["player"]["name_first"], "Victor")
        self.assertEqual(profile_dict["player"]["name_last"], "Zheng")

        tour_data = profile.get_last_tournaments(5)
        print(tour_data)
        assert len(tour_data) == 5

        games_played = profile.get_games_played()
        print(games_played)

    def test_name_input_correct_local(self) -> None:
        config = Config(web_profile=False)

        profile = CFCProfile(150532, config)  # for now, input int
        profile_dict = profile.get_profile()
        self.assertEqual(profile_dict["player"]["name_first"], "Victor")
        self.assertEqual(profile_dict["player"]["name_last"], "Zheng")

        tour_data = profile.get_last_tournaments(5)
        print(tour_data)
        assert len(tour_data) == 5

        games_played = profile.get_games_played()
        print(games_played)

    def test_get_lifetime_high_regular(self) -> None:
        config = Config(web_profile=False, quick=False)

        profile = CFCProfile(150532, config)  # for now, input int

        regular_high = profile.get_lifetime_high()
        assert regular_high == 2160

    def test_get_lifetime_high_quick(self) -> None:
        config = Config(web_profile=False, quick=True)

        profile = CFCProfile(150532, config)  # for now, input int

        regular_high = profile.get_lifetime_high()
        assert regular_high == 2092

    def test_get_lifetime_high_fail(self) -> None:
        config = Config(web_profile=False, quick=True)

        profile = CFCProfile(150532, config)  # for now, input int

        regular_high = profile.get_lifetime_high()
        assert not regular_high == 2091

    def test_get_national_master_norms_invalid(self) -> None:
        config = Config(web_profile=False, quick=False)

        profile = CFCProfile(150532, config)  # for now, input int

        nm_norms = profile.calc_national_master_norms()
        print(nm_norms)
        assert nm_norms[0] is False

        print("National Master Title Unsuccessfully Achieved")

    def test_get_national_master_norms_valid(self) -> None:
        # success fnd nm norms
        config = Config(web_profile=True, quick=False)

        profile = CFCProfile(154677, config)  # for now, input int

        nm_norms = profile.calc_national_master_norms()
        print(nm_norms)

        assert nm_norms[0] is True
        assert len(nm_norms[1]) >= 3

        print("National Master Title Successfully Achieved")

    def test_get_national_master_norms_false(self) -> None:
        # fail nm norms finding
        config = Config(web_profile=True, quick=False)

        profile = CFCProfile(152240, config)  # for now, input int

        nm_norms = profile.calc_national_master_norms()
        print(nm_norms)

        assert nm_norms[0] is False
        assert len(nm_norms[1]) < 3


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
        new_rating = ratings.established_ratings(2160, 2052, 0, [2208])
        print("New Rating is: ", new_rating)
        self.assertEqual(round(new_rating), 2043)  # add assertion here

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

    def test_quick_ratings_gtcl_rapid(self) -> None:
        # test the calc against perf at october open for 150532
        ratings = RatingsCalculator()
        # Can transnational of 14 games
        new_rating = ratings.established_ratings(2002, 2002, 5, [1927, 1876, 1899, 1841, 1429], quick=False)
        print("New Rating is: ", new_rating)
        # within three points
        self.assertTrue(abs(round(new_rating) - 2092) <= 3)  # add assertion here

    def test_quick_ratings_with_lifetime_high(self) -> None:
        # test the calc against perf at october open for 150532
        ratings = RatingsCalculator()
        new_rating = ratings.established_ratings(1856, 1856, 9, [1431, 1431, 2024, 2024, 1478, 1478, 1710, 1710, 1938, 1938, 1535, 1535, 1986, 1986], quick=False)
        print("New Rating is: ", new_rating)
        self.assertEqual(round(new_rating), 1882)  # add assertion here
        # note for this tournament that this should be set to quick as true?


if __name__ == '__main__':
    unittest.main()
