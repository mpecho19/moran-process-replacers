from libs.Graph import Graph
import networkx as nx


def init_method( selected_node : int, nx_graph : nx.Graph = None, colors : list = None, graph : Graph = None):
    if graph is not None: 
        nx_graph = graph.G
        colors = graph.get_colors()
    neighbors = nx_graph.neighbors(selected_node)
    return (selected_node, colors, neighbors)


def standard_select( selected_node : int, colors : list = None, neighbors : list = None):
    nodes = []
    for node in neighbors:
        nodes.append(node)
    if nodes:
        return nodes

def replacer_select( selected_node : int, colors : list = None, neighbors : list = None ):
    
    nodes = []
    for node in neighbors:
        if colors[node] != colors[selected_node]:
            nodes.append(node)
    if nodes:
        return nodes

        
        

        
            