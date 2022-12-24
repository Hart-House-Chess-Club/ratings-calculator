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
"""


def average_rating(ratings: list) -> float:
    """
    Average ratings of the list of the ratings
    :param ratings: a list of ratings
    :return: average rating
    """
    ave_rating = 0
    for rating in ratings:
        ave_rating += rating
    return ave_rating / len(ratings)


def provisional_unrated_players(ratings: list, wins: int, losses: int, games_played: int) -> object:
    """
    wins is the number of wins,
    losses is the number of losses
    games_played is the number of games
    ratings is the list of opponent's ratings
    """
    Rc = average_rating(ratings)
    # Rp = Rc + 400 (W - L) / N
    Rp = Rc + 400 * (wins - losses) / games_played
    return Rp


def established_ratings(old_rating: int, score: int, opponent_ratings: list, all_time_high_rating: int) -> int:
    """
    Returns the updated rating from the dictionary of ratings after adjusting for bonuses
    :param score: the total score from the tournament
    :param all_time_high_rating: the player's all time high rating
    :param opponent_ratings: a list of opponent ratings
    :param old_rating: the player's old rating
    :return: returns the established rating of the player.
    >>> established_ratings(1450, 4, [1237, 1511, 1214, 1441, 1579, 2133], 1600)
    1496
    """
    # K=32 for players under 2200 and K=16 for players at or over 2200;
    # Rn = Ro + 32 (S - Sx)
    if old_rating >= 2199:
        multiplier = 16
    else:
        multiplier = 32

    expected_scores = expected_scores_init()
    new_rating = old_rating + multiplier * (score - expected_total_score(expected_scores, old_rating, opponent_ratings))

    if new_rating > all_time_high_rating:
        all_time_high = 1
    else:
        all_time_high = 0

    bonus = bonuses(all_time_high, multiplier, new_rating, old_rating, len(opponent_ratings))
    sum_of_scores = round(new_rating + bonus)
    final_rating = check_ratings_under_800(old_rating, sum_of_scores, provisional=False)
    return final_rating


def bonuses(a: int, k_factor: int, r_new: int, r_old: int, n: int) -> float:
    """
    Returns the total sum of all bonuses available
    :param a:
    :param k_factor:
    :param r_new:
    :param r_old:
    :param n:
    :return:
    """
    R_MAX_BONUS = 20
    R_CHANGE_BONUS = 1.75
    R_CHANGE_THRESHOLD = 13

    k_error = k_factor / 32  # k error is the ratio of the player's k factor to the k
    # factor used for players rated under 2200.

    bonus1 = a * R_MAX_BONUS * k_error
    threshold = R_CHANGE_THRESHOLD * k_error * math.sqrt(n)

    if r_new > (r_old + threshold):
        b = 1
    else:
        b = 0

    bonus2 = b * R_CHANGE_BONUS * (r_new - r_old - threshold) * k_error
    return bonus1 + bonus2


def check_ratings_under_800(old_rating: int, new_rating: int, provisional: bool) -> int:
    """
    Returns a new rating based on whether the user's ratings were over 800 before the tournament.
    If the user's rating was over 800, then their rating cannot be lower than 799. RULE 416 a
    If the user's rating was below 800, and their rating afterwards is also below 800, we take the highest of either. RULE 416 b
    If the post tournament rating is below 200, we set their rating to 200. RULE 416 c

    :param old_rating: the rating (regardless of whether provisional) before the tournament.
    :param new_rating: the new rating after bonus points
    :param provisional: whether the rating is provisional
    :return: an integer of their rating post adjustments
    >>> check_ratings_under_800(1000, 300, False)
    799
    >>> check_ratings_under_800(600, 790, False)
    790
    >>> check_ratings_under_800(650, 560, False)
    650
    >>> check_ratings_under_800(204, 190, True)
    200
    >>> check_ratings_under_800(500, 1000, False)
    1000
    """
    # RULE 416 a
    if new_rating < 800 and old_rating > 799:
        new_rating = 799

    # RULE 416 b. Note: this only applies to permanent ratings
    if new_rating < 800 and old_rating < 800 and not provisional:
        if new_rating < old_rating:
            new_rating = old_rating

    if new_rating < 200 and provisional:
        new_rating = 200

    return new_rating


def expected_total_score(expected_dict: dict, rating: int, opponent_ratings: list):
    """
    Returns the expected total score from the tournament
    :param expected_dict: is the expected dictionary of scores based on CFC data
    :param rating: is the player's rating
    :param opponent_ratings: is the opponent's rating in a lists
    >>> expected_dict = expected_scores_init()
    >>> expected_total_score(expected_dict, 1450, [1237, 1511, 1214, 1441, 1579, 2133])
    2.84
    """
    sum_expected = 0
    for opp_rating in opponent_ratings:
        if rating >= opp_rating:  # your rating is bigger than the opponents
            sum_expected += find_expected_value(expected_dict, rating - opp_rating, 0)
        else:
            sum_expected += find_expected_value(expected_dict, opp_rating - rating, 1)

    return sum_expected


def find_expected_value(expected_dict: dict, difference: int, lower_val: int):
    """
    Returns the expected value of the individual based on whether it is a lower or higher score.
    :param lower_val: whether the number is a lower value
    :param expected_dict: dictionary with the expected scores
    :param difference: is the difference in ratings
    :return: expected value based on the expected dictionary
    """
    expected = expected_dict[int(difference)]
    if lower_val == 1:
        expected = round(1 - expected, 2)
    else:
        # keep the older value
        pass

    return expected


def expected_scores_init() -> dict:
    """
    Returns the expected score dictionary
    :return: dictionary containing expected scores
    """
    # file is recommend to be in the following format: starting rank, Name of Player, CFC ID
    # information of the event
    file_name = "ExpectedScores.csv"
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
    print(expected_scores_init())
    pass
