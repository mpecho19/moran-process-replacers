import networkx as nx
import numpy as np
import scipy.sparse.linalg as spsl
import scipy.sparse as sps

import itertools
import libs.Methods as Methods


BLUE = 1
RED = 0

def binary_list_to_decimal(binary_list):
 
    
    decimal_number = 0
    for bit in binary_list:
        decimal_number = (decimal_number << 1) | bit
    return decimal_number


class Numeric_Solver:
    def __init__(self, nxGraph : nx.Graph, fitness : float = 1, select_method = None, res_select_method = None):
        self.nxGraph = nxGraph
        self.fitness = fitness
        self.select_method = select_method
        self.res_select_method = res_select_method
        self.powers = []
        self.matrix = None
  
        for k in range(self.__number_of_nodes()):
            self.powers.append(2**(self.__number_of_nodes()-1-k))

        self.__init_matrix()
    
    def __number_of_nodes(self):
        return self.nxGraph.number_of_nodes()
    def __get_power(self, exponent):
        return self.powers[exponent]
    
    def __init_matrix(self):
        number_of_states = 2**self.__number_of_nodes()
        self.matrix = sps.lil_matrix((number_of_states,number_of_states))
        for state_vector in itertools.product((0,1),repeat=self.__number_of_nodes()):
            mut=[]
            total_fitness = 0
            state_number = binary_list_to_decimal(state_vector)
            for k in range(self.__number_of_nodes()):
                if state_vector[k]==BLUE:
                    mut.append(self.fitness)
                    total_fitness += self.fitness
                else:
                    mut.append(1)
                    total_fitness += 1
            for node in self.nxGraph.nodes():
                secondary_nodes = None
                if state_vector[node] == BLUE:
                    secondary_nodes =self.select_method(*Methods.init_method(selected_node = node, nx_graph = self.nxGraph, colors = state_vector))
                if state_vector[node] == RED:
                    secondary_nodes =self.res_select_method(*Methods.init_method(selected_node = node, nx_graph = self.nxGraph, colors = state_vector))
                if secondary_nodes is None:
                    continue
                for secondary_node in secondary_nodes:
                    if state_vector[node] != state_vector[secondary_node]:
                        if state_vector[node] == RED:
                            new_state = state_number - self.__get_power(secondary_node)
                        else:
                            new_state = state_number + self.__get_power(secondary_node)
                        self.matrix[state_number, new_state] += mut[node]/float(total_fitness*len(secondary_nodes))
                        self.matrix[state_number, state_number] -= mut[node]/float(total_fitness*len(secondary_nodes))
        self.matrix[0,0] = 1
        self.matrix[number_of_states-1,number_of_states-1] = 1  
        #print("DONE Matrix")
    def solve(self ):
        size=self.matrix.shape[1]
        right_hand_side=np.zeros((2,size))
        right_hand_side[0][size-1]=1
        right_hand_side[1] = np.full(size, -1)
        right_hand_side[1][size-1] = 0
        right_hand_side[1][0] = 0
        right_hand_side = np.transpose(right_hand_side)
        self.__solution = spsl.spsolve(sps.csr_matrix(self.matrix),right_hand_side)
        
        self.__fixation_probabilities = []
        self.__absorption_times = []
        
        ind=1
        sum_fixation_probabilities = 0
        sum_absorption_times = 0
        while ind<size:
            self.__fixation_probabilities.append(float(self.__solution[ind][0]))
            self.__absorption_times.append(float(self.__solution[ind][1]))
            sum_fixation_probabilities += float(self.__solution[ind][0])
            sum_absorption_times += float(self.__solution[ind][1])
            ind=2*ind
        self.__fixation_probabilities = self.__fixation_probabilities[::-1]
        self.__absorption_times = self.__absorption_times[::-1]    
        self.__average_fixation_probability = sum_fixation_probabilities/len(self.__fixation_probabilities)
        self.__average_absorption_time = sum_absorption_times/len(self.__absorption_times)


    def __color_list_to_decimal(self, color_list):
        number = 0
        for i in range(len(color_list)):
            if color_list[i] == 'blue' or color_list[i] == BLUE:
                number += self.__get_power(i)
        return number
    
    def get_average_fixation_probability(self):
        return self.__average_fixation_probability
    
    def get_average_absorption_time(self):
        return self.__average_absorption_time
    
    def get_fixation_probabilities(self, list_of_blues :list = None , color_list : list = None):
        
        if list_of_blues is not None:
            index = 0
            for node in list_of_blues:
                index += self.__get_power(node)
            return float(self.__solution[index][0])
        elif color_list is not None:
            return float(self.__solution[self.__color_list_to_decimal(color_list)][0])
        else:
            return self.__fixation_probabilities
    
    def get_absorption_times(self, list_of_blues :list = None , color_list : list = None):
        if list_of_blues is not None:
            index = 0
            for node in list_of_blues:
                index += self.__get_power(node)
            return float(self.__solution[index][1])
        elif color_list is not None:
            return float(self.__solution[self.__color_list_to_decimal(color_list)][1])
        else:
            return self.__absorption_times
    
                    
