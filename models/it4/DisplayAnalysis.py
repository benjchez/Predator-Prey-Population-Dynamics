import numpy as np

import matplotlib.animation as animation
import matplotlib.pyplot as plt
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
            FEnAD: FiledEnAData,
    ):
        self.fd = FEnAD
        self.ed = FEnAD.FED.d
        self.ad = FEnAD.FAD.d
    


    def plt_popd(self, ymax: float | None = None) -> Figure:
        fig, ax = plt.subplots()
        ax.plot(self.ed.popd['Time step'], self.ed.popd['Prey number'], 'b', label = 'Prey')
        ax.plot(self.ed.popd['Time step'], self.ed.popd['Predator number'], 'r', label = 'Predators')

        if ymax is not None:
            ax.set_ylim(bottom = 0, top = ymax)

        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.set_title('Prey and Predator Population Counts Against Time')

        ax.grid(True)
        ax.legend()
        return fig
    
    def plt_phase_portrait(
            self
    ) -> Figure:
        """Plot a phase portrait of the number of prey against the number of predators at each timestamp.

        Returns:
            Figure: Returns the figure as a matplotlib object
        """
        fig, ax = plt.subplots()

        # ax.plot(self.ed.popd['Prey number'], self.ed.popd['Predator number'])

        sc = ax.scatter(self.ed.popd['Prey number'], self.ed.popd['Predator number'], c = self.ed.popd['Time step'], cmap = 'viridis', s = 2, label = 'Trajectory')

        cbar = fig.colorbar(sc, ax=ax)
        cbar.set_label('Time')

        ax.set_xlabel('Number of prey')
        ax.set_ylabel('Number of predators')
        ax.set_title("Phase Portrait of Predator Population Counts Against Prey's at each Timestamp")

        ax.grid(visible = True)

        return fig

    def pmft(self, timestamp: int) -> Figure:
        """Returns the point map at a fixed time timestamp as an image.

        Args:
            timestamp (int): fixed time

        Returns:
            Figure: gpmft image
        """
        pm_ft = self.ad.pmd[timestamp]
        arr = np.array(pm_ft)
        fig, ax = plt.subplots()
        ax.imshow(arr)
        return fig
    
    def show_pmft(self, timestamp: int):
        """Calculate and shows point map at fixed time point.

        Args:
            timestamp (int): Time point
        """
        self.pmft(timestamp)
        plt.show()

    def save_all_plots(self):
        self.save_point_map_video()
        self.save_population_time_series()
        self.save_phase_portrait()

    def save_point_map_video(self):
        number_of_timestamps = len(self.ad.pmd)

        artists = []

        fig, ax = plt.subplots()

        for timestamp in range(number_of_timestamps):
            pm_ft = self.ad.pmd[timestamp]
            arr = np.array(pm_ft)
            container = ax.imshow(arr)
            artists.append([container])
            
        
        self.animation = animation.ArtistAnimation(fig = fig, artists = artists, interval = 200)

        name = "pointmap.mp4"
        folderpath = self.fd.dir / 'plots'
        filepath = folderpath / name

        folderpath.mkdir(parents=True, exist_ok=True)

        # self.animation.save(filename = filename, writer = "pillow")
        self.animation.save(filename = filepath, writer="ffmpeg", bitrate=-1)
        # dpi = 300
    
    def save_population_time_series(
            self,
    ):
        fig = self.plt_popd()

        filename = "pop-ts.pdf"
        folderpath = self.fd.dir / 'plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )
        
    def save_phase_portrait(
            self,
    ):
        fig = self.plt_phase_portrait()

        filename = "phase-portrait.pdf"
        folderpath = self.fd.dir / 'plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )