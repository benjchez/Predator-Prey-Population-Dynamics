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

    def prey_timeseries(self) -> Figure:

        fig, ax = plt.subplots()

        max_in_num_prey = 0

        for i in range(len(self.l)):
            popd = self.l[i].FED.d.popd
            ax.plot(popd['Time step'], popd['Prey number'], label = 'Prey line ' + str(i))

            in_num_prey = self.l[i].FED.d.paramd["Graph options"]["init_num_prey"]

            if in_num_prey > max_in_num_prey:
                max_in_num_prey = in_num_prey

        ax.set_ylim(bottom = 0, top = max_in_num_prey * 4)

        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.set_title('Prey Counts Against Time')

        ax.grid(True)
        ax.legend()
        return fig

    def pred_timeseries(self) -> Figure:

        fig, ax = plt.subplots()

        for i in range(len(self.l)):
            popd = self.l[i].FED.d.popd
            ax.plot(popd['Time step'], popd['Predator number'], label = 'Predators ' + str(i))


        ax.set_xlabel('Time step')
        ax.set_ylabel('Population number')
        ax.set_title('Prey Counts Against Time')

        ax.grid(True)
        ax.legend()
        return fig