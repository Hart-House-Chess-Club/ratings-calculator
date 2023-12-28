"""Class to get cfc profile information of the user"""
import json
import requests


class CFCProfile:
    """User id of the user that we are trying to get data for"""

    # default constructor for ratings calculator
    def __init__(self, user_id: int, request=True) -> None:
        self.user_id = user_id
        self.profile = self.initialize_profile(request)
        return

    def initialize_profile(self, request=True) -> dict:
        """
        Gets the profile of the user
        :param request: boolean indicating whether to use the web to search for this fvalue or not.
        :return: json dictionary mapping of the player and its fields
        """
        if request:
            URL = f"https://server.chess.ca/api/player/v1/{self.user_id}"
            page = requests.get(URL)
            return page.json()
        else:
            # open the json file and place the file as the value into the page
            filepath = "player_info.json"
            f = open(filepath)
            data = json.load(f)
            return data

    def get_profile(self) -> dict:
        """
        Gets the profile of the current user
        :return: json dictionary mapping of the player and its fields
        """
        return self.profile

    def get_events_played(self) -> int:
        """
        Gets the number of events that this user has participated in
        :return: events that this user has played in
        """
        numEvents = 0
        if self.profile["player"]["events"] == []:
            return 0
        else:
            return len(self.profile["player"]["events"])

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
