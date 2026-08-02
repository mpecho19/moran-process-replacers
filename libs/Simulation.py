
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
import timeit
from libs.Graph import Graph
import random
from libs.Functions import normalise_nxgraph
import libs.Methods as Methods
BLUE = 1

    

class Simulation:

    
    def __init__(self, nxGraph : nx.Graph,
                 fitness : float = 1 ,
                 select_method = Methods.standard_select,
                 res_select_method = Methods.replacer_select) -> None:



        self.nxGraph = normalise_nxgraph(nxGraph)
        
            
        self.select_method = select_method    
        self.res_select_method = res_select_method if res_select_method else select_method
        
        
        self.fitness = fitness
        
        self.graph = Graph(nxGraph, [], fitness)

        
        self.blue_wins = 0 
        self.total_games = 0
        self.number_of_steps = 0
        self.number_of_active_steps = 0 
        self.average_steps = 0
        
    def __number_of_nodes(self):
        return self.nxGraph.number_of_nodes()
    
    def start_simulation(self, number = 10000):
        self.step_numbers = []

        for i in range(number):
            current_graph = Graph(copy=self.graph)

            random_node = random.randint(0, self.graph.G.number_of_nodes() - 1)
            current_graph.change_color_to(random_node, 'blue')
            number_of_steps = 0
            while current_graph.get_number_of_color('blue') > 0 and current_graph.get_number_of_color('red') > 0:
                # print(current_graph.get_number_of_color('blue'))
                current_graph.select_primary(current_graph.get_random_node())
                number_of_steps += 1
                nodeSecond = None
                
                if (current_graph.get_colors(current_graph.get_primary()) == 'blue') :
                    select_list = self.select_method(*Methods.init_method(current_graph.get_primary(), graph=current_graph))
                    # print(f"Select list for node {current_graph.get_primary()} is {select_list}")
                    if(select_list is None):
                        continue
                    nodeSecond = random.choice(select_list)
                elif current_graph.get_colors(current_graph.get_primary()) == 'red':
                    select_list =self.res_select_method(*Methods.init_method(current_graph.get_primary(), graph=current_graph))
                    if select_list is None:
                        continue
                    nodeSecond = random.choice(select_list)
                else:
                    raise ValueError("Selected node has an unexpected color.")
                
                if nodeSecond is None:

                    continue

                current_graph.select_secondary(nodeSecond)
                current_graph.change_color_of_selection()
                current_graph.clear_selection()

            if current_graph.get_number_of_color('red') == 0:
                self.blue_wins += 1
            self.total_games += 1 
            self.step_numbers.append(number_of_steps)

        
    def get_probability(self):
        if self.total_games > 0:
            return self.blue_wins/self.total_games
    
    def get_blue_wins(self):
        return self.blue_wins
    
    def get_average_steps(self):
        average = sum(self.step_numbers) / len(self.step_numbers) 
        return average
    