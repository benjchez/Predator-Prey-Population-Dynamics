import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt

    from Analyser import Analyser
    from FileHelper import FileHelper, delete_data_folder
    from EnAData import FiledEnAData
    from DisplayAnalysis import DisplayAnalysis

    return DisplayAnalysis, FileHelper, FiledEnAData, delete_data_folder, mo


@app.cell
def _(mo):
    refresh = mo.ui.refresh()
    return (refresh,)


@app.cell
def _(FileHelper, mo, refresh):
    refresh. value # Makes this cell dependent on refresh

    dh = FileHelper()

    if 'output' in dh. dfos:
        look_in = mo.ui.radio(dh.dfos, value = 'output')

    else:
        look_in = mo.ui.radio(dh.dfos)
    return dh, look_in


@app.cell
def _(DisplayAnalysis, FiledEnAData, experiment_radio, got_experiment, subdir):
    if got_experiment == True:
        exp_name = experiment_radio.value
        exp_folder = subdir

        FEnAd = FiledEnAData.from_files(data_folder = exp_folder, experiment_name = exp_name)
        disp = DisplayAnalysis(FEnAd)
    return FEnAd, disp


@app.cell
def _(disp, got_experiment):
    if got_experiment == True:
        pair_plot = disp. plt_pairs ()
    return (pair_plot,)


@app.cell
def _(disp, got_experiment, mo, ts_choice):
    if got_experiment == True:
        num_time_stamps = disp.ad.infod['number of time stamps']

        num_time_steps = num_time_stamps - 1

        if ts_choice.value == "drag and drop":
            timestamp_specifier = mo.ui.slider(start=0, stop = num_time_steps, step=1, full_width=True)
        elif ts_choice.value == "specify number":
            timestamp_specifier = mo.ui.number(value = 0, stop = num_time_steps)
        else:
            raise Exception("No given timestamp specifier")
    return (timestamp_specifier,)


@app.cell
def _(disp, got_experiment):
    # Find out where plots should be saved

    if got_experiment == True:
        plots_folder = disp. get_plots_folder ()
    return


@app.cell
def _(disp, got_experiment, timestamp_specifier):
    if got_experiment == True:
        timestamp = timestamp_specifier.value
        img = disp.pmft(timestamp)
    return img, timestamp


@app.cell
def _(dh, look_in, mo, refresh):
    if look_in.value:
        got_experiment_folder = True

        subdir = look_in.value
        experiment_list = dh.expl(subdir)

        if len(experiment_list) == 0:
            experiment_radio = "Choose a folder with experiments saved in it. If no folders have experiments saved in them, run an experiment in marimo-run.py."
            experiments_in_list = False

        else:
            experiment_radio = mo.ui.radio(experiment_list)
            experiments_in_list = True

        mo. output. append (refresh)

    else:
        got_experiment_folder = False
    return experiment_radio, experiments_in_list, got_experiment_folder, subdir


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
    ###If you want to see the output of a run then it will be in the output folder.
    """)
    return


@app.cell
def _(look_in, mo):
    mo.output.append(look_in)
    return


@app.cell
def _(mo):
    delete_folder_button = mo. ui. run_button (label = 'delete folder')
    return (delete_folder_button,)


@app.cell
def _(delete_folder_button, got_experiment_folder, mo):
    if got_experiment_folder:
        mo.output.append(delete_folder_button)
    return


@app.cell
def _(
    delete_data_folder,
    delete_folder_button,
    got_experiment_folder,
    look_in,
    mo,
):
    if got_experiment_folder and delete_folder_button. value:
        delete_data_folder (data_folder = look_in. value)
        mo. output. append ('Deleted. Please refresh.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Experiment:
    """)
    return


