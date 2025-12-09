import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    pass


@app.cell
def _():
    import sys
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt

    from Analyser import Analyser
    return Analyser, Path, mo, plt


@app.cell
def _(Path, mo):
    folder_list = list()
    parent = Path(__file__).parent / 'data'
    for folder_path in parent.iterdir():
        folder_list.append(str(folder_path.relative_to(parent)))


    look_in = mo.ui.radio(folder_list, value = 'output')
    mo.output.append(look_in)
    return look_in, parent


@app.cell
def _(look_in, mo, parent):
    experiment_list = list()
    subdir = look_in.value

    path = parent / subdir
    print(path)
    for experiment_path in path.iterdir():
        experiment_list.append(str(experiment_path.relative_to(path)))

    experiment_radio = mo.ui.radio(experiment_list)
    mo.output.append(experiment_radio)
    return experiment_radio, subdir


@app.cell
def _(Analyser, experiment_radio, subdir):
    exp_folder = subdir + '/' + experiment_radio.value
    exp_name = experiment_radio.value
    an = Analyser(exp_folder, exp_name)
    return (an,)


@app.cell
def _(an, mo):
    timestamp1 = mo.ui.slider(start=0, stop = an.nts - 1, step=1)
    # timestamp2 = mo.ui.number(value = 0, stop = num_time_stamps - 1)
    return (timestamp1,)


@app.cell
def _(an):
    fig = an.plt_nums()
    return (fig,)


@app.cell
def _(an, timestamp1):
    timestamp = timestamp1.value
    #timestamp = timestamp2.value
    pm = an.pmft(timestamp)
    return (pm,)


@app.cell
def _(an, mo):
    mo.ui.table(an.nums)
    return


@app.cell
def _(fig):
    fig
    return


@app.cell
def _(timestamp1):
    timestamp1
    # timestamp2
    return


@app.cell
def _(plt, pm):
    plt.imshow(pm)
    return


if __name__ == "__main__":
    app.run()
