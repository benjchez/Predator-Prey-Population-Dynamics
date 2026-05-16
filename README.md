# Modelling Predator-Prey Population Dynamics

This repository contains Python files that simulate the population dynamics of predators and prey using an individual-based model.

## Use

We provide three Marimo notebooks that allow us to conduct experiments, visualise the output of these, and compare different results.

### Initial Setup

This repository uses `uv` to manage the Python enviroment. Instructions to install `uv` can be found here: [UV Installation](https://docs.astral.sh/uv/getting-started/installation/).

Once `uv` has been installed, please run `uv sync` in the command line to sync the python environment. This makes sure that the correct Python packages are installed to run the code.

### Using the Notebooks

Once we have synced the enviroment, we can open our three notebooks by running these commands in the command line:
- `uv run marimo run IBM/marimo-run.py` - Opens a notebook for running an experiment using the individual-based model.
- `uv run marimo run IBM/marimo-visualise.py` - Opens a notebook for visualising the results of an experiment.
- `uv run marimo run IBM/marimo-compare.py` - Opens a notebook for comparing results from multiple experiments.

To conduct an experiment, please open the first notebook, choose some parameters and press **run**. Once the results have been computed, it will say **Experiment Finished** at the bottom of the notebook. We can then view the results in the second notebook. In the second notebook, choose the folder and name that the experiment is saved under. We will then be shown different figures and pieces of information about the experiment we ran.

After, We can go back to the run notebook and try different parameters to see their output.

The comparison notebook can be used for comparing two runs together or multiple runs if we tick the run-multiple tick box in the run notebook.

### Exploring the Code

The code for the IBM can be found in the `IBM/` directory.
