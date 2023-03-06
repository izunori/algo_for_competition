import random
import matplotlib.pyplot as plt

def getDist(p,q):
    d2 = (p[0]-q[0])**2 + (p[1]-q[1])**2
    return d2**0.5

class TSP:
    def __init__(self, n_city, size=100):
        self.cities = []
        while len(self.cities) < n_city:
            city = (random.randint(0,size), random.randint(0,size))
            if city not in self.cities:
                self.cities.append(city)

    def eval(self, sol):
        res = 0
        for i,j in zip(sol, sol[1:]):
            p,q = self.cities[i], self.cities[j]
            res += getDist(p,q)
        p,q = self.cities[sol[-1]], self.cities[sol[0]]
        res += getDist(p,q)
        return res

    def twoOpt(self, sol,i,j):
        sub = sol[i+1:j+1]
        sol[i+1:j+1] = sub[::-1]

    def solve(self, sol):
        scores = [self.eval(sol)]
        for i in range(20000):
            i,j = sorted(random.sample(range(len(sol)-1),2))
            si,si2,sj,sj2 = sol[i],sol[i+1],sol[j],sol[j+1]
            pi,pi2,pj,pj2 = [self.cities[i] for i in [si,si2,sj,sj2]]
            old_d1 = getDist(pi,pi2)
            old_d2 = getDist(pj,pj2)
            new_d1 = getDist(pi,pj)
            new_d2 = getDist(pi2,pj2)
            if new_d1 + new_d2 < old_d1 + old_d2:
                self.twoOpt(sol,i,j)
            scores.append(self.eval(sol))
        return scores

if __name__=='__main__':
    N = 100
    tsp = TSP(N)
    sol = list(range(N))
    print(tsp.eval(sol))
    scores = tsp.solve(sol)
    path = [tsp.cities[i] for i in sol]
    path += [path[0]]
    path = list(zip(*path))
    print(tsp.eval(sol))
    scores = tsp.solve(sol)
    print(tsp.eval(sol))
    path2 = [tsp.cities[i] for i in sol]
    path2 += [path2[0]]
    path2 = list(zip(*path2))
    plt.plot(path[0],path[1])
    plt.plot(path2[0],path2[1])
    plt.show()

