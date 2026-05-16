import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt

    from Analyser import Analyser
    from FileHelper import FileHelper
    from EnAData import FiledEnAData
    from DisplayAnalysis import DisplayAnalysis
    from DisplayTogether import DisplayTogether, save_together_plot

    return (
        DisplayAnalysis,
        DisplayTogether,
        FileHelper,
        FiledEnAData,
        mo,
        save_together_plot,
    )


@app.cell
def _(mo):
    refresh = mo.ui.refresh()
    return (refresh,)


@app.cell
def _(FileHelper, mo, refresh):
    refresh. value

    dh = FileHelper()

    if 'output' in dh. dfos:
        look_in = mo.ui.radio(dh.dfos, value = 'output')

    else:
        look_in = mo.ui.radio(dh.dfos)
    return dh, look_in


@app.cell
def _(
    DisplayAnalysis,
    DisplayTogether,
    FiledEnAData,
    experiment_radio,
    experiment_radio2,
    find_files_from_root_button,
    get_from_root,
    got_experiment,
    mo,
    root_name,
    subdir,
):
    if got_experiment == True:
        exp_folder = subdir

        if get_from_root and find_files_from_root_button. value:
            try:
                displayers = DisplayTogether. from_root_name (root_name = root_name, experiment_folder = exp_folder, lite = True)

                got_displayers = True
            except ValueError as VE:
                mo.output.append (VE)

                got_displayers = False

        elif get_from_root:
            got_displayers = False

        else:
            exp_name = experiment_radio.value
            exp_name2 = experiment_radio2.value

            FEnAd = FiledEnAData.from_files(data_folder = exp_folder, experiment_name = exp_name, lite = True)
            FEnAd2 = FiledEnAData.from_files(data_folder = exp_folder, experiment_name = exp_name2, lite = True)
            disp = DisplayAnalysis(FEnAd)
            disp2 = DisplayAnalysis(FEnAd2)

            displayers = DisplayTogether (
                list_of_displayers = [disp, disp2],
                name = 'experiments',
            )

            got_displayers = True

    else:
        got_displayers = False
    return displayers, got_displayers


@app.cell
def _(displayers, got_displayers):
    if got_displayers:
        phase_portrait = displayers. displayers [0].plt_phase_portrait()
        phase_portrait2 = displayers. displayers [1].plt_phase_portrait()
    else:
        phase_portrait = phase_portrait2 = 'No phase portrait available'
    return


@app.cell
def _(dh, look_in, mo, refresh):
    if look_in. value:
        subdir = look_in.value
        experiment_list = dh.expl(subdir)
        if len(experiment_list) == 0:
            experiment_radio = "Choose a folder with experiments saved in it. If no folders have experiments saved in them, run an experiment in marimo-run.py."
            experiment_radio2 = ""

            experiments_in_list = False

        else:
            experiment_radio = mo.ui.radio(experiment_list, value = experiment_list[0])
            experiment_radio2 = mo.ui.radio(experiment_list, value = experiment_list[0])

            experiments_in_list = True

        got_experiment_folder = True

    else:
        got_experiment_folder = False

    refresh
    return (
        experiment_radio,
        experiment_radio2,
        experiments_in_list,
        got_experiment_folder,
        subdir,
    )


@app.cell
def _(experiment_radio, experiments_in_list, got_experiment_folder):
    if not got_experiment_folder or not experiments_in_list or not experiment_radio. value:
        got_experiment = False

    else:
        got_experiment = True
    return (got_experiment,)


@app.cell
def _(mo):
    mo.md(r"""
    #Experiment analysis
    ##Choose experiment folder:
    """)
    return


@app.cell
def _(look_in, mo):
    mo.output.append(look_in)
    return


@app.cell
def _(mo):
    get_from_root_checkbox = mo. ui. checkbox (label = 'Get from root name')
    return (get_from_root_checkbox,)


@app.cell
def _(get_from_root_checkbox):
    get_from_root = get_from_root_checkbox. value
    return (get_from_root,)


@app.cell
def _(get_from_root_checkbox, mo):
    mo. output. append (get_from_root_checkbox)
    return


@app.cell
def _(
    experiment_radio,
    experiment_radio2,
    get_from_root,
    got_experiment_folder,
    mo,
):
    if got_experiment_folder:
        if get_from_root:
            root_name_field = mo. ui. text (label = 'Root name')
            mo. output. append (root_name_field)

            find_files_from_root_button = mo. ui. run_button (label = 'Find')

            mo. output. append (find_files_from_root_button)

        else:
            mo.output.append(
            mo.vstack([
                mo.md("###Experiment one:"),
                experiment_radio,
                mo.md('###Experiment two:'),
                experiment_radio2,
            ] ) )
    return find_files_from_root_button, root_name_field


@app.cell
def _(get_from_root, got_experiment_folder, root_name_field):
    if got_experiment_folder and get_from_root:
        root_name = root_name_field.value
    return (root_name,)


