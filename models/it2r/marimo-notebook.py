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
    return AnimalParameters, ExperimentOptions, Experimenter, GraphOptions, mo


@app.cell
def _(AnimalParameters, ExperimentOptions, Experimenter, GraphOptions, mo):
    params = mo.ui.dictionary({
        'a': mo.ui.number(value = 0.8, step = 0.01, stop = 1),
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
    def on_run(_):
        print('--- Experiment started ---')
        ps = AnimalParameters(**params.value)
        os = GraphOptions(**ops.value)
        exos = ExperimentOptions(**exops.value)
        e = Experimenter(os, ps, exos)
        e.out_to_files()

        print('--- Experiment finished ---')



    run_btn = mo.ui.button(label="Run", on_click = on_run)

    mo.output.append([params, ops, exops, run_btn])
    return


if __name__ == "__main__":
    app.run()
