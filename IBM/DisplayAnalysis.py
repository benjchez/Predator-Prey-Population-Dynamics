from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

from ExperimentData import ExperimentData
from AnalysisData import AnalysisData
from EnAData import FiledEnAData

class DisplayAnalysis:
    """Class that takes experiment and analysis filed data and gives functions to display and modify it.
    """

    fd: FiledEnAData
    ed: ExperimentData
    ad: AnalysisData
    lite: bool

    def __init__(
            self,
            FEnAD: FiledEnAData,
    ):
        self.fd = FEnAD
        self.ed = FEnAD.FED.d
        self.ad = FEnAD.FAD.d

        self. lite = FEnAD. lite

    @classmethod
    def from_files (
        cls,
        experiment_name: str,
        experiment_folder: str,
        lite: bool = False,
    ) -> 'DisplayAnalysis':
        
        FEnAD = FiledEnAData. from_files (
            data_folder = experiment_folder,
            experiment_name = experiment_name,
            lite = lite,
        )

        return cls (
            FEnAD = FEnAD,
        )

    def plt_popd(
            self,
            ymax: float | None = None,
            plot_prey: bool = True,
            plot_predators: bool = True,
            twin_axes: bool = False,
            add_title: bool = True,
        ) -> Figure:
        """plot_prey and plot_predators must be true if twin_axes is true."""

        prey_colour = 'b' # Blue
        pred_colour = 'r' # Red

        fig, ax = plt.subplots()

        if twin_axes and (not plot_prey or not plot_predators):
            raise ValueError ('Cannot have twin_axes true as well as either plot_prey or plot_predators false.')

        if plot_prey:
            ax.plot(self.ed.popd['Time step'], self.ed.popd['Prey number'], prey_colour, label = 'Prey')

        if plot_predators and not twin_axes:
            ax.plot(self.ed.popd['Time step'], self.ed.popd['Predator number'], 'r', label = 'Predators')
        
        if twin_axes:
            ax2 = ax. twinx ()

            ax2. plot (self.ed.popd['Time step'], self.ed.popd['Predator number'], pred_colour, label = 'Predators')

            ax. set_ylabel ('Prey Population', color = prey_colour)
            ax2. set_ylabel ('Predator Population', color = pred_colour)

            ax. tick_params (axis = 'y', labelcolor = prey_colour)
            ax2.tick_params(axis='y', labelcolor = pred_colour)
        
        else:
            ax.set_ylabel('Population number')

        if ymax is not None:
            ax.set_ylim(bottom = 0, top = ymax)

        ax.set_xlabel('Turn')
        
        if add_title:
            ax.set_title('Prey and Predator Population Counts Against Time')

        ax.grid(True)

        if not twin_axes:
            ax.legend()

        return fig
    
    def show_populations_plot (self):
        self. plt_popd ()
        plt. show ()

    def plt_pairs (self) -> Figure:
        fig, ax = plt.subplots()

        ax.plot(self.ed.popd['Time step'], self.ed.popd['Predator-prey pairs'])

        ax.set_xlabel('Time step')
        ax.set_ylabel('Pairs')
        ax.set_title('Number of Pairs Against Time')

        ax.grid(True)
        
        return fig
    
    def total_pairs (self) -> int:
        return self. ed. popd ['Predator-prey pairs']. sum ()
    
    def total_pairs_from_i_to_j (self, i: int, j: int) -> int:
        """Sums the individual predator-prey pairs at every turn from i up to and including j."""

        if not j >= i:
            raise ValueError ('j should be greater or equal to i')
        
        return self. ed. popd ['Predator-prey pairs'] [i: j + 1]. sum ()
    
    def sum_of_xy_over_all_time (self) -> int:
        """Sums the value of x * y at every turn."""
        return (self. ed. popd ['Prey number'] * self. ed. popd ['Predator number']). sum ()
    
    def sum_of_xy_from_i_to_j (self, i: int, j: int) -> int:
        """Sums the value of x * y at every turn in i, i + 1, ..., j."""

        if not j >= i:
            raise ValueError ('j should be greater or equal to i')
        
        return (self. ed. popd ['Prey number'] * self. ed. popd ['Predator number'] ) [i: j + 1]. sum ()
    
    def calculate_rho_est (self, i: int, j: int) -> float:
        """Calculates rho_est (i, j)."""

        return self. total_pairs_from_i_to_j (i, j) / self. sum_of_xy_from_i_to_j (i, j)

    def calculate_rho_ests (self, i: int, j: int) -> list:
        """Calculates rho_est (i, k) for k = i, i + 1, ..., j."""

        rho_ests = []

        if not j >= i:
            raise ValueError ('j should be greater or equal to i')     

        for k in range (i, j + 1):
            rho_ests. append (self. calculate_rho_est (i, k) )

        return rho_ests
    
    def plt_rho_ests (
            self, i: int = 0, j: int  = -1,
            xlabel: str = 't',
            ylabel: str = r'$\rho_{\text {est} } (0, t)$',
            add_title: bool = True,
            title: str = r'Change in $\rho_{\text {est} } (0, t)$ over Time',
            grid: bool = True,
            add_div_nm_line: bool = False,
            width: float | None = None,
            height: float | None = None,
        ) -> Figure:
        """Plots rho_est (i, k) for k = i, i + 1, ..., j."""

        if j == -1:
            j = self. ed. popd ['Time step']. iloc [-1]

        fig, ax = plt. subplots ()

        data = self. calculate_rho_ests (i, j)

        ax. plot (data, label = r"$\rho_{\text {est} } (0, t)$")

        if add_div_nm_line:
            m = self. ed. paramd ["Graph options"] ["row_num"]
            n = self. ed. paramd ["Graph options"] ["col_num"]

            ax. axhline (y = 1 / (m * n), color = 'red', label = r'$1 / (m \times n)$')

            ax. legend ()

        ax. set_xlabel (xlabel)
        ax. set_ylabel (ylabel)

        if add_title:
            ax. set_title (title)

        ax. grid (grid)

        if width and height:
            fig. set_size_inches (
                w = width,
                h = height,
            )
        
        return fig

    def plt_pairs_div_xy (
            self,
            xlabel: str = 'Time Step',
            ylabel: str = 'Pairs / $xy$',
            add_title: bool = True,
            title: str = 'Number of Pairs divided by $xy$ Against Time',
            grid: bool = True,
            add_div_nm_line: bool = False,
            scatter_plot: bool = False,
            width: float | None = None,
            height: float | None = None,
    ) -> Figure:
        """Plot number of predator-prey pairs divided by prey pop x * predator pop y against time."""

        fig, ax = plt. subplots ()


        if scatter_plot:
            ax. scatter (
                self. ed. popd ['Time step'],
                self. ed. popd ['Predator-prey pairs'] / (self.ed.popd ['Prey number'] * self.ed.popd ['Predator number'] ),
                label = r'$\rho_{\text{sim}}(t)$',
                s = 20,
            )
            
        else:
            ax. plot (
                self. ed. popd ['Time step'],
                self. ed. popd ['Predator-prey pairs'] / (self.ed.popd ['Prey number'] * self.ed.popd ['Predator number'] ),
                label = r'$\rho_{\text{sim}}(t)$',
            )

        ax. set_xlabel (xlabel)
        ax. set_ylabel (ylabel)

        if add_div_nm_line:
            m = self. ed. paramd ["Graph options"] ["row_num"]
            n = self. ed. paramd ["Graph options"] ["col_num"]

            ax. axhline (y = 1 / (m * n), color = 'red', label = r'$1 / (m \times n)$')

            ax. legend ()

        if add_title:
            ax. set_title (title)

        ax. grid (grid)

        if width and height:
            fig. set_size_inches (
                w = width,
                h = height,
            )
        
        return fig
    
    def plt_phase_portrait(
            self,
            scatter_plot: bool = True,
            add_title: bool = True,

            xlabel: str = 'Number of prey',
            ylabel: str = 'Number of predators',

            width: float | None = None,
            height: float | None = None,
    ) -> Figure:
        """Plot a phase portrait of the number of prey against the number of predators at each timestamp.

        Returns:
            Figure: Returns the figure as a matplotlib object
        """
        
        fig, ax = plt.subplots()

        if scatter_plot:
            sc = ax.scatter(self.ed.popd['Prey number'], self.ed.popd['Predator number'], c = self.ed.popd['Time step'], cmap = 'viridis', s = 2, label = 'Trajectory')

            cbar = fig.colorbar(sc, ax=ax)
            cbar.set_label('Time')

        else:
            ax.plot(
                self.ed.popd['Prey number'],
                self.ed.popd['Predator number'],
            )





        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if add_title:
            ax.set_title("Phase Portrait of Predator Population Counts Against Prey's at each Timestamp")

        ax.grid(visible = True)

        if width and height:
            fig. set_size_inches (
                w = width,
                h = height,
            )

        return fig

    def pmft(self, timestamp: int) -> Figure:
        """(Point Map Fixed Time) - Returns the point map at a fixed time timestamp as an image.

        Args:
            timestamp (int): fixed time

        Returns:
            Figure: gpmft image
        """

        if self. lite:
            raise ValueError ('Cannot plot point map in lite mode')
        
        assert self. ad. pmd is not None

        pm_ft = self.ad.pmd[timestamp]
        arr = np.array(pm_ft)
        fig, ax = plt.subplots()
        ax.imshow(arr, origin = 'lower')
        return fig
    
    def show_pmft(self, timestamp: int):
        """Calculates and shows point map at fixed time point.

        Args:
            timestamp (int): Time point
        """

        self.pmft(timestamp)
        plt.show()

    def save_pmft (
            self, 
            ts: int, # timestamp
    ):
        """Saves a point map fixed time picture for the given timestamp as `t{ts}.pdf` in `pms` folder under the `plots` folder.
        
        Args:
            ts (int): Timestamp"""
        
        # fn - file name
        # fop - folder path
        # fp - file path

        fn = f"t{ts}.pdf" # eg t1.pdf
        fop = self. get_plots_folder () / 'pms'
        fp = fop / fn

        # Makes the necessary folders if they don't exist
        fop. mkdir (parents = True, exist_ok = True)

        # Generates point map
        fig = self. pmft (timestamp = ts)

        # Saves it. bbox_inches tight removes unnecessary space on the sides of the pdf
        fig. savefig (fname = fp, bbox_inches = 'tight')

    def save_all_plots(self):
        self.save_point_map_video()
        self.save_population_time_series()
        self.save_population_time_series_png()
        self.save_phase_portrait()
        self.save_phase_portrait_png()

    def save_point_map_video(self):

        if self. lite:
            raise ValueError ('Cannot plot point map in lite mode')
        
        assert self. ad. pmd is not None

        number_of_timestamps = len(self.ad.pmd)

        artists = []

        fig, ax = plt.subplots()

        for timestamp in range(number_of_timestamps):
            pm_ft = self.ad.pmd[timestamp]
            arr = np.array(pm_ft)
            container = ax.imshow(arr, origin = 'lower')
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

    def save_population_time_series_png(
            self,
    ):
        fig = self.plt_popd()

        filename = "pop-ts.png"
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

    def save_phase_portrait_png(
            self,
    ):
        fig = self.plt_phase_portrait()

        filename = "phase-portrait.png"
        folderpath = self.fd.dir / 'plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )
    
    def heat_map (self):
        """For each point, sums the number of animals every turn and displays this as a heat map."""


        if self. lite:
            raise ValueError ('Cannot plot heat map in lite mode')
        
        assert self. ed. graphd is not None

        self.cn = self.ed.paramd['Graph options']['col_num']
        self.rn = self.ed.paramd['Graph options']['row_num']

        num_time_stamps = len(self.ed.graphd.columns)

        # hm - heat map
        hm = [[0. for _ in range(self.cn)] for _ in range(self.rn)]

        for t in range(num_time_stamps):

            graph = self.ed.graphd['timestamp' + str(t)]

            for row in range(self.rn):
                for column in range(self.cn):
                    point = graph[row][column]

                    animals = point [0] + point [1]

                    hm[row][column] += animals


        max_value = 0

        for row in range(self.rn):
            for column in range(self.cn):
                point_value = hm[row][column]

                if point_value > max_value:
                    max_value = point_value

        if max_value == 0:
            max_value = 1

        scale = 1 / max_value

        for row in range(self.rn):
            for column in range(self.cn):
                hm[row][column] *= scale

        arr = np.array(hm)
        fig, ax = plt.subplots()

        im = ax.imshow(arr, origin = 'lower', cmap = 'hot')
        fig.colorbar(im, ax = ax, label = 'Total animals divided by max value')

        return fig

    def show_heat_map (self):
        self. heat_map ()
        plt. show ()

    def get_plots_folder (self) -> Path:
        """Returns the folder where plots are to be saved in and makes it if it doesn't yet exist."""
        
        directory = self. fd. dir / 'plots'

        directory. mkdir (exist_ok = True)

        return directory
    
    def save_plot (
            self,
            fig: Figure,
            save_as: str,
            width: float | None = None,
            height: float | None = None,
    ):
        """Give the name and extension in save_as."""
        
        save_as_path = self. get_plots_folder () / save_as

        if width and height:
           fig. set_size_inches (w = width, h = height)

        fig. savefig (
            save_as_path,
            bbox_inches = 'tight',
        )