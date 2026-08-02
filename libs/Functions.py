import networkx as nx

def normalise_nxgraph(graph : nx.Graph):
    normalised_graph = nx.Graph()
    mapping = {node: i for i, node in enumerate(sorted(graph.nodes))}
    normalised_graph.add_nodes_from(mapping.values())
    normalised_graph.add_edges_from((mapping[u], mapping[v]) for u, v in graph.edges)
    return normalised_graph
        
def read_graph6_file(filename : str):
    return nx.read_graph6(f'graphs/{filename}.g6')
    