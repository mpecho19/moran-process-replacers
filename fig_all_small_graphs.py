import networkx as nx
from libs.Methods import *
# from libs.Functions import draw_nxgraph
from libs.Numeric import Numeric_Solver
from libs.SaveSystem import SaveSystem
import time


#Used to generate the figure for different values of r
PLOT_NUM = 1
r_values = [0.9, 1.1, 2]
r = r_values[PLOT_NUM]





num = 7


timer_all_graphs = time.time()

ss = SaveSystem(f"fig_all_small_graphs", load=False)
ss.set_description(f"Fix prob for all connected graphs on {num} vertices for r = {r}")
ss.auto_init_lists(True)
graphs = nx.read_graph6(f'graphs/graph{num}c.g6')
ids = list(range(len(graphs)))

if True:

        
    for i, G in enumerate(graphs):
        timer_grah = time.time()
        
        solver = Numeric_Solver(G, r, replacer_select, replacer_select)
        solver.solve()
        ss["ss"].append(solver.get_average_fixation_probability())
        
        
        
        average_nn = solver.get_average_fixation_probability()
        

        
        solver = Numeric_Solver(G, r, standard_select, standard_select)
        solver.solve()
        ss["nn"].append(solver.get_average_fixation_probability())
        
        average_ss = solver.get_average_fixation_probability()
        
        difference = average_ss - average_nn  # Calculate the ratio
        
        
        ss['graph_x'].append(average_ss)
        ss['graph_y'].append(average_nn)
        ss['colors'].append(difference)
        
    ss.save()     

from better_plots.better_plots import set_defaults, use_science, fig, save
use_science("science", "ieee")


f, ax = fig(font=15, aspect=0.8)

max_val = max(max(ss['graph_x']), max(ss['graph_y']))
min_val = min(min(ss['graph_x']), min(ss['graph_y']))
scatter = ax.scatter(ss['graph_x'], ss['graph_y'], cmap='plasma_r', c=ss['colors'], marker='o', s=5)

ax.text(0.97, 0.97, rf'$r={r:.1f}$', transform=ax.transAxes, ha='right', va='top', fontsize=18,
    bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='black', alpha=0.9))

ax.set_xlabel(r'Fixation probability in $\mathcal{M}$, $\rho_r^{\mathcal{M}}(G_7)$')
ax.set_ylabel(r'Fixation probability in $\mathcal{R}$, $\rho_r^{\mathcal{R}}(G_7)$')
f.colorbar(scatter, ax=ax ) #label=r'Difference of $\mathcal{M}$ and $\mathcal{R}$'

save(f, f"fig_all_small_graphs.pdf")
    
 