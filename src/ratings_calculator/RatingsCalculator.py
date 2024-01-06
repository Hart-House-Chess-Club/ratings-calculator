"""Ratings Calculator is a class that calculates ratings, cfc-style

@copywrite @ 2024, Hart House Chess Club
"""

import math
from csv import reader


class RatingsCalculator:
    """Ratings Calculator is a class that calculates ratings, cfc-style"""

    # default constructor for ratings calculator
    def __init__(self) -> None:
        self.expected_scores = self.expected_scores_init()

        return

    def average_rating(self, ratings: list) -> float:
        """
        Average ratings of the list of the ratings
        :param ratings: a list of ratings
        :return: average rating
        """
        ave_rating = 0
        for rating in ratings:
            ave_rating += rating
        return ave_rating / len(ratings)

    def provisional_unrated_players(self, ratings: list, wins: int, losses: int, games_played: int) -> object:
        """
        wins is the number of wins,
        losses is the number of losses
        games_played is the number of games
        ratings is the list of opponent's ratings
        """
        Rc = self.average_rating(ratings)
        # Rp = Rc + 400 (W - L) / N
        Rp = Rc + 400 * (wins - losses) / games_played
        return Rp

    def established_ratings(self, all_time_high_score: int, old_rating: int, score: float, opponent_ratings: list,
                            quick=False) -> float:
        """
        Returns the established rating from the dictionary of ratings
        :param all_time_high_score: the all time high of the player
        :param score: the total score from the tournament
        :param opponent_ratings: a list of opponent ratings
        :param old_rating: the player's old rating
        :param quick: if the time control used is between 5 and 14 minutes
        :return: returns the established rating of the player
        >>> ratingTest = RatingsCalculator()
        >>> # expected_dict = ratingTest.expected_scores_init()
        >>> ratingTest.established_ratings(1450, 1450, 4, [1237, 1511, 1214, 1441, 1579, 2133])
        1487
        """
        if score > len(opponent_ratings):
            raise Exception("Cannot have higher score than games played")

        # K=32 for players under 2200 and K=16 for players at or over 2200;
        # Rn = Ro + 32 (S - Sx)
        if old_rating >= 2199:
            multiplier = 16
        else:
            multiplier = 32

        # if quick (where time control used is between 5-14 min)
        if quick:
            multiplier = multiplier // 2

        # expected_scores_dict = self.expected_scores_init()

        expected_total = self.expected_total_score(old_rating, opponent_ratings)
        new_rating = old_rating + multiplier * (score - expected_total)

        if new_rating > all_time_high_score:
            all_time_high_valid = 1
        else:
            all_time_high_valid = 0

        multiplier_e = multiplier // 32  # ratio of the multiplier to ratings under 2200.
        bonus = self.bonuses(all_time_high_valid, multiplier_e, new_rating, old_rating, len(opponent_ratings))
        sum_of_scores = new_rating + bonus
        return sum_of_scores

    def bonuses(self, a: int, k_factor_e: int, r_new: float, r_old: int, n: int) -> int:
        """
        Returns the total sum of all bonuses available
        :param a: is = 1 if all time high, 0 otherwise
        :param k_factor_e: ratio of the player's k factor to the k factor used for players under 2200
        :param r_new: post-event rating
        :param r_old: pre-event rating
        :param n: number of games played
        :return: value of the new rating
        >>> ratingTest = RatingsCalculator()
        >>> ratingTest.bonuses(0, 1, 1487, 1450, 6)
        1496
        """
        if n < 4:  # no bonus points awarded if less than 4 games played
            return 0

        R_MAX_BONUS = 20  # constants set
        R_CHANGE_BONUS = 1.75
        R_CHANGE_THRESHOLD = 13

        bonus1 = a * R_MAX_BONUS * k_factor_e
        threshold = R_CHANGE_THRESHOLD * k_factor_e * math.sqrt(n)

        if r_new > (r_old + threshold):
            b = 1
        else:
            b = 0

        bonus2 = b * R_CHANGE_BONUS * (r_new - r_old - threshold) * k_factor_e
        total_bonus = round(bonus1 + bonus2)
        return total_bonus

    def expected_total_score(self, rating: int, opponent_ratings: list):
        """
        Returns the expected total score from the tournament
        :param rating: is the player's rating
        :param opponent_ratings: is the opponent's rating in a lists
        >>> ratingTest = RatingsCalculator()
        >>> ratingTest.expected_total_score(1450, [1237, 1511, 1214, 1441, 1579, 2133])
        2.84
        """
        sum_expected = 0
        for opp_rating in opponent_ratings:
            if rating >= opp_rating:  # your rating is bigger than the opponents
                sum_expected += self.find_expected_value(rating - opp_rating, 0)
            else:
                sum_expected += self.find_expected_value(opp_rating - rating, 1)

        return sum_expected

    def find_expected_value(self, difference: int, lower_val: int):
        """
        Returns the expected value of the individual based on whether it is a lower or higher score.
        :param lower_val: whether the number is a lower value
        :param difference: is the difference in ratings
        :return: expected value based on the expected dictionary
        """
        expected_dict = self.expected_scores
        expected = expected_dict[int(difference)]
        if lower_val == 1:
            expected = round(1 - expected, 2)
        else:
            # keep the older value
            pass

        return expected

    def expected_scores_init(self) -> dict:
        """
        Returns the expected score dictionary
        :return: dictionary containing expected scores
        """
        # file is recommend to be in the following format: starting rank, Name of Player, CFC ID
        # information of the event
        file_name = "C:\\Users\\zheng\\PycharmProjects\\ratings-calculator\\ExpectedScores.csv"
        expected_scores_higher = {}

        with open(file_name, 'r') as f:
            csv_reader = reader(f)
            next(csv_reader)

            for row in csv_reader:
                # iterate through each row
                # print(row)
                # if it's the last line
                max_diff = 2000
                if row[0][0:3] == "735":
                    for j in range(735, max_diff):
                        expected_scores_higher[j] = 1
                else:
                    row_vals = row[0].split("-")
                    starting_val = int(row_vals[0])
                    end_val = int(row_vals[1])

                    for j in range(starting_val, end_val + 1):
                        expected_scores_higher[j] = float(row[1])  # the location of the csv file

        return expected_scores_higher
