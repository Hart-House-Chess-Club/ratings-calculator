"""Generates all FIDE data and stores it into the bin

Includes Analysis Data
- data on rating changes
- data on arbiters
- data on masters
- data on potential norm tournaments

Player Data
- data on ratings of all players, from
- http://ratings.fide.com/download/players_list.zip

"""
from pathlib import Path
from chess import Board
from fideparser import tournament, ratingperiod

country = "CAN"


class FideAssets:
    """Generates a list of norm eligble tournaments in the given country"""

    def generate_fide_arbiters(self, arb_type: int) -> None:
        """Generates the list of FIDE arbiters for the given country

        :param arb_type: Represents which type of master title to generate.
        """
        pass

    def generate_fide_international_masters(self, master_type: int) -> None:
        """Generates JSONS for FIDE international masters for the given country
        :param master_type: Represents which type of master title to generate.
        """
        pass

    def generate_fide_rating_changes(self) -> None:
        """Generates a list of rating changes within the country
        """
        pass

    def generate_norm_tournaments(self) -> None:
        """Generates a list of norm elidble tournaments in the given country
        """
        pass


class FidePlayerData:
    """Generates FIDE player data"""
    def generate_player_data(self) -> None:
        """Generates a list of norm eligble tournaments in the given country

        """

        print("Running")

        rating_period = ratingperiod.RatingPeriod(
            "ESP",
            "2013-01-01"
        )

        # output_file = "2023-12-01-csv.csv"
        rating_period.save()

        output_file = Path(__file__).parent.parent / "src" / "ratings_calculator" / "assets" / "cache" / "output_file.csv"
        rating_period.export(output_file, "csv")


data = FidePlayerData()

data.generate_player_data()
