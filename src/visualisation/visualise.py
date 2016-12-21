'''
Visually compare the number of pairs of dead nodes with shortest path length
ell with the results of a Monte Carlo Simulation in which dead nodes are chosen
at random.

For each ell value generate a histogram for the number of Monte Carlo runs
that produced x pairs of dead nodes with ell.

0. Get input and output filepaths.
    - inputs are results dictionaries (both actual results and Monte Carlo
        results dictionary).
1.
'''
import os

project_root = os.path.join(os.path.dirname(__file__), os.pardir)
