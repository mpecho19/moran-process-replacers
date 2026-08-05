import numpy as np
import matplotlib.pyplot as plt
import math

def complete_graph_fix_ss(N, r, i=1):

    sum = 0     
    for i in range(1, i):
        sum += math.factorial(N-1) / (math.factorial(i) * math.factorial(N-1-i)) * (1/r)**i
    numerator = 1 + sum
    denominator = (1+1/r)**(N-1)
    return numerator / denominator

def oblivious_complete_fix(N,r,i=1):
    if r == 1:
        return i/N
    
    numerator = 1 - (1/r)**i
    denominator = 1 - (1/r)**N
    return numerator / denominator


from better_plots.better_plots import set_defaults, use_science, fig, save
use_science("science", "ieee")

eps = 0.1
r_range = np.concatenate(([0 + 0.001], np.arange(eps, 5.01, eps)))

initial_mutants = [1,2,5,10]

plots = [[] for _ in range(len(initial_mutants))]
obl_plot = []
N = 10
for r in r_range:
    for i, initial in enumerate(initial_mutants):
        plots[i].append(complete_graph_fix_ss(N, r, initial))

    obl_plot.append(oblivious_complete_fix(N, r, 1))
        
f, ax = fig(font=15, aspect=.7)

import matplotlib.pyplot as plt


ax.plot(r_range, obl_plot, label="Baseline", color="black", linestyle="--")

ax.plot(r_range, plots[0], label=f"$i={initial_mutants[0]}$", color="red")
ax.plot(r_range, plots[1], label=f"$i={initial_mutants[1]}$", color="orange")
ax.plot(r_range, plots[2], label=f"$i={initial_mutants[2]}$", color="green")
ax.plot(r_range, plots[3], label=f"$i={initial_mutants[3]}$", color="blue")

ax.text(0.0298, 0.5125, rf'$N={N}$', transform=ax.transAxes, ha='left', va='top', fontsize=18,
    bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='black', alpha=0.9))

# Decreased x from 0.033 to 0.02 to pull the legend box left over the text box padding
plt.legend(loc="upper left", bbox_to_anchor=(0.0175, 0.9825), borderaxespad=0)

ax.set_xlabel(r'Reproductive rate, $r$')
ax.set_ylabel(r'Fixation probability')
# plt.legend(loc="lower right", bbox_to_anchor=(0.925, 0.05))


save(f, f"fig_complete_r_initial_{N}.pdf") 