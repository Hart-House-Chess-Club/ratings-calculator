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
from src.ratings_calculator.Profile import CFCProfile
from src.ratings_calculator.config import Config


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
    def __init__(self):
        """ Initialization variables
        """
        pass

    """Generates CFC player data"""
    def generate_player_data(self, player_id: int) -> None:
        """Generates a list of all tournaments in the given country
        """
        print("Running generate player data")

        profile = CFCProfile(player_id)

        output_file = f"cfc_player_info_{player_id}"

        output_file = Path(__file__).parent.parent / "src" / "ratings_calculator" / "assets" / "cache" / "cfc" / f"{output_file}.json"

        profile.save_profile(str(output_file))

        print("Finished generating CFC player data to ", output_file)

    def generate_all_players(self, max_id: int):
        """Generates a list of all tournaments this year in the given country
        """
        period = ""

        # iterate through 12 months
        for i in range(max_id + 1):
            # format for the period is yyyy-mm-dd
            self.generate_player_data(i)


data = CFCPlayerData()
data.generate_player_data(150768)
