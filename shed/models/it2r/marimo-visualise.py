import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt

    from Analyser import Analyser
    from DataHandler import DataHandler
    return Analyser, DataHandler, mo


@app.cell
def _(DataHandler, mo):
    dh = DataHandler()

    look_in = mo.ui.radio(dh.dfos, value = 'output')
    refresh = mo.ui.refresh()
    return dh, look_in, refresh


@app.cell
def _(Analyser, experiment_radio, subdir):
    exp_name = experiment_radio.value
    exp_folder = subdir + '/' + exp_name
    an = Analyser(exp_folder, exp_name)
    return (an,)


@app.cell
def _(an):
    fig = an.plt_nums()
    return (fig,)


@app.cell
def _(an, mo):
    timestamp1 = mo.ui.slider(start=0, stop = an.nts - 1, step=1, full_width=True)
    # timestamp2 = mo.ui.number(value = 0, stop = num_time_stamps - 1)
    return (timestamp1,)


@app.cell
def _(an, timestamp1):
    timestamp = timestamp1.value
    #timestamp = timestamp2.value
    img = an.pmft(timestamp)
    return (img,)


@app.cell
def _(dh, look_in, mo, refresh):
    subdir = look_in.value
    experiment_list = dh.expl(subdir)

    experiment_radio = mo.ui.radio(experiment_list, value = experiment_list[0])
    refresh
    return experiment_radio, subdir


@app.cell
def _(mo):
    mo.md(r"""
    #Experiment analysis
    ##Choose experiment folder:
    ###If you want to see the output of a run then it will be in the output folder.
    """)
    return


@app.cell
def _(look_in, mo):
    mo.output.append(look_in)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Experiment folders:
    """)
    return


@app.cell
def _(experiment_radio, mo):
    mo.output.append(experiment_radio)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Experiment data:
    ###It shows population count of prey and predators per turn.
    """)
    return


@app.cell
def _(an, mo):
    mo.ui.table(an.nums)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Plot of population data:
    """)
    return


@app.cell
def _(fig):
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Distribution image
    ###An image showing the distribution of predators and prey across the map a particular timestamp.

    More red in a pixel indicates more predators are at that point in the graph and more blue indicates more prey are at that point in the graph.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###Choose time step:
    """)
    return


@app.cell
def _(timestamp1):
    timestamp1
    # timestamp2
    return


@app.cell
def _(img):
    img
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Parameters
    """)
    return


@app.cell
def _(an, mo):
    mo.output.append(an.params)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Notes
    """)
    return


@app.cell
def _(an, mo):
    text = an.notes()
    text_area = mo.ui.text_area(text)
    mo.output.append(text_area)
    return (text_area,)


@app.cell
def _(mo, submit_notes_button):
    mo.output.append(submit_notes_button)
    return


@app.cell
def _(an, mo, text_area):
    def submit_notes(event):
        text = text_area.value
        an.up_notes(text)
        mo.output.append('Submitted!')

    submit_notes_button = mo.ui.button(label = 'Save', on_click = submit_notes)
    return (submit_notes_button,)


if __name__ == "__main__":
    app.run()
