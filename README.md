# moran-process-replacers

This repository contains the source code and scripts used to generate the figures for the paper **"Replacers and their evolutionary stability in the Moran process on graphs"**.

Each Python script in the root directory corresponds to a specific figure in the paper, except for `moran-beads.py`, which is used for computations in Lemma 6 of the Supplementary Information.

Running a script will generate the plot and save it automatically into the `paper_figures/` directory.

Note that `fig_large_graphs.py` uses pre-computed, saved values to generate its plots. To run new simulations and regenerate the plots from scratch, set `LOAD = False` inside the Python script.

The code was originally developed and tested using **Python 3.14.6**.

You can use `pip` to install the necessary dependencies.
