import matplotlib.pyplot as plt
import numpy as np

from Profile import CFCProfile
from config import Config
from Profile import Event

# set random seed
np.random.seed(444)


class Visualization:
    """Visualization class"""

    def __init__(self) -> None:
        return

    def visualize_ratings(self, id: int) -> None:
        """Visualize ratings for a given user ID
        
        :param id: Represents the id that we want to get
        """

        # get the cfc profile from the id
        configuration = Config(use_profile=True, web_profile=True, quick=False)
        cfc_profile = CFCProfile(id, config=configuration)

        reg_events, quick_events = cfc_profile.get_events()

        dateReg = [float(event.date.year + event.date.month/12 + event.date.day/300)  for event in reg_events]
        rtgReg = [event.rating_after for event in reg_events]
        dateQuick = [float(event.date.year + event.date.month/12 + event.date.day/300) for event in quick_events]
        rtgQuick = [event.rating_after for event in quick_events]

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(dateReg, rtgReg, ls="solid", label="Regular Rating")
        ax.plot(dateQuick, rtgQuick, ls="solid", label="Quick Rating")
        ax.set_title('CFC Regular and Quick Ratings Over Time for id ' + str(id))
        ax.legend(loc='upper left')
        ax.set_ylabel('CFC Rating')
        ax.set_xlabel('Year')
        ax.set_xlim(xmin=min(dateQuick + dateReg), xmax=max(dateQuick + dateReg))
        fig.tight_layout()
        plt.show()

    def visualize_test(self):
        """Test ability to visualize using matplotlib
        """

        rng = np.arange(50)
        rnd = np.random.randint(0, 10, size=(3, rng.size))
        yrs = 1950 + rng

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.stackplot(yrs, rng + rnd, labels=['Eastasia', 'Eurasia', 'Oceania'])
        ax.set_title('Combined debt growth over time')
        ax.legend(loc='upper left')
        ax.set_ylabel('Total debt')
        ax.set_xlim(xmin=yrs[0], xmax=yrs[-1])
        fig.tight_layout()
        plt.show()


vis = Visualization()
vis.visualize_ratings(150532)