@app.cell
def _(experiment_radio, got_experiment_folder, mo):
    if got_experiment_folder:
        mo.output.append(experiment_radio)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Refresh lists:
    """)
    return


@app.cell
def _(mo, refresh):
    mo. output. append (refresh)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _(FEnAd, got_experiment, mo):
    if got_experiment == True:

        move_options = mo.ui.dictionary({
            'new_name': mo.ui.text (value = ''),
            'move_to_folder': mo.ui.text(value = ''),
        })

        def move_exp (event):
            mo. output. append (mo. md ('Moving...') )
            FEnAd. move (**move_options.value)
            mo. output. replace ( mo. md ('Moved. Please refresh.') )

        move_button = mo. ui. button (label = 'Move Experiment', on_click = move_exp)
    return move_button, move_options


@app.cell
def _(got_experiment, mo, move_button, move_options):
    if got_experiment:
        mo. output. append (mo. md ('### Move Experiment') )
        mo.output.append([move_options, move_button])
    return


@app.cell
def _(FEnAd, got_experiment, mo):
    if got_experiment == True:

        def delete_exp (event):
            FEnAd. delete ()
            mo. output. append ('Deleted. Please refresh.')

        delete_button = mo. ui. button (label = 'Delete Experiment', on_click = delete_exp)
    return (delete_button,)


@app.cell
def _(delete_button, got_experiment, mo):
    if got_experiment:
        mo. output. append (mo. md ('### Delete Experiment') )
        mo.output.append (delete_button)
    return


@app.cell
def _(disp, got_experiment, mo):
    if got_experiment:
        mo. output. append (mo. md ("""##Experiment data:
    ###It shows population count of prey and predators per turn.""") )
        mo. output. append (mo.ui.table(disp.ed.popd) )
    return


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        add_title_checkbox = mo. ui. checkbox (label = 'Add title', value = True)
        plot_prey_checkbox = mo. ui. checkbox (label = 'Plot prey', value = True)
        plot_predators_checkbox = mo. ui. checkbox (label = 'Plot predators', value = True)
        plot_twax_checkbox = mo. ui. checkbox (label = 'Plot on twin axes', value = False)

        mo. output. append (mo. md ('##Plot of population data:') )
    
        mo. output. append (
            mo. vstack ( [
                add_title_checkbox,
                plot_prey_checkbox,
                plot_predators_checkbox,
            ] )
        )
    return (
        add_title_checkbox,
        plot_predators_checkbox,
        plot_prey_checkbox,
        plot_twax_checkbox,
    )


@app.cell
def _(
    add_title_checkbox,
    got_experiment,
    mo,
    plot_predators_checkbox,
    plot_prey_checkbox,
    plot_twax_checkbox,
):
    if got_experiment:
        add_title = add_title_checkbox. value
        plot_prey = plot_prey_checkbox. value
        plot_predators = plot_predators_checkbox. value
        plot_twax = plot_twax_checkbox. value    

        if plot_prey and plot_predators:

            mo. output. append (plot_twax_checkbox)
    return add_title, plot_predators, plot_prey, plot_twax


@app.cell
def _(
    add_title,
    disp,
    got_experiment,
    mo,
    plot_predators,
    plot_prey,
    plot_twax,
):
    if got_experiment:

        fig = disp.plt_popd(
            plot_prey = plot_prey,
            plot_predators = plot_predators,
            twin_axes = plot_twax,
            add_title = add_title,
        )
        mo. output. append (fig)
    return (fig,)


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        save_as_ts = mo. ui. text (label = 'Save as:', value = 'time-series.pdf')
        save_ts_plot_button = mo. ui. run_button (label = 'Save figure')
    return save_as_ts, save_ts_plot_button


@app.cell
def _(disp, fig, got_experiment, mo, save_as_ts, save_ts_plot_button):
    if got_experiment:
        mo. stop (not save_ts_plot_button. value)

        disp. save_plot (
            fig = fig,
            save_as = save_as_ts. value,
        )

        mo. output. append ('Saved.')
    return


@app.cell
def _(got_experiment, mo, save_as_ts, save_ts_plot_button):
    if got_experiment:
        mo. output. append (save_as_ts)
        mo. output. append (save_ts_plot_button)
    return


@app.cell
def _(got_experiment, mo, pair_plot):
    if got_experiment:
        mo. output. append (mo. md ('##Plot of predator-prey pairs against time:') )
        mo. output. append (pair_plot)
    return


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        pairs_div_xy_label_options = mo.ui.dictionary({
            'title': mo.ui.text (value = 'Number of Pairs divided by $xy$ Against Time'),
            'add_title': mo. ui. checkbox (True),
            'xlabel': mo.ui.text(value = 'Turn ($t$)'),
            'ylabel': mo. ui. text (value = '$\\rho_{\\text{sim}}(t)$'),
            'grid': mo. ui. checkbox (True),
            'add_div_nm_line': mo. ui. checkbox (False),
            'scatter_plot': mo. ui. checkbox (False),
        })
        size_options = mo. ui. dictionary ( {
            'width': mo. ui. number (value = 6.4),
            'height': mo. ui. number (value = 4.8),
        } )

        mo. output. append (mo. md (r"""##Plot of number of pairs divided by xy against time:

    In the report this is the value $\rho_{\text{sim}}$.

    - The plot gets saved in the same size as you set using width and height.
        - For a 2-by-2 grid in latex, save as width: 3.2, height: 2.4 ."""))
        mo.output.append(pairs_div_xy_label_options)
        mo. output. append (size_options)
    return pairs_div_xy_label_options, size_options


