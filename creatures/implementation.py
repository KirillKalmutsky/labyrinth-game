from creatures.interface import MovingCreature


class Player(MovingCreature):
    
    def __init__(self, x, y):
        self.inventory = []
        self.exit_seen = False
        self.x = x
        self.y = y
        
        
    def get_item(self, item):
        self.inventory.append(item)
        
        
    def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1
        else:
            assert False
           
        
    def check_item(self, item):
        return item in self.inventory