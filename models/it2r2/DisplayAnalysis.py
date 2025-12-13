import numpy as np

import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
from matplotlib.figure import Figure

from ExperimentData import ExperimentData
from AnalysisData import AnalysisData
from EnAData import FiledEnAData

class DisplayAnalysis:
    """Class that takes experiment and analysis filed data and gives functions to display and modify it.
    """

    fd: FiledEnAData
    ed: ExperimentData
    ad: AnalysisData

    def __init__(
            self,
            FEnAd: FiledEnAData,
    ):
        self.fd = FEnAd
        self.ed = FEnAd.FED.d
        self.ad = FEnAd.FAD.d

    def plt_popd(self) -> Figure:
        fig, ax = plt.subplots()
        ax.plot(self.ed.popd['Time step'], self.ed.popd['Prey number'], 'b', label = 'Prey')
        ax.plot(self.ed.popd['Time step'], self.ed.popd['Predator number'], 'r', label = 'Predators')
        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.grid(True)
        ax.legend()
        return fig

    def pmft(self, timestamp: int) -> AxesImage:
        """Returns the point map at a fixed time timestamp as an image.

        Args:
            timestamp (int): fixed time

        Returns:
            AxesImage: pmft image
        """
        pm_ft = self.ad.pmd[timestamp]
        arr = np.array(pm_ft)
        image = plt.imshow(arr)
        return image
    
    def show_pmft(self, timestamp: int):
        """Calculate and shows point map at fixed time point.

        Args:
            timestamp (int): Time point
        """
        self.pmft(timestamp)
        plt.show()    