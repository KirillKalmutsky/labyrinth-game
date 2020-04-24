from creatures.interface import MovingCreature


class Bear(MovingCreature):
    
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dmg = 50

        
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
    
    
    def hit(self, target):
        return target.lose_hp(self.dmg)