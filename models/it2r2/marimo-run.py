import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np

    from AnimalParameters import AnimalParameters
    from GraphOptions import GraphOptions
    from Experimenter import Experimenter
    from Analyser import Analyser
    from ExperimentOptions import ExperimentOptions
    from EnAData import EnAData
    return (
        Analyser,
        AnimalParameters,
        EnAData,
        ExperimentOptions,
        Experimenter,
        GraphOptions,
        mo,
    )


@app.cell
def _(mo):
    params = mo.ui.dictionary({
        'a': mo.ui.number(value = 0.5, step = 0.01, stop = 1),
        'b': mo.ui.number(value = 0.1, step = 0.01, stop = 1),
        'c': mo.ui.number(value = 0.05, step = 0.01, stop = 1),
        'd': mo.ui.number(value = 0.02, step = 0.01, stop = 1)
    })
    ops = mo.ui.dictionary({
        'col_num': mo.ui.number(value = 20),
        'row_num': mo.ui.number(value = 20),
        'init_num_prey': mo.ui.number(value = 50),
        'init_num_pred': mo.ui.number(value = 30)
    })
    exops = mo.ui.dictionary({
        'experiment_name': mo.ui.text(value = "test"),
        'num_turns': mo.ui.number(value = 100)
    })
    return exops, ops, params


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Run experiment
    ##Choose animal parameters a,b,c,d, set graph and experiment options and then press run.

    a is the probability that if a prey gets paired with a predator, it will die.

    b is the probability that if a predator gets paired with a prey, it will reproduce.

    c is the probability that a prey will reproduce.

    d is the probability of death for a predator.
    """)
    return


@app.cell
def _(exops, mo, ops, params, run_btn):
    mo.output.append([params, ops, exops, run_btn])
    return


@app.cell
def _(
    Analyser,
    AnimalParameters,
    EnAData,
    ExperimentOptions,
    Experimenter,
    GraphOptions,
    exops,
    mo,
    ops,
    params,
):
    def on_run(_):
        mo.output.append('--- Experiment started ---')
        ps = AnimalParameters(**params.value)
        os = GraphOptions(**ops.value)
        exos = ExperimentOptions(**exops.value)
    
        e = Experimenter(os, ps, exos)
        exp_data = e.run_experiment()

        an = Analyser(exp_data)
        an_data = an.analyse()

        EnAd = EnAData(ed = exp_data, ad = an_data)

        FEnAd = EnAd.to_files(
            experiment_name = exops.value['experiment_name']
        )

        mo.output.append('--- Experiment finished ---')

    run_btn = mo.ui.button(label="Run", on_click = on_run)
    return (run_btn,)


if __name__ == "__main__":
    app.run()
