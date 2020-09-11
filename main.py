import numpy as np
import random
from scipy import signal
from collections import defaultdict

class RandomAgent:
    def turn(self, field):
        h,w = field.shape
        selected = False
        stepx, stepy = None, None
        while not selected:
            stepx = random.randint(0, h-1)
            stepy = random.randint(0, w-1)
            if field[stepx, stepy] == 0:
                selected = True

        return stepx+1, stepy+1
class XO:
    """
    Game tic tac toe
    This class define field and rules.
    """
    def __init__(self, *args):
        self.n, self.k = args
        self.counter = self.n*self.k
        assert self.k <= self.n , "Params are impossible, n must be > or = than k"
        assert type(self.k) == int and type(self.n) == int , "Invalid type, change n and k to INT"
    
    def create_field(self):
        self.field = np.zeros((self.n, self.n))
        
        # Sliding window
        self.kind_step = defaultdict(np.array)
        
        for kind in ['hor','vert','diag', 'diag_rev']:
            if kind == 'hor':
                self.kind_step[kind] = np.ones(self.k).reshape(self.k,1)
            elif kind == 'vert':
                self.kind_step[kind] = np.ones(self.k).reshape(1, self.k)
            elif kind == 'diag':
                self.kind_step[kind] = np.eye(self.k)
            elif kind == 'diag_rev':
                self.kind_step[kind] = np.rot90(np.eye(self.k))
        
        return self.field
    
    def get_field(self):
        return self.field
    
    def make_round(self,x,y, turn):
        if self.field[x-1,y-1] != 0:
            print("The place have already taken! Choose another cell.")
            return False
        self.field[x-1,y-1] = (1 if turn == 1 else -1)
        return True
    
    def start(self):
        print("Choose your side. 1/0?")
        self.side = int(input())
        assert type(self.side) or (self.side != 0 or self.side != 1), "Incorrect value"
        
        return self.create_field()
    
    def get_win_table(self):
        win_table = list()
        for kind in self.kind_step.values():
            win_table.append(signal.convolve2d(self.field, kind, mode='same'))
        return win_table
    
    def check_to_win(self):
        win_checker = self.get_win_table()
        for i in win_checker:
            if np.where(i == k)[0].size > 0 or np.where(i == -k)[0].size > 0:
                print("Game end")
                return True
        return False
    def print_field(self):
        res = self.field.copy().astype(str)
        res[res == "-1.0"] = "0"
        res[res == "0.0"] = "."
        res[res == "1.0"] = "X"
        print(res)
        del res
        return

#GAME LOOP
print("Enter playground size N x N and K toes to win (ex. 1 2)")
n,k = map(lambda x: int(x),input().split())
assert n > 0 and k > 0, "N and K must be more then 0 both."
game = XO(n,k)
game.start()

#Define who will make first step
turn = 1 if game.side == 1 else 0

AI = RandomAgent()
while True:
    game.counter -= 1
    if turn==1:
        indicator = False
        while not indicator:
            print(f"Put COLUMN and ROW (ex. {random.randint(1, n)} {random.randint(1, n)})")
            y,x = map(lambda x: int(x),input().split())
            if x <= game.n and y <= game.n and x > 0 and y > 0:
                print(x <= game.n)
                indicator = game.make_round(x,y,game.side)
            else:
                assert False, "OOPS! You have fall under ground"
        turn = 0
        if game.check_to_win():
            print("You Won!")
            break
    else:
        # Simple AI
        x,y = AI.turn(game.get_field())
        game.make_round(x,y,abs(game.side-1))
        turn = 1
        game.print_field()
        if game.check_to_win():
            print("Agent Won!")
            break
    if game.counter == 0:
            print("Draw!")
            break
