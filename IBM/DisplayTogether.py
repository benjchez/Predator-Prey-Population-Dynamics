from pathlib import Path

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from DisplayAnalysis import DisplayAnalysis

class DisplayTogether:

    displayers: list [DisplayAnalysis]
    name: str
    lite: bool

    def __init__(
            self,
            list_of_displayers: list[DisplayAnalysis],
            name: str,
    ):
        self. displayers = list_of_displayers

        if len(list_of_displayers) == 0:
            raise ValueError ("No experiments to display in class DisplayTogether.")

        self. name = name

        self. lite = False

        for displayer in list_of_displayers:
            if displayer.lite:
                self.lite = True
    
    @classmethod
    def from_root_name (
        cls,
        root_name: str,
        experiment_folder: str,
        lite: bool = False,
    ) -> 'DisplayTogether':
        
        i = 1

        list_of_displayers = []

        while True:

            experiment_name = root_name + '_' + str (i)

            try:
                displayer = DisplayAnalysis. from_files (
                    experiment_name = experiment_name,
                    experiment_folder = experiment_folder,
                    lite = lite,
                )

                list_of_displayers. append (displayer)

                print (i)

                i += 1

            except ValueError:
                break

        return cls (
            list_of_displayers = list_of_displayers,
            name = root_name,
        )

    def num_experiments (
            self,
    ) -> int:
        """Returns the number of experiments in the instantiation."""

        return len (self. displayers)

    def together_time_series(
            self,
            from_range: int,
            to_range: int,
            xlabel: str,
            ylabel: str,
            add_title: bool,
            title: str,
            grid: bool,
            add_legend: bool,
            data: list,
            line_labels: list,

            do_x_rescale: bool = False,
            x_rescale_which: list [int] | None = None,
            x_scaler: float = 1,
    ) -> tuple [Figure, Axes]:
        """Together time series."""

        if x_rescale_which is None:
            x_rescale_which = []

        assert len (data) == len (line_labels)

        fig, ax = plt.subplots()

        for i in range (len (data) ):

            number_of_turns = len (data [i] )

            up_to = min (number_of_turns - 1, to_range) 

            if not do_x_rescale or (do_x_rescale and i not in x_rescale_which):
                ax. plot (range (from_range, up_to + 1), data [i] [from_range: up_to + 1], label = line_labels [i] )

            else:
                xs = list (range (from_range, up_to + 1) )
                
                xs_scaled = [x * x_scaler for x in xs]

                ax. plot (xs_scaled, data [i] [from_range: up_to + 1], label = line_labels [i] )                    



        ax. set_xlabel (xlabel)
        ax. set_ylabel (ylabel)

        if add_title:
            ax. set_title (title)

        ax. grid (grid)

        if add_legend:
            ax. legend ()

        return fig, ax

    def prey_time_series(
            self,

            i: int = 0,
            j: int | None = None,
            xlabel: str = 'Turn',
            ylabel: str = 'Population',
            add_title: bool = True,
            title: str = 'Prey Count against Time',
            grid: bool = True,
            add_legend: bool = True,
            line_labels: list | None = None,

            set_ymax: bool = False,
            ymax: int | None = None,

            do_x_rescale: bool = False,
            x_rescale_which: list [int] | None  = None,
            x_scaler: float = 1,
    ) -> Figure:

        fig, ax = plt.subplots()

        max_in_num_prey = 0

        data = []

        default_labels = []

        for k in range(len(self. displayers)):

            popd = self. displayers [k]. ed. popd

            data. append (popd ['Prey number'] )

            default_labels. append ('Experiment ' + str(k + 1))

            in_num_prey = self. displayers [k]. ed. paramd ["Graph options"] ["init_num_prey"]

            if in_num_prey > max_in_num_prey:
                max_in_num_prey = in_num_prey


        if line_labels is None:
            line_labels = default_labels

        end = j if j is not None else max (
            displayer. ed. popd ['Time step']. iloc [-1] for displayer in self.displayers
        )

        fig, ax = self. together_time_series (
            from_range = i,
            to_range = end,
            xlabel = xlabel,
            ylabel = ylabel,
            add_title = add_title,
            title = title,
            grid = grid,
            add_legend = add_legend,
            data = data,
            line_labels = line_labels,

            do_x_rescale = do_x_rescale,
            x_rescale_which = x_rescale_which,
            x_scaler = x_scaler,
        )

        if set_ymax:
            if ymax is None:
                ymax = max_in_num_prey * 4
            ax. set_ylim (bottom = 0, top = ymax)

        return fig

    def pred_time_series(
            self,

            i: int = 0,
            j: int | None = None,
            xlabel: str = 'Turn',
            ylabel: str = 'Population',
            add_title: bool = True,
            title: str = 'Predator Count against Time',
            grid: bool = True,
            add_legend: bool = True,
            line_labels: list | None = None,

            do_x_rescale: bool = False,
            x_rescale_which: list [int] | None = None,
            x_scaler: float = 1,

            set_ymax: bool = False,
            ymax: int | None = None,
    ) -> Figure:

        fig, ax = plt.subplots()

        max_in_num_pred = 0

        data = []

        default_labels = []

        for k in range(len(self. displayers)):

            popd = self. displayers [k]. ed. popd

            data. append (popd ['Predator number'] )

            default_labels. append ('Experiment ' + str(k + 1))

            in_num_pred = self. displayers [k]. ed. paramd ["Graph options"] ["init_num_pred"]

            if in_num_pred > max_in_num_pred:
                max_in_num_pred = in_num_pred

        if line_labels is None:
            line_labels = default_labels

        end = j if j is not None else max (
            displayer. ed. popd ['Time step']. iloc [-1] for displayer in self.displayers
        )

        fig, ax = self. together_time_series (
            from_range = i,
            to_range = end,
            xlabel = xlabel,
            ylabel = ylabel,
            add_title = add_title,
            title = title,
            grid = grid,
            add_legend = add_legend,
            data = data,
            line_labels = line_labels,

            do_x_rescale = do_x_rescale,
            x_rescale_which = x_rescale_which,
            x_scaler = x_scaler,
        )


        if set_ymax:
            if ymax is None:
                ymax = max_in_num_pred * 4

            ax. set_ylim (bottom = 0, top = ymax)

        return fig
    
    def rho_ests_time_series(
            self,
            i: int = 0,
            j: int | None = None,
            xlabel: str = 't',
            ylabel: str = r'$\rho_{\text {est} } (0, t)$',
            add_title: bool = True,
            title: str = r'Change in $\rho_{\text {est} } (0, t)$ over Time',
            grid: bool = True,
            add_div_nm_line: bool = False,
            add_legend: bool = True,
            line_labels: list | None = None,
    ) -> Figure:
        """if add_div_nm_line, it adds the one for the first data."""

        fig, ax = plt.subplots()

        data = []

        default_line_labels = []

        for k in range (len (self. displayers) ):

            displayer = self. displayers [k]

            ed = displayer. ed

            end = j if j is not None else ed. popd ['Time step']. iloc [-1]

            data. append (displayer. calculate_rho_ests (i, end) )

            default_line_labels. append (f'Experiment {k + 1}')

        end = j if j is not None else max (
            displayer. ed. popd ['Time step']. iloc [-1] for displayer in self.displayers
        )

        if not line_labels:
            line_labels = default_line_labels

        fig, ax = self. together_time_series (
            from_range = i,
            to_range = end,
            xlabel = xlabel,
            ylabel = ylabel,
            add_title = add_title,
            title = title,
            grid = grid,
            add_legend = add_legend,
            data = data,
            line_labels = line_labels,
        )

        if add_div_nm_line:
            m = self. displayers [0]. ed. paramd ["Graph options"] ["row_num"]
            n = self. displayers [0]. ed. paramd ["Graph options"] ["col_num"]
            
            ax. axhline (y = 1 / (m * n), color = 'red', label = r'$1 / (m \times n)$')

        return fig
    
    def average_rho_est (
            self,
    ) -> float:
        """Calculates the average rho_est value for the different experiments for 0 to end."""

        total = 0

        number_of_displayers = len (self. displayers)

        for i in range (number_of_displayers):

            displayer = self. displayers [i]

            ed = displayer. ed

            end = ed. popd ['Time step']. iloc [-1]

            total += displayer. calculate_rho_est (0, end)

        total /= number_of_displayers

        return total
    
    
def save_together_plot (
        fig: Figure,
        save_as: str,
        width: float | None = None,
        height: float | None = None,
):
    """Give the name and extension in save_as."""

    folderpath = get_together_plots_folder ()

    folderpath. mkdir (parents = True, exist_ok = True)
    
    save_as_path = folderpath / save_as

    if width and height:
        fig. set_size_inches (w = width, h = height)

    fig. savefig (
        save_as_path,
        bbox_inches = 'tight',
    )

def get_together_plots_folder () -> Path:
    return Path(__file__).parent / 'together_plots'