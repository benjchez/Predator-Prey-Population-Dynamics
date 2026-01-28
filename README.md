# MATH30000-Double-Project

## Info
Using uv for dependency control.

## Use

The best way to use this system is to experiment and analyse the output using the three marimo notebooks.


First make sure uv is installed.

Then run `uv sync` to sync the python environment. (This is so that all the right versions of packages are installed and python has configured the paths to the packages correctly.)

To open marimo notebooks, run `uv run marimo edit`.

Once you have opened this, scrolling down to workspace, you will find the three notebooks under models/it4 (ignore notebooks under 'shed' as they pertain to earlier models).

The notebook 'marimo-run.py' is an interface to run an experiment. Choose the parameters you want for the experiment and click run.

The notebook 'marimo-visualise.py' shows the analysis of past experiments. You should be able to find experiments that you have run if you press on 'output' on the list of folder options. You will see a list of different experiments, choose the one that matches the name that you entered in marimo-run.py (default is 'test').

The notebook 'marimo-compare.py' allows you to compare two different tests.

It is much easier to view the notebooks in app view (there's a button near bottom right or you can do `ctrl + .`).

If you have 'marimo-visualise.py' open when you run a test in 'marimo-run.py', use the reload button in the visualise notebook in the top left and you will be able to see the new experiment.

## Other use
To activate the virtual environment, run:
source .venv/bin/activate (linux)
.venv\Scripts\activate (windows).

Run deactivate to deactivate the environment

## Trustworthiness of results
Results from models before it2r2 cannot be trusted as there was a bug where initial predator count was set to equal the initial prey count.

## TODO and ideas
Stop adding the historical grids all to one variable and instead write the them to file every so often to massively reduce the space complexity.