@app.cell
def _(got_displayers, mo):
    if got_displayers:
        what_to_plot_dropdown = mo. ui. dropdown(
            options = [
                'rho ests',
                'prey populations',
                'predator populations',
            ],
            label = 'What to plot?',
        )
    return (what_to_plot_dropdown,)


@app.cell
def _(got_displayers, what_to_plot_dropdown):
    if got_displayers:
        what_to_plot = what_to_plot_dropdown. value

    else:
        what_to_plot = None
    return (what_to_plot,)


@app.cell
def _(got_displayers, mo, what_to_plot_dropdown):
    if got_displayers:
        mo. output. append (
            what_to_plot_dropdown
        )
    return


@app.cell
def _(got_displayers, mo, what_to_plot):
    if got_displayers:
        if what_to_plot == 'rho ests':
            specific_options = mo. ui. dictionary ( {
                'add_div_nm_line': mo. ui. checkbox (False),
            })

            default_title = 'Number of Pairs divided by $xy$ Against Time'
            default_ylabel = r'$\rho_{\text{est}}(0, t)$'
            default_save_as = 'rho-ests.pdf'

        elif what_to_plot == 'prey populations':
            specific_options = mo. ui. dictionary ( {
                'set_ymax': mo. ui. checkbox (False),
                'ymax': mo. ui. number ()
            })

            default_title = 'Prey Populations'
            default_ylabel = 'Population'
            default_save_as = 'prey.pdf'

        elif what_to_plot == 'predator populations':
            specific_options = mo. ui. dictionary ( {
                'set_ymax': mo. ui. checkbox (False),
                'ymax': mo. ui. number ()
            })

            default_title = 'Predator Populations'
            default_ylabel = 'Population'
            default_save_as = 'pred.pdf'
    return default_save_as, default_title, default_ylabel, specific_options


@app.cell
def _(
    displayers,
    got_displayers,
    graph_options,
    size_options,
    specific_options,
    what_to_plot,
):
    if got_displayers:
        if what_to_plot == 'rho ests':

            description = r'### Plot of $\rho_{\text{est}}(0,t)$' + f'\n Average is: {displayers. average_rho_est ()}'
            figure = displayers. rho_ests_time_series (**graph_options. value, **specific_options. value)

        elif what_to_plot == 'prey populations':
            description = r'### Plot of Prey Populations'
            figure = displayers. prey_time_series (
                **graph_options. value,
                **specific_options. value,
            )


        elif what_to_plot == 'predator populations':
            description = r'### Plot of Predator Populations'
            figure = displayers. pred_time_series (**graph_options. value, **specific_options. value)

        if what_to_plot:
            figure. set_size_inches (
                w = size_options. value ['width'],
                h = size_options. value ['height'],
            )
    return description, figure


@app.cell
def _(default_title, default_ylabel, mo, specific_options, what_to_plot):
    if what_to_plot:

        graph_options = mo.ui.dictionary({
            'title': mo.ui.text (value = default_title),
            'add_title': mo. ui. checkbox (False),
            'xlabel': mo.ui.text(value = 'Turn ($t$)'),
            'ylabel': mo. ui. text (value = default_ylabel),
            'grid': mo. ui. checkbox (True),
            'add_legend': mo. ui. checkbox (False),
        })

        size_options = mo. ui. dictionary ( {
            'width': mo. ui. number (value = 6.4),
            'height': mo. ui. number (value = 4.8),
        } )

        explanation = 'For a 2-by-2 grid in latex, save as width: 3.2, height: 2.4'

        mo.output.append(
            mo. vstack (
                [
                    graph_options,
                    specific_options,
                    size_options,
                    mo. md (explanation)
                ]
            )
        )
    return graph_options, size_options


@app.cell
def _(description, figure, mo, what_to_plot):
    if what_to_plot:
        mo. output. append (
            mo. vstack ( [
                mo. md (description),
                figure,
            ] )
        )
    return


@app.cell
def _(default_save_as, mo, what_to_plot):
    if what_to_plot:
        save_as_text = mo. ui. text (label = 'Save as:', value = default_save_as)

        save_together_plot_button = mo. ui. run_button (label = 'Save figure')
    return save_as_text, save_together_plot_button


@app.cell
def _(mo, save_as_text, save_together_plot_button, what_to_plot):
    if what_to_plot:
        mo. output. append (save_as_text)
        mo. output. append (save_together_plot_button)
    return


@app.cell
def _(
    figure,
    mo,
    save_as_text,
    save_together_plot,
    save_together_plot_button,
    what_to_plot,
):
    if what_to_plot:
        mo. stop (not save_together_plot_button. value)

        save_together_plot (
            fig = figure,
            save_as = save_as_text. value,
        )

        mo. output. append ('Saved.')
    return


if __name__ == "__main__":
    app.run()
