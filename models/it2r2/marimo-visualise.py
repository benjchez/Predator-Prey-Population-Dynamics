import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt

    from Analyser import Analyser
    from FileHelper import FileHelper
    from EnAData import FiledEnAData
    from DisplayAnalysis import DisplayAnalysis
    return DisplayAnalysis, FileHelper, FiledEnAData, mo


@app.cell
def _(FileHelper, mo):
    dh = FileHelper()

    look_in = mo.ui.radio(dh.dfos, value = 'output')
    refresh = mo.ui.refresh()
    return dh, look_in, refresh


@app.cell
def _(DisplayAnalysis, FiledEnAData, experiment_radio, got_experiment, subdir):
    if got_experiment == True:
        exp_name = experiment_radio.value
        exp_folder = subdir
    
        FEnAd = FiledEnAData.from_files(data_folder = exp_folder, experiment_name = exp_name)
        disp = DisplayAnalysis(FEnAd)
    return (disp,)


@app.cell
def _(disp, got_experiment):
    if got_experiment == True:
        fig = disp.plt_popd()
    else:
        fig = 'No figure'
    return (fig,)


@app.cell
def _(disp, got_experiment, mo):
    if got_experiment == True:
        num_time_stamps = disp.ad.infod['number of time stamps']

        num_time_steps = num_time_stamps - 1

        timestamp1 = mo.ui.slider(start=0, stop = num_time_steps, step=1, full_width=True)
        # timestamp2 = mo.ui.number(value = 0, stop = num_time_steps)
    return (timestamp1,)


@app.cell
def _(disp, got_experiment, timestamp1):
    if got_experiment == True:
        timestamp = timestamp1.value
        # timestamp = timestamp2.value
        img = disp.pmft(timestamp)
    return (img,)


@app.cell
def _(dh, look_in, mo, refresh):
    subdir = look_in.value
    experiment_list = dh.expl(subdir)
    if len(experiment_list) == 0:
        experiment_radio = "Choose a folder with experiments saved in it. If no folders have experiments saved in them, run an experiment in marimo-run.py."
        got_experiment = False
    else:
        experiment_radio = mo.ui.radio(experiment_list, value = experiment_list[0])
        got_experiment = True
    refresh
    return experiment_radio, got_experiment, subdir


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
    ##Experiment:
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
def _(disp, mo):
    mo.ui.table(disp.ed.popd)
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
def _(disp, mo):
    mo.output.append(disp.ed.paramd)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ##Notes
    """)
    return


@app.cell
def _(disp, mo):
    text = disp.ad.notesd
    text_area = mo.ui.text_area(text)
    mo.output.append(text_area)
    return (text_area,)


@app.cell
def _(mo, submit_notes_button):
    mo.output.append(submit_notes_button)
    return


@app.cell
def _(disp, mo, text_area):
    def submit_notes(event):
        text = text_area.value
        disp.fd.FAD.write_notes(text)
        mo.output.append('Submitted!')

    submit_notes_button = mo.ui.button(label = 'Save', on_click = submit_notes)
    return (submit_notes_button,)


if __name__ == "__main__":
    app.run()
