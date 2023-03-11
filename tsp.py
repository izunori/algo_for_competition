import random

def getDist(p,q):
    d2 = (p[0]-q[0])**2 + (p[1]-q[1])**2
    return d2**0.5

class TSP:
    def __init__(self, n_city, size=100, dist=getDist):
        self.cities = []
        self.dist = dist
        while len(self.cities) < n_city:
            city = (random.randint(0,size), random.randint(0,size))
            if city not in self.cities:
                self.cities.append(city)
    def eval(self, sol):
        res = 0
        for i,j in zip(sol, sol[1:]):
            p,q = self.cities[i], self.cities[j]
            res += self.dist(p,q)
        p,q = self.cities[sol[-1]], self.cities[sol[0]]
        res += self.dist(p,q)
        return res
    def twoOpt(self, sol,i,j):
        sub = sol[i+1:j+1]
        sol[i+1:j+1] = sub[::-1]
    def evalTwoOpt(self,sol,i,j):
        si,si2,sj,sj2 = sol[i],sol[i+1],sol[j],sol[j+1]
        pi,pi2,pj,pj2 = [self.cities[i] for i in [si,si2,sj,sj2]]
        old_d1 = self.dist(pi,pi2)
        old_d2 = self.dist(pj,pj2)
        new_d1 = self.dist(pi,pj)
        new_d2 = self.dist(pi2,pj2)
        return (new_d1+new_d2)-(old_d1+old_d2)

if __name__=='__main__':
    N = 100
    tsp = TSP(N)
    sol = list(range(N))
    print(tsp.eval(sol))
    for _ in range(1000):
        i,j = sorted(random.sample(range(len(sol)-1),2))
        diff = tsp.evalTwoOpt(sol,i,j)
        if diff < 0:
            tsp.twoOpt(sol,i,j)
    print(tsp.eval(sol))

