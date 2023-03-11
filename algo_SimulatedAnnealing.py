from tsp import TSP
import time
import random
import math

class HillClimbing:
    def accept(slef, new_cost, old_cost):
        return new_cost < old_cost

class SimulatedAnnealing:
    def __init__(self, end_val, stemp, etemp):
        self.end_val = end_val
        self.stemp = stemp
        self.etemp = etemp
    def accept(self, new_cost, old_cost, val):
        diff = new_cost - old_cost
        if diff < 0:
            return True
        temp = self.stemp + val * (self.etemp - self.stemp) / self.end_val
        prob = pow(math.e, -diff/temp)
        if random.random() < prob:
            return True
        return False

def test_HC(sol, tsp, M):
    hc = HillClimbing()
    score = tsp.eval(sol)
    cities = list(range(len(sol)-1))
    for _ in range(M):
        i,j = sorted(random.sample(cities,2))
        diff = tsp.evalTwoOpt(sol,i,j)
        new_score = score + diff
        if hc.accept(new_score, score):
            score = new_score
            tsp.twoOpt(sol,i,j)
    score = tsp.eval(sol)
    print(score)

def test_SA(sol, tsp, M):
    sa = SimulatedAnnealing(M, 10, 1)
    score = tsp.eval(sol)
    cities = list(range(len(sol)-1))
    for m in range(M):
        i,j = sorted(random.sample(cities,2))
        diff = tsp.evalTwoOpt(sol,i,j)
        new_score = score + diff
        if sa.accept(new_score, score, m):
            score = new_score
            tsp.twoOpt(sol,i,j)
    score = tsp.eval(sol)
    print(score)

if __name__=='__main__':
    N = 100
    tsp = TSP(N)
    sol = list(range(N))
    ini_score = tsp.eval(sol)
    print(ini_score)
    M = 10**5
    test_HC(sol[:], tsp, M)
    test_SA(sol[:], tsp, M)