@app.cell
def _(disp, got_experiment, mo, pairs_div_xy_label_options, size_options):
    if got_experiment:
        pairs_div_xy_plot = disp.plt_pairs_div_xy(**pairs_div_xy_label_options.value)

        pairs_div_xy_plot. set_size_inches (
            w = size_options. value ['width'],
            h = size_options. value ['height'],
        )

        mo.output.append(pairs_div_xy_plot)
    return (pairs_div_xy_plot,)


@app.cell
def _(disp, got_experiment, mo, pairs_div_xy_plot):
    if got_experiment:
        save_as_text = mo. ui. text (label = 'Save as:', value = 'rho-sim-plot.pdf')

        def save_pair_plot_div_xy (event):

            disp. save_plot (
                fig = pairs_div_xy_plot,
                save_as = save_as_text. value,
            )

            mo. output. append ('Saved.')

        save_pair_plot_button = mo. ui. button (label = 'Save figure', on_click = save_pair_plot_div_xy)
    return save_as_text, save_pair_plot_button


@app.cell
def _(got_experiment, mo, save_as_text, save_pair_plot_button):
    if got_experiment:
        mo. output. append (save_as_text)
        mo. output. append (save_pair_plot_button)
    return


@app.cell
def _(disp, got_experiment, mo):
    if got_experiment:
        mo. output. append (mo. md ('The total pairs is:'))
        mo. output. append (int (disp. total_pairs () ) )
    return


@app.cell
def _(disp, got_experiment, mo):
    if got_experiment:
        mo. output. append (mo. md ('The total pairs divided by the sum of x*y for all time is:') )
        mo. output. append (float (disp.total_pairs() / disp.sum_of_xy_over_all_time() ) )
    return


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        rho_est_options = mo.ui.dictionary({
            'title': mo.ui.text (value = r'$\rho_{\text{est}}(0, t)$ over Time'),
            'add_title': mo. ui. checkbox (True),
            'xlabel': mo.ui.text(value = 'Turn ($t$)'),
            'ylabel': mo. ui. text (value = r'$\rho_{\text{est}}(0, t)$'),
            'grid': mo. ui. checkbox (True),
            'add_div_nm_line': mo. ui. checkbox (False),
        })
        save_rho_est_options = mo. ui. dictionary ( {
            'width': mo. ui. number (value = 6.4),
            'height': mo. ui. number (value = 4.8),
        } )

        mo. output. append (mo. md (r'We use $\rho_{\text{est}}$ defined in the report'))
        mo.output.append(rho_est_options)
        mo. output. append (save_rho_est_options)
    return rho_est_options, save_rho_est_options


@app.cell
def _(disp, got_experiment, mo, rho_est_options, save_rho_est_options):
    if got_experiment:
        rho_est_fig = disp. plt_rho_ests (
            ** rho_est_options. value,
            ** save_rho_est_options. value,
        )
        mo. output. append (rho_est_fig)
    return (rho_est_fig,)


@app.cell
def _(
    disp,
    got_experiment,
    mo,
    rho_est_fig,
    save_as_rho_ests,
    save_rho_ests_button,
):
    if got_experiment:
        mo. stop (not save_rho_ests_button. value)

        disp. save_plot (
            fig = rho_est_fig,
            save_as = save_as_rho_ests. value,
        )

        mo. output. append ('Saved.')
    return


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        save_as_rho_ests = mo. ui. text (label = 'Save as:', value = 'rho-ests.pdf')
        save_rho_ests_button = mo. ui. run_button (label = 'Save figure')
    return save_as_rho_ests, save_rho_ests_button


@app.cell
def _(got_experiment, mo, save_as_rho_ests, save_rho_ests_button):
    if got_experiment:
        mo. output. append (save_as_rho_ests)
        mo. output. append (save_rho_ests_button)
    return


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        phase_portrait_options = mo.ui.dictionary({
            'add_title': mo. ui. checkbox (True),
            'scatter_plot': mo. ui. checkbox (True),
            'xlabel': mo. ui. text (value = 'Number of prey'),
            'ylabel': mo. ui. text (value = 'Number of predators'),
        })
        phase_portrait_size = mo. ui. dictionary ( {
            'width': mo. ui. number (value = 6.4),
            'height': mo. ui. number (value = 4.8),
        } )

        mo. output. append (mo. md ('## Phase portrait:') )
        mo. output. append (phase_portrait_options)
        mo. output. append (phase_portrait_size)
    return phase_portrait_options, phase_portrait_size


