import math
from csv import reader

"""
@author Victor Zheng

For previously unrated and provisionally rated players, the performance rating is:

Rp = Rc + 400 (W - L) / N

where Rp is the performance rating,
Rc is the average rating of the player’s opponents,
W is the number of wins,
L is the number of losses,
N is the total number of games played.

For players with established ratings the new rating is

Rn = Ro + 32 (S - Sx)

In applying this equation to players of 2199 or over, change 32 to 16.
For players who start an event below 2199 and then in the event go above 2199 the gains are computed normally,
 namely with 32 in 414b and then the increase over 2199 is cut in half.
 For players who start an event above 2199 and then in the event go below 2200 the loss is computed normally,
 namely with 16 in 414b and then the decrease under 2200 is doubled.

Where Rn is the post event (new) rating before the application of bonus or participation points, Ro is the pre event
(old) rating, S is the score, and Sx is the expected score. This is determined by the following table to two
significant decimals (a more accurate determination of the expected score may be used in the actual calculation):


Result Bonus Points [Motion 2012-S Leblanc/McKim]

BONUS1 = a * RMaxBonus * Ke
BONUS2 = b * RChangeBonus * (Rnew – Rold – Threshold) * Ke
BONUSTotal = BONUS1 + BONUS2

where:

No bonus points are awarded if less than 4 games are played;
a = 1 if the new rating is at an all time high, 0 otherwise;
b = 1 if Rnew > (Rold + Threshold), 0 otherwise;
Threshold = RChangeThreshold * Ke * sqrt(n)
where n is the number of games played;
Ke is the ratio of the player’s K factor to the K factor used for players rated under 2200;
For the CFC rating system, K=32 for players under 2200 and K=16 for players at or over 2200;
Rnew is the post-event rating
Rold is the pre-event rating;
RMaxBonus = 20 (a constant);
RChangeBonus = 1.75 (a constant);
RChangeThreshold = 13 (a constant).
The numerical values in the bonus point equation may be adjusted from time to time by the Rating Auditor
as deemed necessary and in consultation with the CFC Executive.

TODO: From 411.1 Quick Chess, quick ratings will be calculated with 1/2 of the k factor
- this appears to not be in effect? 

TODO: This is not covered by the current calculation: 
416. For a player with a pre-event rating below 800.

TODO: If a player’s post tournament rating (including any participation and bonus points) is less than 200, the player is entered in the rating list at 200. This applies to both provisional and permanent ratings.

TODO: Provisional ratings: 3 to 24 games


TODO: For players who start a tournament above 2200 and during the event drop below 2200, we currently assume that the k factor remians the same.
However, this is not correct as the ratings can change. 

"""

"""
Calculates the ratings
"""


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

    def established_ratings(self, all_time_high_score: int, old_rating: int, score: float, opponent_ratings: list, quick = False) -> float:
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


if __name__ == "__main__":
    print("Welcome to Ratings Calculator\n\n"
          "This project is about calculating more accurate CFC ratings than ever before. \n"
          "\n"
          "Please note the following: \n"
          "     - You must use ratings < 3000 \n"
          "     - You must use no extra whitespace\n"
          "\n"
          "These are initial considerations and we will aim to remove these requirements in future iterations\n"
          "\n"
          "Best of luck in your chess endeavours!\n")

    # initialize expected scores dictionary to begin

    ratingsCalc = RatingsCalculator()

    # expected_scores = ratingsCalc.expected_scores_init()

    # get data from user
    cfc_id_input = input("Enter CFC ID: ")

    if not cfc_id_input.isnumeric():
        print("ERROR: input for cfc id must be numeric")
        exit(-1)

    # else, convert
    cfc_id = int(cfc_id_input)

    # get number of games played
    numInput = input("Number of games played: ")
    if not numInput.isnumeric():
        print("Error: input must be numeric")
        exit(-1)  # exit with exit code 1

    # else, convert
    n = int(numInput)

    ratings_list = []
    for i in range(1, n+1):
        ele = input("Rating of player " + str(i) + ": ")

        if not ele.isnumeric():
            print("Error: rating input must be numeric")
            exit(-1)  # exit with exit code 1

        # convert element to numeric
        ele = int(ele)

        ratings_list.append(ele)

    # get total score of player
    wins = int(input("Wins: "))
    losses = int(input("Losses: "))
    draws = int(input("Draws: "))

    # get all time high rating, current rating, (we can use the CFC api in the future to remove the need for this).
    current_rating = int(input("Current Rating: "))

    all_time_high = int(input("All Time High Rating: "))

    # established or provisional rating? (can be removed in the future))
    rating_type = int(input("Rating Type: (1 for established, 0 for provisional: "))

    if rating_type == 1:
        # new_rating = established_ratings(1450, 1450, 4, [1237, 1511, 1214, 1441, 1579, 2133])
        calc_new_rating = ratingsCalc.established_ratings(all_time_high, current_rating, (wins+draws), ratings_list)
    else:
        calc_new_rating = ratingsCalc.provisional_unrated_players(ratings_list, n, wins, losses)

    print("New Rating is: ", calc_new_rating)
