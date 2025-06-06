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

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from fideparser import tournament, ratingperiod
import requests
from Profile import CFCProfile
from config import Config


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


class TDList:
    """
    Get TD List file from public cfc api at https://storage.googleapis.com/cfc-public/data/tdlist.txt
    """

    def __init__(self, get_new_data: bool) -> None:
        """ Initialize data
        :param get_new_data: indicates whether to get new data from the cfc api or use the current one in the cache.
        """

        self.output_file = Path(
            __file__).parent.parent / "assets" / "cache" / "cfc" / f"tdlist.txt"

        # if get_new_data, then save the latest files.
        if get_new_data:
            self.save_td_list()

    def save_td_list(self) -> None:
        """
        Saves the td list file into the cache
        """

        file_loc = "https://storage.googleapis.com/cfc-public/data/tdlist.txt"

        # use requests library to save the file link into the cache.
        # noinspection PyBroadException
        try:
            r = requests.get(file_loc, allow_redirects=True)

            # output file will be in cache
            open(self.output_file, 'wb').write(r.content)

        except Exception:
            print("Failed to connect to API, check connection to requests library")

    def generate_cfc_ids_list(self) -> []:
        """
        Generate and return a list of all active cfc ids
        """

        id_list = []
        
        print("Output file is", self.output_file)
        
        file = open(self.output_file, 'r', encoding='utf-8', errors='replace')
        # file = file.read()

        lines = file.readlines()

        count = 0
        # Strips the newline character
        for line in lines:
            # skip line 1
            if count != 0:
                id_list.append(line.split(",")[0])

            count += 1

        return id_list


class CFCPlayerData:
    """Using fideparser library to generate files for exporting FIDE data.
    """
    def __init__(self) -> None:
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

        output_file = Path(__file__).parent.parent / "assets" / "cache" / "cfc" / f"{output_file}.json"

        profile.save_profile(str(output_file))

        print("Finished generating CFC player data to ", output_file)

    def generate_all_players(self, max_id: int):
        """Generates a list of all tournaments this year in the given country
        """

        # iterate through all valid ids. Get ids from tdlist file
        for i in range(max_id + 1):
            # format for the period is yyyy-mm-dd
            self.generate_player_data(i)

# data = CFCPlayerData()
# data.generate_player_data(150768)


td_list = TDList(True)
user_ids = td_list.generate_cfc_ids_list()
print(user_ids)

data = CFCPlayerData()
for id in user_ids:
    data.generate_player_data(int(id))
