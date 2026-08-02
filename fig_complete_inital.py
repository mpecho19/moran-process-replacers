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

r_values = [0.5,1, 1.5]

plots = [[] for _ in range(len(r_values))]
obl_plots = [[] for _ in range(len(r_values))]
N = 100
for i, r in enumerate(r_values):
  
    for k in range(N+1):
        p = complete_graph_fix_ss(N, r, i=k)
        plots[i].append(p)
    for k in range(N+1):
        p = oblivious_complete_fix(N, r, i=k)
        obl_plots[i].append(p)
f, ax = fig(font=15, aspect=.7)

import matplotlib.pyplot as plt

x_values = np.arange(0, N+1, 1)

vertical_lines = [N/(r+1)  for r in r_values]


ax.plot(x_values, plots[2], label=f"$r={r_values[2]}$", color='green', linewidth=2)
ax.plot(x_values, plots[1], label=f"$r={r_values[1]}$", color='orange', linewidth=2)
ax.plot(x_values, plots[0], label=f"$r={r_values[0]}$", color='blue', linewidth=2)

ax.plot(x_values, obl_plots[2], color='green', linestyle='--', linewidth=2)
ax.plot(x_values, obl_plots[1], color='orange', linestyle='--', linewidth=2)
ax.plot(x_values, obl_plots[0], color='blue', linestyle='--', linewidth=2)

ax.set_xlabel(r'Number of initial mutants, $i$')
ax.set_ylabel(r'Fixation probability')
plt.legend(loc="lower right", bbox_to_anchor=(0.925, 0.05))

save(f, f"fig_complete_initial.pdf") 