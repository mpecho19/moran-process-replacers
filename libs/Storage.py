from libs.RandomAccessContainer import *

class Storage:
    blueContainer : RandomAccessContainer
    redContainer : RandomAccessContainer
    allColors : list
    
    def __init__(self,  redList  = [] , blueList = [] , nodes = [], copy : 'Storage' = None) -> None:
        if copy is None:
            self.blueContainer = RandomAccessContainer()
            self.redContainer = RandomAccessContainer()
            self.allColors = []
            for node in blueList:
                self.add_item(node, 'blue')
            for node in redList:
                self.add_item(node, 'red')
            for node in nodes:
                if self.get_color_of_node(node) == 'blue':
                    self.allColors.append('blue')
                elif self.get_color_of_node(node) == 'red':
                    self.allColors.append('red')
        else:
            self.blueContainer = RandomAccessContainer(copy.blueContainer)
            self.redContainer = RandomAccessContainer(copy.redContainer)
            self.allColors = copy.allColors.copy()
            
    
            
    def add_item(self, item, color):
        if color == 'blue':
            self.blueContainer.add_item(item)
        if color == 'red':
            self.redContainer.add_item(item)
    
    def get_color_of_node(self, item):
        if self.blueContainer.check_if_in(item):
            return 'blue'
        elif self.redContainer.check_if_in(item):
            return 'red'
        
    def get_all_colors(self):
        return self.allColors
        
    def change_color_to(self, item, color):
        if self.get_color_of_node(item) != color:
            self.swap(item)
    
    def swap(self, item):
        if self.blueContainer.check_if_in(item):
            self.blueContainer.remove_item(item)
            self.redContainer.add_item(item)
            self.allColors[item] = 'red'
        elif self.redContainer.check_if_in(item):
            self.redContainer.remove_item(item)
            self.blueContainer.add_item(item)
            self.allColors[item] = 'blue'
            
    def get_number_of(self, color):
        if color == 'blue':
            return len(self.blueContainer)
        elif color == "red":
            return len(self.redContainer)
            
    def get_random_of_color(self, color):
        if color == 'blue':
            return self.blueContainer.get_random_item()
        elif color == "red":
            return self.redContainer.get_random_item()
        