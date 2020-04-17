import pickle
import os


def parse_command():
        print('Type command "start <labyrinth_size>", "load <file_name>" or "quit"')
        
        while True:
            command = input().split()
            if command[0] == 'start':
                command[1] = int(command[1])
                return True, command[1]
            
            elif command[0] == 'load':
                command[1] = command[1] + '.pkl'
                return False, command[1]
            
            elif command[0] == 'quit':
                return False
            
            else:
                print('Unknown command, try again or type "quit"')
                

def load_game(file_name):
    with open(os.path.join('saves', file_name), 'rb') as f:
        game = pickle.load(f)
    return game