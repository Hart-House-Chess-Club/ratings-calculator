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
    """Using fideparser library to generate files for exporting FIDE data.
    """
    def __init__(self, country: str, arb_data: bool, report_data: bool):
        """ Initialization variables
        """
        self.country = country
        self.arb_data = arb_data
        self.report_data = report_data

    """Generates FIDE player data"""
    def generate_player_data(self, period: str) -> None:
        """Generates a list of all tournaments in the given country
        """
        print("Running generate player data")

        rating_period = ratingperiod.RatingPeriod(
            self.country,
            period,
            arbiters_data=self.arb_data,
            report_data=self.report_data
        )

        output_file = f"{period}-{self.country}"

        # append to the output file name
        if self.report_data:
            output_file += "-report-true"
        else:
            output_file += "-report-false"

        if self.arb_data:
            output_file += "-arb-true"
        else:
            output_file += "-arb-false"

        rating_period.save()

        output_file = Path(__file__).parent.parent / "src" / "ratings_calculator" / "assets" / "cache" / f"{output_file}.csv"
        rating_period.export(output_file, "csv")

        print("Finished generating player data")

    def generate_full_year(self, year: str):
        """Generates a list of all tournaments this year in the given country
        """
        period = ""

        # iterate through 12 months
        for i in range(1, 13):
            # format for the period is yyyy-mm-dd
            period = year + "-" + str.zfill(str(i), 2) + "-" + "01"

            self.generate_player_data(period)


data = FidePlayerData("CAN", False, True)

data.generate_full_year("2023")
