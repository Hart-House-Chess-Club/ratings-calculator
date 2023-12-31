"""Class to get cfc profile information of the user"""
import json
import requests
from config import Config


class CFCProfile:
    """User id of the user that we are trying to get data for"""

    # default constructor for ratings calculator
    def __init__(self, user_id: int, config: Config = Config()) -> None:
        self.user_id = user_id
        self.use_profile = config.use_profile
        self.web_profile = config.web_profile
        self.quick = config.quick

        self.profile = self.initialize_profile()
        return

    def initialize_profile(self) -> dict:
        """
        Gets the profile of the user
        :return: json dictionary mapping of the player and its fields
        """
        if self.web_profile:
            URL = f"https://server.chess.ca/api/player/v1/{self.user_id}"
            page = requests.get(URL)
            return page.json()
        else:
            # open the json file and place the file as the value into the page
            filepath = "../player_info.json"
            f = open(filepath)
            data = json.load(f)
            return data

    def get_profile(self) -> dict:
        """
        Gets the profile of the current user
        :return: json dictionary mapping of the player and its fields
        """
        return self.profile

    def get_games_played(self) -> int:
        """
        Gets the profile of the current user
        :return: json dictionary mapping of the player and its fields
        """
        games = 0
        for tournament in self.profile["player"]["events"]:
            if tournament["rating_type"] == "R" and not self.quick:
                games += tournament["games_played"]
            elif tournament["rating_type"] == "Q" and self.quick:
                games += tournament["games_played"]
            else:
                # not matching
                pass

        return games

    def get_events_played(self) -> int:
        """
        Gets the number of events that this user has participated in
        :return: events that this user has played in
        """
        if self.profile["player"]["events"] == []:
            return 0
        else:
            return len(self.profile["player"]["events"])

    def get_lifetime_high(self) -> int:
        """
        Gets the lifetime high for the event that the user is participating in
        :return: the lifetime high for this user based on whether quick or regular rating
        """
        search_name = "regular_indicator"
        if self.quick:
            search_name = "quick_indicator"

        # if the regular indicator is null, that means they haven't played enough games
        if self.profile["player"][search_name] == []:
            return 0
        else:
            return self.profile["player"][search_name]

    def get_last_tournaments(self, num_tournaments: int) -> []:
        """
        Gets the number of events that this user has participated in
        :param num_tournaments: previous n tournaments to get.
        :return: events that this user has played in
        """

        tournament_data = []

        if num_tournaments > len(self.profile["player"]["events"]):
            # if the number of tournaments is greater than the number that exists in the json, take that number
            num_tournaments = len(self.profile["player"]["events"])

        for i in range(num_tournaments):
            tournament_data.append(self.profile["player"]["events"][i])

        return tournament_data


class FIDEProfile:
    """Gets user id data for FIDE profile"""

    pass
