import matplotlib.pyplot as plt
import numpy as np

# set random seed
np.random.seed(444)


class Visualization:
    """Visualization class"""

    def __init__(self) -> None:
        return

    def visualize_ratings(self) -> None:
        """Visualize ratings for a given user ID
        
        :param id: Represents the id that we want to get
        """
        fig, ax = plt.subplots(figsize=(5, 3))

        dateReg = [2000, 2001, 2002, 2003, 2004, 2005, 2006]
        rtgReg = [200, 500, 500, 600, 1000, 2000, 2400]
        dateQuick = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2020]
        rtgQuick = [300, 400, 500, 600, 1030, 2200, 2300, 2350]
        labels=['Regular Rating', 'Quick Rating',]

        ax.plot(dateReg, rtgReg, ls="solid", label="Regular Rating")
        ax.plot(dateQuick, rtgQuick, ls="solid", label="Quick Rating")
        ax.set_title('Ratings over time')
        ax.legend(loc='upper left')
        ax.set_ylabel('Rating')
        ax.set_xlim(xmin=2000, xmax=2020)
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
vis.visualize_ratings()