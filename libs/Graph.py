from libs.Storage import *
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy

class Graph: 
    selected = [None, None]
    outlines = []
    storage : Storage
    
    G : nx.Graph
    def __init__(self, nxGraph = None, blueStart : list = [0], coefficient = 1, copy : 'Graph' = None):

        if copy is None:
            self.G = nxGraph
            self.coefficient = coefficient
            self.nodes = self.G.nodes()
            self.storage = Storage(redList=self.nodes, nodes=self.nodes)
            
            self.outlines = ['black']*len(self.G.nodes)
            for node in blueStart:
                self.storage.change_color_to(node, 'blue')
        else:
            self.G = copy.G
            self.nodes = self.G.nodes
            self.storage = Storage(copy=copy.storage)
            self.outlines = copy.outlines.copy()
            self.selected = [None, None]
            self.coefficient = copy.coefficient
         
    
    

    def get_nxgraph(self):
        return self.G

    def get_number_of_nodes(self):
        return self.G.number_of_nodes()
    
    def set_color(self, node, color):
        self.storage.change_color_to(node, color)

    def select_primary(self, node):
        if self.selected[0] is not None:
            self.outlines[self.selected[0]] = 'black' 
        self.selected[0] = node
        self.outlines[node] = 'pink'
    
    def get_primary(self):
        if self.selected[0] is not None:
            return self.selected[0]
    
    def get_nodes(self):
        return self.nodes
    
    def get_coefficient(self):
        return self.coefficient
    
    def select_secondary(self,node):
        if self.selected[1] is not None:
            self.outlines[self.selected[1]] = 'black' 
        self.selected[1] = node
        self.outlines[node] = 'yellow'

    def clear_selection(self):
        if self.selected[0] is not None:
            self.outlines[self.selected[0]] = 'black'
        if self.selected[1] is not None:
            self.outlines[self.selected[1]] = 'black'
        self.selected= [None, None]

    def get_selected(self, number):
        if number == 0 or number == 1:
            return self.selected[number]
        
    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position
    
    def change_color_to(self, node, color):
        self.storage.change_color_to(node, color)
    
    def get_colors(self, node = None):
        if node == None:
            return self.storage.get_all_colors()
        else: 
            return self.storage.get_color_of_node(node)
    
    def get_outlines(self):
        return self.outlines
    
    def get_neighbors(self, node):
        return self.G.neighbors(node)
    
    def get_degree(self, node):
        return self.G.degree(node)
    
    def get_number_of_color(self, color):
        return self.storage.get_number_of(color)
    


    def get_random_node(self):
        prop = self.get_number_of_color('blue')*self.coefficient/(self.get_number_of_color('blue')*self.coefficient + self.get_number_of_color('red'))

        rand = random.random()
        if(rand < prop):
            
            return self.storage.get_random_of_color('blue')
        else:
            return self.storage.get_random_of_color('red')
        
    def change_color_of_selection(self):
        if self.selected[0] is not None and self.selected[1] is not None:
            self.change_color_to(self.selected[1], self.get_colors(self.selected[0]))