@app.cell
def _(disp, got_experiment, phase_portrait_options, phase_portrait_size):
    if got_experiment == True:
        phase_portrait = disp.plt_phase_portrait(
            ** phase_portrait_options. value,
            ** phase_portrait_size. value
        )
    return (phase_portrait,)


@app.cell
def _(got_experiment, mo, phase_portrait):
    if got_experiment:
        mo. output. append (phase_portrait)
    return


@app.cell
def _(
    disp,
    got_experiment,
    mo,
    phase_portrait,
    save_as_phase_portrait,
    save_phase_portrait_button,
):
    if got_experiment:
        mo. stop (not save_phase_portrait_button. value)

        disp. save_plot (
            fig = phase_portrait,
            save_as = save_as_phase_portrait. value,
        )

        mo. output. append ('Saved.')
    return


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        save_as_phase_portrait = mo. ui. text (label = 'Save as:', value = 'phase_portrait.pdf')
        save_phase_portrait_button = mo. ui. run_button (label = 'Save figure')
    return save_as_phase_portrait, save_phase_portrait_button


@app.cell
def _(got_experiment, mo, save_as_phase_portrait, save_phase_portrait_button):
    if got_experiment:
        mo. output. append (save_as_phase_portrait)
        mo. output. append (save_phase_portrait_button)
    return


@app.cell
def _(got_experiment, mo):
    ts_choice = mo.ui.radio(options=["drag and drop","specify number"], inline=True, value="drag and drop")

    if got_experiment:
        mo. output. append (mo. md ("""##Distribution image
    ###An image showing the distribution of predators and prey across the map at a particular timestamp.

    More red in a pixel indicates more predators are at that point in the graph and more blue indicates more prey are at that point in the graph.

    ###Choose time step:

    Choose the type of time stamp specificier:"""))
    
        mo. output. append (ts_choice)
    return (ts_choice,)


@app.cell
def _(got_experiment, mo, timestamp_specifier):
    if got_experiment:
        mo. output. append (timestamp_specifier)
    return


@app.cell
def _(got_experiment, img, mo):
    if got_experiment:
        mo.output. append (img)
    return


@app.cell
def _(got_experiment, mo, save_pmft_button):
    if got_experiment:
        mo. output. append (save_pmft_button)
    return


@app.cell
def _(disp, mo, timestamp):
    def save_pmft (event):
        disp. save_pmft (ts = timestamp)
        mo. output. append ('Saved.')

    save_pmft_button = mo. ui. button (label = 'Save pmft as a file', on_click = save_pmft)
    return (save_pmft_button,)


@app.cell
def _(got_experiment, mo):
    if got_experiment:
        make_heatmap_checkbox = mo. ui. checkbox (label = 'make heat map')
        mo. output. append (mo. md ('###Heat map'))
        mo. output. append (make_heatmap_checkbox)
    return (make_heatmap_checkbox,)


@app.cell
def _(disp, got_experiment, make_heatmap_checkbox, mo):
    if got_experiment and make_heatmap_checkbox. value:
        mo.output. append ('making...')
        mo.output.replace(disp. heat_map ())

    else:
        mo.output. clear ()
    return


@app.cell
def _(disp, got_experiment, mo):
    if got_experiment:
        mo. output. append (mo. md ('##Parameters'))
        mo.output.append(disp.ed.paramd)
    return


@app.cell
def _(disp, got_experiment, mo):
    if got_experiment:
        text = disp.ad.notesd
        text_area = mo.ui.text_area(text)

        mo. output. append (mo. md ('##Notes') )
        mo.output.append(text_area)

    return (text_area,)


@app.cell
def _(got_experiment, mo, submit_notes_button):
    if got_experiment:
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


@app.cell
def _(got_experiment, mo, save_plots_button):
    if got_experiment:
        mo. output. append (mo. md ('## Save plots as files') )
        mo. output. append (save_plots_button)
    return


@app.cell
def _(disp, mo):
    def save_plots (event):
        mo. output. append ('Saving...')
        disp. save_all_plots ()
        mo. output. replace (mo. md ('Saved.') )

    save_plots_button = mo. ui. button (label = 'Save all plots', on_click = save_plots)
    return (save_plots_button,)


if __name__ == "__main__":
    app.run()
