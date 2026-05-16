import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from AnimalParameters import AnimalParameters
    from GridOptions import GridOptions
    from Experimenter import Experimenter
    from Analyser import Analyser
    from ExperimentOptions import ExperimentOptions
    from EnAData import EnAData
    from Recipes import run_and_save, run_and_save_multiple_one_at_a_time
    from utils import resolve_seed

    return (
        AnimalParameters,
        ExperimentOptions,
        GridOptions,
        mo,
        resolve_seed,
        run_and_save,
        run_and_save_multiple_one_at_a_time,
    )


@app.cell
def _(mo):
    params = mo. ui. dictionary ( {
        'a': mo. ui. number (value = 0.5, step = 0.000001, stop = 1),
        'b': mo. ui. number (value = 0.1, step = 0.000001, stop = 1),
        'c': mo. ui. number (value = 0.05, step = 0.000001, stop = 1),
        'd': mo. ui. number (value = 0.02, step = 0.000001, stop = 1),
    })

    ops = mo. ui. dictionary ( {
        'row_num': mo. ui. number (value = 6),
        'col_num': mo. ui. number (value = 6),
        'init_num_prey': mo. ui. number (value = 3),
        'init_num_pred': mo. ui. number (value = 3),
        'movement_at_edge_choice': mo. ui. dropdown (options = {'No Escape': 'ne', 'Random Edge Point': 'rep' }, value = 'No Escape'),
        'predator_reproduction_choice': mo. ui. dropdown (options = {'Independent of prey death': 'ipd', 'Dependent on prey death': 'dpd' }, value = 'Dependent on prey death'),
        'turn_choice': mo. ui. dropdown (
            options = {
                'Default': 'd',
                'Randomise grid after movement': 'r',
            },
            value = 'Default',
        ),
    })

    exops = mo. ui. dictionary ( {
        'data_folder': mo. ui. text (value = 'output'),
        'experiment_name': mo. ui. text (value = 'test'),
        'num_turns': mo. ui. number (value = 10),
    } )

    # mros - multiple run options
    mros = mo. ui. dictionary (
        {
            'number_of_experiments': mo. ui. number (value = 1),
            'same_initial_conditions': mo. ui. checkbox (value = False),
        }
    )
    return exops, mros, ops, params


@app.cell
def _(mo):
    # Seed
    add_seed_checkbox = mo. ui. checkbox (value = False)
    seed_input = mo. ui. number (value = 0)
    return add_seed_checkbox, seed_input


@app.cell
def _(mo):
    run_btn = mo. ui. run_button (label = 'Run')
    clear_btn = mo. ui. run_button (label = 'Clear')
    return clear_btn, run_btn


@app.cell
def _(mo):
    run_multiple_checkbox = mo. ui. checkbox (label = 'Run Multiple')
    return (run_multiple_checkbox,)


@app.cell
def _(run_multiple_checkbox):
    run_multiple = run_multiple_checkbox. value
    return (run_multiple,)


@app.cell
def _(mros, run_multiple):
    if run_multiple:

        run_multiple_form = f"""
    | option  |   value  |
    |---|---|
    | Number of experiments  | {mros['number_of_experiments'] } |
    | Keep starting graph the same? | {mros['same_initial_conditions'] }       |
    """

    else:
        run_multiple_form = ''
    return (run_multiple_form,)


@app.cell
def _(add_seed_checkbox):
    add_seed = add_seed_checkbox. value
    return (add_seed,)


@app.cell
def _(add_seed, add_seed_checkbox, seed_input):
    if add_seed:
        seed_form = f"""
    ## Seed
    | option | value |
    |---|---|
    | Add seed | {add_seed_checkbox} |
    | Seed | {seed_input} |
    """

    else:
        seed_form = f"""
    ## Seed
    | option | value |
    |---|---|
    | Add seed | {add_seed_checkbox} |
    """
    return (seed_form,)


@app.cell
def _(add_seed, seed_input):
    if add_seed:
        seed = seed_input. value

    else:
        seed = None
    return (seed,)


@app.cell
def _(ops):
    # Predator reproduction parameter and description

    if ops ['predator_reproduction_choice']. value == 'dpd':
        pred_rep_par = r'$\frac{{1}}{{\sigma_{{\text{{sim}} }} }}$'
        pred_rep_desc = 'Probability a predator reproduces when it kills a prey'

    else:
        pred_rep_par = r'$\frac {{\delta_ {{\text {{sim}} }} }} {{\rho_ {{\text {{sim}} }} }}$'
        pred_rep_desc = 'Probability a predator reproduces when paired with a prey'
    
    return pred_rep_desc, pred_rep_par


@app.cell
def _(
    exops,
    mo,
    ops,
    params,
    pred_rep_desc,
    pred_rep_par,
    run_btn,
    run_multiple_checkbox,
    run_multiple_form,
    seed_form,
):
    mo.md(rf"""
    # Run experiment

    Predator Reproduction is: {ops ['predator_reproduction_choice'] }

    ## Animal parameters
    | parameter | meaning | value |
    |---|---|---|
    | **$\alpha_{{\text{{sim}} }}$** | Probability a prey reproduces                                                         | {params ['c'] } |
    | **$\gamma_{{\text{{sim}} }}$** | Probability a predator dies                                                           | {params ['d'] } |
    | **$\beta_{{\text{{1sim}} }}$** | Probability a prey dies when paired with a predator                                   | {params ['a'] } |
    | **{pred_rep_par}** | {pred_rep_desc} | {params ['b'] } |

    ## Grid
    | option | value |
    |---|---|
    | width (columns)                  | {ops ['col_num'] }                      |
    | height (rows)                    | {ops ['row_num'] }                      |
    | initial prey                     | {ops ['init_num_prey'] }                |
    | initial predators                | {ops ['init_num_pred'] }                |
    | edge behaviour                   | {ops ['movement_at_edge_choice'] }      |
    | turn type                        | {ops ['turn_choice'] }                  |

    {seed_form}

    ## Experiment
    | option  |   value  |
    |---|---|
    | folder| {exops ['data_folder'] }     |
    | name  | {exops ['experiment_name'] } |
    | turns | {exops ['num_turns'] }       |

    {run_multiple_checkbox}

    {run_multiple_form}

    {run_btn}
    """)
    return


@app.cell
def _(
    AnimalParameters,
    ExperimentOptions,
    GridOptions,
    clear_btn,
    exops,
    mo,
    mros,
    ops,
    params,
    resolve_seed,
    run_and_save,
    run_and_save_multiple_one_at_a_time,
    run_btn,
    run_multiple,
    seed,
):
    mo. stop (not run_btn. value, mo. md ('Press **Run** to start.') )

    mo. stop (clear_btn. value)

    mo. output. append (mo. callout ('Experiment Started', kind = 'info') )

    try:
        ps = AnimalParameters (** params. value)
        os = GridOptions (
            seed = resolve_seed (seed),
            ** ops. value
        )
        exos = ExperimentOptions (** exops. value)

        if not run_multiple:
            run_and_save (
                animal_parameters = ps,
                grid_options = os,
                experiment_options = exos,
            )
        else:
            run_and_save_multiple_one_at_a_time (
                animal_parameters = ps,
                grid_options = os,
                experiment_options = exos,
                ** mros. value
            )

        mo. output. append (mo. callout ('Experiment Finished', kind = 'success') )

    except Exception as ex:
        mo. output. append (mo. callout (f'{type (ex). __name__}: {ex}', kind = 'danger') )

    mo. output. append (clear_btn)
    return


if __name__ == "__main__":
    app.run()
