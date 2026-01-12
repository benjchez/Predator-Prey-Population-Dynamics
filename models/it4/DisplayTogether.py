from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from DisplayAnalysis import DisplayAnalysis
from EnAData import FiledEnAData

class DisplayTogether:
    def __init__(
            self,
            list_of_FEnAD: list[FiledEnAData],
    ):
        self.l = list_of_FEnAD

        if len(list_of_FEnAD) == 0:
            raise ValueError("No experiments to display in class DisplayTogether.")
        
        first_experiment_name = list_of_FEnAD[0].FED.d.paramd["Experiment options"]["experiment_name"]

        self.root_name = first_experiment_name[:-2]


    @classmethod
    def from_displayers(
            cls,
            list_of_displayers: list[DisplayAnalysis]
    ) -> "DisplayTogether":
        list_of_FEnAD: list[FiledEnAData] = []
        for displayer in list_of_displayers:
            list_of_FEnAD.append(displayer.fd)
        
        return cls(
            list_of_FEnAD = list_of_FEnAD,
        )

    def prey_time_series(
            self,
            ymax: int | None = None,
        ) -> Figure:

        fig, ax = plt.subplots()

        max_in_num_prey = 0

        for i in range(len(self.l)):
            popd = self.l[i].FED.d.popd
            ax.plot(popd['Time step'], popd['Prey number'], label = 'Experiment ' + str(i + 1))

            in_num_prey = self.l[i].FED.d.paramd["Graph options"]["init_num_prey"]

            if in_num_prey > max_in_num_prey:
                max_in_num_prey = in_num_prey
        
        if ymax is None:
            ymax = max_in_num_prey * 4

        ax.set_ylim(bottom = 0, top = ymax)

        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.set_title('Prey Counts Against Time')

        ax.grid(True)
        ax.legend()
        
        return fig

    def pred_time_series(
            self,
            ymax: int | None = None,
    ) -> Figure:

        fig, ax = plt.subplots()

        max_in_num_pred = 0

        for i in range(len(self.l)):
            popd = self.l[i].FED.d.popd
            ax.plot(popd['Time step'], popd['Predator number'], label = 'Experiment ' + str(i + 1))

            in_num_pred = self.l[i].FED.d.paramd["Graph options"]["init_num_pred"]

            if in_num_pred > max_in_num_pred:
                max_in_num_pred = in_num_pred

        if ymax is None:
            ymax = max_in_num_pred * 4

        ax.set_ylim(bottom = 0, top = ymax)

        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.set_title('Predator Counts Against Time')

        ax.grid(True)
        ax.legend()

        return fig
    
    def save_prey_time_series(
            self,
            ymax: int | None = None,
        ):

        fig = self.prey_time_series(ymax)

        filename = self.root_name + "-prey-ts.pdf"
        folderpath = Path(__file__).parent / 'together_plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )

    def save_prey_time_series_png(
            self,
            ymax: int | None = None,
        ):

        fig = self.prey_time_series(ymax)

        filename = self.root_name + "-prey-ts.png"
        folderpath = Path(__file__).parent / 'together_plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )


    def save_pred_time_series(
            self,
            ymax: int | None = None,
        ):

        fig = self.pred_time_series(ymax)

        filename = self.root_name + "-pred-ts.pdf"
        folderpath = Path(__file__).parent / 'together_plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )

    def save_pred_time_series_png(
            self,
            ymax: int | None = None,
        ):

        fig = self.pred_time_series(ymax)

        filename = self.root_name + "-pred-ts.png"
        folderpath = Path(__file__).parent / 'together_plots'
        filepath = folderpath / filename

        folderpath.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            fname = filepath,
        )