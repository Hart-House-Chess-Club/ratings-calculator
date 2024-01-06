"""Generates all CFC data and stores it into the bin.

This data is not related to data recovered from cfc's open api at

Includes Analysis Data
- data on rating changes
- data on arbiters
- data on masters
- data on potential norm tournaments

Includes data on NMs/NCMs which have not been awarded.

Player Data
- data on ratings of all players

"""
from pathlib import Path
from fideparser import tournament, ratingperiod


class CFCAssets:
    """Generates a list of norm eligble tournaments in the given country"""

    def generate_cfc_arbiters(self, arb_type: int) -> None:
        """Generates the list of cfc national arbiters for the given country

        :param arb_type: Represents which type of master title to generate.
        """
        pass

    def generate_cfc_national_masters(self, master_type: int) -> None:
        """Generates JSONS for FIDE national masters for the given country
        :param master_type: Represents which type of master title to generate.
        """
        pass

    def generate_cfc_rating_changes(self) -> None:
        """Generates a list of rating changes within the country
        """
        pass

    def generate_cfc_norm_tournaments(self) -> None:
        """Generates a list of norm elidble tournaments in the given country
        """
        pass


class CFCPlayerData:
    """Using fideparser library to generate files for exporting FIDE data.
    """
    def __init__(self, arb_data: bool, report_data: bool):
        """ Initialization variables
        """
        self.arb_data = arb_data
        self.report_data = report_data

    """Generates FIDE player data"""
    def generate_player_data(self, period: str) -> None:
        """Generates a list of all tournaments in the given country
        """
        print("Running generate player data")

        output_file = f"{period}-"

        # append to the output file name
        if self.report_data:
            output_file += "-report-true"
        else:
            output_file += "-report-false"

        if self.arb_data:
            output_file += "-arb-true"
        else:
            output_file += "-arb-false"

        output_file = Path(__file__).parent.parent / "src" / "ratings_calculator" / "assets" / "cache" / "fide" / f"{output_file}.csv"
        # file.export(output_file, "csv")

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


data = CFCPlayerData(False, True)
data.generate_full_year("2023")
