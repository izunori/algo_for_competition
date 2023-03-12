import othello
import random

class RandomPlayer:
    def __init__(self, __nstates):
        self.__nstates = __nstates
    def act(self, state):
        nstates = [nstate for nstate in self.__nstates(state)]
        if nstates:
            return random.choice(nstates)
        return None

def game(p1, p2):
    bw = othello.generate()
    while True:
        update = False
        for p,t in [(p1,1),(p2,-1)]:
            nbw = p.act((bw,t))
            if nbw is not None:
                update = True
                bw = nbw
        if not update:
            break
    othello.printBoard(bw)

if __name__=='__main__':
    def getAllNextState(state):
        bw,turn = state
        return [nbw for nbw,_ in othello.nextStateOf(bw,turn)]
    p1 = RandomPlayer(getAllNextState)
    p2 = RandomPlayer(getAllNextState)
    game(p1,p2)
