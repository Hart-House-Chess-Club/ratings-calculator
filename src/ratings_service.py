from RatingsCalculator import RatingsCalculator

def calculate_rating(
    cfc_id: int,
    n_games: int,
    ratings_list: list,
    wins: int,
    losses: int,
    draws: int,
    current_rating: int,
    all_time_high: int,
    rating_type: int,
    quick_tourney: int
):
    ratingsCalc = RatingsCalculator()
    if rating_type == 1:
        calc_new_rating = ratingsCalc.established_ratings(
            all_time_high, current_rating, (wins + draws * 0.5), ratings_list
        )
        perf_rating = ratingsCalc.performance_rating(ratings_list, wins, losses, len(ratings_list))
        return {
            "performance_rating": perf_rating,
            "new_rating": calc_new_rating
        }
    else:
        calc_new_rating = ratingsCalc.performance_rating(ratings_list, wins, losses, n_games)
        return {
            "performance_rating": calc_new_rating,
            "new_rating": calc_new_rating
        }