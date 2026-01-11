import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    pass


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
def _(
    DisplayAnalysis,
    FiledEnAData,
    experiment_radio,
    experiment_radio2,
    got_experiment,
    subdir,
):
    if got_experiment == True:
        exp_name = experiment_radio.value
        exp_name2 = experiment_radio2.value
        exp_folder = subdir

        FEnAd = FiledEnAData.from_files(data_folder = exp_folder, experiment_name = exp_name)
        FEnAd2 = FiledEnAData.from_files(data_folder = exp_folder, experiment_name = exp_name2)
        disp = DisplayAnalysis(FEnAd)
        disp2 = DisplayAnalysis(FEnAd2)
    return disp, disp2


@app.cell
def _(disp, disp2, got_experiment, ymax, ymax1):
    if got_experiment == True:
        fig = disp.plt_popd(ymax.value)
        fig2 = disp2.plt_popd(ymax1.value)
    else:
        fig = fig2 = 'No figure'
    return fig, fig2


@app.cell
def _(disp, disp2, got_experiment):
    if got_experiment == True:
        phase_portrait = disp.plt_phase_portrait()
        phase_portrait2 = disp2.plt_phase_portrait()
    else:
        phase_portrait = phase_portrait2 = 'No phase portrait available'
    return phase_portrait, phase_portrait2


@app.cell
def _(disp, disp2, got_experiment, mo, ts_choice, ts_choice2):
    if got_experiment == True:
        num_time_stamps = disp.ad.infod['number of time stamps']
        num_time_stamps2 = disp2.ad.infod['number of time stamps']

        num_time_steps = num_time_stamps - 1
        num_time_steps2 = num_time_stamps2 - 1

        if ts_choice.value == "drag and drop":
            timestamp_specifier = mo.ui.slider(start=0, stop = num_time_steps, step=1, full_width=True)
        elif ts_choice.value == "specify number":
            timestamp_specifier = mo.ui.number(value = 0, stop = num_time_steps)
        else:
            raise Exception("No given timestamp specifier")

        if ts_choice2.value == "drag and drop":
            timestamp_specifier2 = mo.ui.slider(start=0, stop = num_time_steps2, step=1, full_width=True)
        elif ts_choice2.value == "specify number":
            timestamp_specifier2 = mo.ui.number(value = 0, stop = num_time_steps2)
        else:
            raise Exception("No given timestamp specifier")
    return timestamp_specifier, timestamp_specifier2


@app.cell
def _(disp, disp2, got_experiment, timestamp_specifier, timestamp_specifier2):
    if got_experiment == True:
        timestamp = timestamp_specifier.value
        img = disp.pmft(timestamp)

    if got_experiment == True:
        timestamp2 = timestamp_specifier2.value
        img2 = disp2.pmft(timestamp2)
    return img, img2


@app.cell
def _(dh, look_in, mo, refresh):
    subdir = look_in.value
    experiment_list = dh.expl(subdir)
    if len(experiment_list) == 0:
        experiment_radio = "Choose a folder with experiments saved in it. If no folders have experiments saved in them, run an experiment in marimo-run.py."
        experiment_radio2 = ""
        got_experiment = False
    else:
        experiment_radio = mo.ui.radio(experiment_list, value = experiment_list[0])
        experiment_radio2 = mo.ui.radio(experiment_list, value = experiment_list[0])
        got_experiment = True
    refresh
    return experiment_radio, experiment_radio2, got_experiment, subdir


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


@app.cell
def _(mo):
    mo.md(r"""
    ###Second experiment:
    """)
    return


@app.cell
def _(experiment_radio2, mo):
    mo.output.append(experiment_radio2)
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


@app.cell
def _(disp2, mo):
    mo.ui.table(disp2.ed.popd)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Plot of population data:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    y max first
    """)
    return


@app.cell
def _(mo):
    ymax = mo.ui.number()
    ymax1 = mo.ui.number()
    ymax
    return ymax, ymax1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    y max second
    """)
    return


@app.cell
def _(ymax1):
    ymax1
    return


@app.cell
def _(fig):
    fig
    return


@app.cell
def _(fig2):
    fig2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase portrait:
    """)
    return


@app.cell
def _(phase_portrait):
    phase_portrait
    return


@app.cell
def _(phase_portrait2):
    phase_portrait2
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Choose the type of time stamp specificier:
    """)
    return


@app.cell
def _(mo):
    ts_choice = mo.ui.radio(options=["drag and drop","specify number"], inline=True, value="drag and drop")
    ts_choice2 = mo.ui.radio(options=["drag and drop","specify number"], inline=True, value="drag and drop")
    ts_choice
    return ts_choice, ts_choice2


@app.cell
def _(timestamp_specifier):
    timestamp_specifier
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###Second specifier:
    """)
    return


@app.cell
def _(ts_choice2):
    ts_choice2
    return


@app.cell
def _(timestamp_specifier2):
    timestamp_specifier2
    return


@app.cell
def _(img):
    img
    return


@app.cell
def _(img2):
    img2
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
def _(disp2, mo):
    mo.output.append(disp2.ed.paramd)
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
def _(disp2, mo):
    text2 = disp2.ad.notesd
    text_area2 = mo.ui.text_area(text2)
    mo.output.append(text_area2)
    return (text_area2,)


@app.cell
def _(mo, submit_notes_button2):
    mo.output.append(submit_notes_button2)
    return


@app.cell
def _(disp, mo, text_area):
    def submit_notes(event):
        text = text_area.value
        disp.fd.FAD.write_notes(text)
        mo.output.append('Submitted!')

    submit_notes_button = mo.ui.button(label = 'Save', on_click = submit_notes)
    return (submit_notes_button,)


@app.cell
def _(disp2, mo, text_area2):
    def submit_notes2(event):
        text2 = text_area2.value
        disp2.fd.FAD.write_notes(text2)
        mo.output.append('Submitted!')

    submit_notes_button2 = mo.ui.button(label = 'Save', on_click = submit_notes2)
    return (submit_notes_button2,)


if __name__ == "__main__":
    app.run()
