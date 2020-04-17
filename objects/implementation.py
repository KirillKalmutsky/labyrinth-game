from objects.interface import Item


class Treasure(Item):
    
    def __init__(self):
        self.name = 'Treasure'
        self.value = 10
        
    def __str__(self):
        return self.name
    
    def buy_values(self):
        return self.value
    
    def sell_value(self):
        return self.value / 2