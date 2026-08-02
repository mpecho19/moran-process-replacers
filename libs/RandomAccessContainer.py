import random
from copy import deepcopy
class RandomAccessContainer:
    def __init__(self, copy : 'RandomAccessContainer' = None) -> None:
        if copy is None:
            self.items = [] #1 2 3 8 5 6 7 14  
            self.item_to_index = {} #1 1, 2 2, ... 8 4,
        else:
            self.items = copy.items.copy()
            #Netusim ci nemusi byt deep copy
            self.item_to_index = copy.item_to_index.copy()
            #self.item_to_index = deepcopy(copy.item_to_index)
        
    def __len__(self) -> int:
        return len(self.items)
    
    def add_item(self, item):
        if item not in self.item_to_index:
            self.item_to_index[item] = len(self.items)
            self.items.append(item)
            
        
    def remove_item(self, item):
        index = self.item_to_index.pop(item)
        popped_item = self.items.pop()
        if index != len(self.items):
            self.items[index] = popped_item
            self.item_to_index[popped_item] = index
            
    def get_random_item(self):
        return random.choice(self.items)
    
    def check_if_in(self, item):
        return item in self.item_to_index

# test = RandomAccessContainer()
# for i in range(10):
#     test.add_item(i)

# test2 = RandomAccessContainer(copy=test)

# for i in range(10,15):
#     test2.add_item(i)
# for i in range(5):
#     test2.remove_item(i)
    
# print(test.item_to_index)
# print(test.items)
# print(test2.item_to_index)
# print(test2.items)     