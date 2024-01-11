import matplotlib.pyplot as plt
import numpy as np

# set random seed
np.random.seed(444)


class Visualization:
    """Visualization class"""

    def __init__(self) -> None:
        return

    def visualize_ratings(self) -> None:
        """Visualize ratings for a given user ID"""

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
