from RatingsCalculator import RatingsCalculator

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

TODO: If a player’s post tournament rating (including any participation and bonus points) is less than 200, the player 
is entered in the rating list at 200. This applies to both provisional and permanent ratings.

TODO: Provisional ratings: 3 to 24 games


TODO: For players who start a tournament above 2200 and during the event drop below 2200, we currently assume that the 
k factor remians the same.

However, this is not correct as the ratings can change. 

"""

"""
Calculates the ratings
"""


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
    for i in range(1, n + 1):
        ele = input("Rating of player " + str(i) + ": ")

        # strip whitespace
        ele = ele.strip()

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
    rating_type = int(input("Rating Type: (1 for established, 0 for provisional): "))

    # established or provisional rating? (can be removed in the future))
    quickTourney = int(input("Quick Tournament: (1 for quick less than 15 minutes total, 0 for classical): "))

    if rating_type == 1:
        # new_rating = established_ratings(1450, 1450, 4, [1237, 1511, 1214, 1441, 1579, 2133])
        calc_new_rating = ratingsCalc.established_ratings(all_time_high, current_rating, (wins + draws * 0.5), ratings_list)
        perf_rating = ratingsCalc.performance_rating(ratings_list, wins, losses, len(ratings_list))
        print("Performance Rating: ", perf_rating)
    else:
        # TODO: test provisional ratings
        calc_new_rating = ratingsCalc.performance_rating(ratings_list, wins, losses, n)

    print("New Rating is: ", calc_new_rating)
