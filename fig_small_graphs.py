import numpy as np
import networkx as nx
from libs.Numeric import Numeric_Solver
from libs.Methods import *
import matplotlib.pyplot as plt

import numba    
from numba import njit, prange




def baseline(N, r):
    if r == 1:
        return 1 / N
    else:
        return (1 - 1 / r) / (1 - 1 / r ** N)

eps = 0.1
r_range = np.concatenate(([0 + 0.001], np.arange(eps, 5.01, eps)))

num_of_vertices = 7


graphs = nx.read_graph6(f'graphs/graph{num_of_vertices}c.g6')





fix_list_min = []
fix_list_max = []
fix_baseline = [baseline(num_of_vertices, r) for r in r_range]

fix_complete = []
fix_path = []
fix_star = []
fix_cycle = []

for r in r_range:
    fix_list = []
    print(f"r = {r}")

    graph = nx.complete_graph(num_of_vertices)
    solver = Numeric_Solver(graph, r, replacer_select, replacer_select)
    solver.solve()
    fix_complete.append(solver.get_average_fixation_probability())
    current_complete = solver.get_average_fixation_probability()
    graph = nx.path_graph(num_of_vertices)
    solver = Numeric_Solver(graph, r, replacer_select, replacer_select)
    solver.solve()
    fix_path.append(solver.get_average_fixation_probability())

    graph = nx.star_graph(num_of_vertices-1)
    solver = Numeric_Solver(graph, r, replacer_select, replacer_select)
    solver.solve()

    fix_star.append(solver.get_average_fixation_probability())


    graph = nx.cycle_graph(num_of_vertices)
    solver = Numeric_Solver(graph, r, replacer_select, replacer_select)
    solver.solve()
    fix_cycle.append(solver.get_average_fixation_probability())

    for i, G in enumerate(graphs):
        solver = Numeric_Solver(G, r, replacer_select, replacer_select)
        solver.solve()
        fix_list.append(solver.get_average_fixation_probability())

    fix_list_min.append(min(fix_list))
    fix_list_max.append(max(fix_list))

from better_plots.better_plots import set_defaults, use_science, fig, save
use_science("science", "ieee")


f, ax = fig(font=15, aspect=.8)

ax.plot(r_range, fix_baseline, color='black', label='Baseline',  linewidth=1.5, linestyle='--')
ax.plot(r_range, fix_path, color='blue', label=r'$P_7$', linewidth=1.5)
ax.plot(r_range, fix_cycle, color='green', label=r'$C_7$', linewidth=1.5)
ax.plot(r_range, fix_star, color='orange', label=r'$S_7$', linewidth=1.5)
ax.plot(r_range, fix_complete, color='red', label=r'$K_7$', linewidth=1.5)
ax.fill_between(r_range, fix_list_min, fix_list_max, color='lightgray', alpha=0.5, label='Range')
ax.set_xlabel(r'Reproductive rate, $r$')

ax.set_ylabel('Fixation Probability')
ax.legend()



save(f, "fig_small_graphs.pdf")



