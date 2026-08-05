import networkx as nx
from libs.Methods import *
from libs.SaveSystem import SaveSystem
import numpy as np
import libs.Simulation as Sim
import itertools



LOAD = True


def baseline(N, r):
    if r == 1:
        return 1 / N
    else:
        return (1 - 1 / r) / (1 - 1 / r ** N)
    
def complete_graph_fix_ss(N, r):
    numerator = 1
    denominator = (1+1/r)**(N-1)
    return numerator / denominator

def cycle_graph_fix_ss(N, r):
    if r != 1:
        numerator = 1-1/r
        denominator= 1 + 1/r -1/r**(N-1) -  1/r**N
    if r==1:
        numerator = 1
        denominator = 2*N-2
    return numerator / denominator

def create_clique_cycle_graph(D, k):
    """
    Generates a D-regular graph made of k complete graphs (cliques) of size D+1,
    arranged in a macro-cycle.
    
    Args:
        D (int): The degree of the resulting regular graph (requires D >= 2).
        k (int): The number of complete graphs to connect in a cycle (requires k >= 1).
        
    Returns:
        nx.Graph: A D-regular NetworkX graph.
    """
    if D < 2:
        raise ValueError("D must be at least 2 to form meaningful complete graphs with removed edges.")
    if k < 1:
        raise ValueError("k must be at least 1.")

    G = nx.Graph()
    
    # Store the 'u' and 'v' nodes for each component to bridge them later
    u_nodes = []
    v_nodes = []
    
    for i in range(k):
        # Generate node labels for the i-th complete graph
        # e.g., for D=3, component 0 gets nodes 0,1,2,3; component 1 gets 4,5,6,7
        start_node = i * (D + 1)
        nodes = list(range(start_node, start_node + D + 1))
        
        # Create a complete graph for these nodes
        G.add_nodes_from(nodes)
        G.add_edges_from(itertools.combinations(nodes, 2))
        
        # Select two nodes to remove the edge between
        u = nodes[0]
        v = nodes[1]
        
        # Remove the internal edge to drop their degrees to D - 1
        G.remove_edge(u, v)
        
        # Save them to connect to neighboring components
        u_nodes.append(u)
        v_nodes.append(v)
        
    # Connect the k components in a macro-cycle
    for i in range(k):
        # Connect v from the current component to u of the next component
        current_v = v_nodes[i]
        next_u = u_nodes[(i + 1) % k]  # Modulo k wraps the last component back to the first
        
        G.add_edge(current_v, next_u)
        
    return G


n_sqrt = 10



ss = SaveSystem(f"fig_large_graphs", load=LOAD)

delta = 0.1
r_range = np.concatenate(([0 + 0.001], np.arange(delta, 5 + delta, delta)))
num_simulations = 1000000

if not LOAD:

    ss.auto_init_lists(True)
    regular_graphs = []
    while len(regular_graphs) < 5:
        print(f"Generating random 4-regular graph {len(regular_graphs)+1}/5")
        random_regular_graph = nx.random_regular_graph(d=4, n=n_sqrt**2)
        if nx.is_connected(random_regular_graph):
            regular_graphs.append(random_regular_graph)

    idx_of_min = 0
    min_fix_prob = float('inf')
    for i, Graph_reg in enumerate(regular_graphs):
        r = 2
        Simulation = Sim.Simulation(Graph_reg, r, replacer_select, replacer_select)
        Simulation.start_simulation(number=num_simulations)

        fix_prob = Simulation.get_probability()
        print(f"Fixation probability for regular graph {i} is {fix_prob}")
        if fix_prob < min_fix_prob:
            min_fix_prob = fix_prob
            idx_of_min = i
            
    for r in r_range:
        print(f"r = {r}")
        
        G= nx.grid_2d_graph(n_sqrt, n_sqrt,periodic=True)
        G= nx.convert_node_labels_to_integers(G)
         

        Simulation = Sim.Simulation(G, r, replacer_select, replacer_select)
        Simulation.start_simulation(number=num_simulations)

        print(f"Fixation probability for r = {r} is {Simulation.get_probability()}")
        ss['r'].append(r)
        ss['fp_grid'].append(Simulation.get_probability())

        
        ss['fp_complete'].append(complete_graph_fix_ss(n_sqrt**2, r))
        ss['fp_cycle'].append(cycle_graph_fix_ss(n_sqrt**2, r))
        ss['baseline'].append(baseline(n_sqrt**2, r))

        G = regular_graphs[idx_of_min]

 
        Simulation = Sim.Simulation(G, r, replacer_select, replacer_select)
        Simulation.start_simulation(number=num_simulations)
    
        ss[f'fp_random_reg'].append(Simulation.get_probability())

        G = create_clique_cycle_graph(4, n_sqrt**2//5)

        Simulation = Sim.Simulation(G, r, replacer_select, replacer_select)
        Simulation.start_simulation(number=num_simulations)
        ss[f'fp_beams'].append(Simulation.get_probability())


from better_plots.better_plots import set_defaults, use_science, fig, save
use_science("science", "ieee")


f, ax = fig(font=15, aspect=.8)



ax.plot(r_range, ss['baseline'], color='black', label='Baseline',  linewidth=1.5, linestyle='--')
ax.plot(r_range, ss['fp_random_reg'], color='orange', label=r'$E_{100}$', linewidth=1.5)
ax.plot(r_range, ss['fp_cycle'], color='green', label=r'$C_{100}$', linewidth=1.5)
ax.plot(r_range, ss['fp_beams'], color='purple', label=r'$B_{100}$', linewidth=1.5)
ax.plot(r_range, ss['fp_grid'], color='blue', label=r'$Sq_{100}$', linewidth=1.5)

ax.plot(r_range, ss['fp_complete'], color='red', label=r'$K_{100}$', linewidth=1.5)
ax.set_xlabel(r'Reproductive rate, $r$')

ax.set_ylabel('Fixation Probability')
ax.legend()



save(f, "fig_large_graphs.pdf")





        
