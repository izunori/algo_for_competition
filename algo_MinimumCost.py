from collections import defaultdict, deque
import heapq as hq
class MinimumCost:
    def __init__(self, N):
        self.N = N
        self.g = [[] for _ in range(N)]
        self.cap = [[0]*N for _ in range(N)]
        self.cost = [[0]*N for _ in range(N)]
        self.ptn = [0]*self.N
        self.first = True
    def add(self,u,v,cap,cost):
        self.g[u].append(v)
        self.g[v].append(u)
        self.cap[u][v] = cap
        self.cost[u][v] = cost
        self.cost[v][u] = -cost
    def minimumCost(self,s,t,f):
        res = 0
        flow = 0
        inf = 2**64
        nedge = sum(map(len,self.g))
        while True:
            cost = [inf]*self.N
            cost[s] = 0
            p = [-1]*self.N
            if self.first:
                # Bellman-Ford
                for _ in range(nedge):
                    update = False
                    for v in range(self.N):
                        for nv in self.g[v]:
                            cap = self.cap[v][nv]
                            if cap <= 0:
                                continue
                            c = self.cost[v][nv]
                            if cost[v] + c < cost[nv]:
                                update = True
                                cost[nv] = cost[v] + c
                                p[nv] = v
                    if not update:
                        break
                else:
                    return inf # find closed negative loop
                self.first = False
            else:
                # Dijkstra
                h = [(0,s)]
                cost[s] = 0
                while h:
                    d,v = hq.heappop(h)
                    if cost[v] < d:
                        continue
                    for nv in self.g[v]:
                        cap = self.cap[v][nv]
                        if cap <= 0:
                            continue
                        c = self.cost[v][nv] + self.ptn[v] - self.ptn[nv]
                        if cost[v]+c < cost[nv]:
                            cost[nv] = cost[v]+c
                            hq.heappush(h,(cost[nv],nv))
                            p[nv] = v
            if cost[t] == inf:
                return inf
            for v in range(self.N):
                cost[v] += self.ptn[v] - self.ptn[s]
                self.ptn[v] += cost[v]
            route = [t]
            while route[-1] != s:
                route.append(p[route[-1]])
            route.reverse()
            tf = min(self.cap[v][nv] for v,nv in zip(route,route[1:]))
            if flow + tf >= f:
                res += cost[t]*(f-flow)
                flow = f
                return res
            else:
                res += cost[t]*tf
                flow += tf
            for v,nv in zip(route,route[1:]):
                self.cap[v][nv] -= tf
                self.cap[nv][v] += tf

# only plus capacity
def minimumCost2(g,s,t,f):
    res = 0
    flow = 0
    inf = 2**64
    E = sum(len(vs) for vs in g.values())
    while True:
        cost = defaultdict(lambda : inf)
        cost[s] = 0
        p = defaultdict(lambda : -inf)
        for i in range(E):
            update = False
            for v in g:
                for nv,(c,d) in g[v].items():
                    if c > 0 and cost[v] + d < cost[nv]:
                        update = True
                        cost[nv] = cost[v] + d
                        p[nv] = v
            if not update:
                break
        else:
            return inf # closed loop
        if cost[t] == inf:
            return -1
        route = [t]
        while route[-1] != s:
            route.append(p[route[-1]])
        tf = min(g[v][nv][0] for v,nv in zip(route[1:],route))
        if flow + tf >= f:
            res += cost[t]*(f-flow)
            return res
        else:
            res += cost[t]*tf
            flow += tf
        for v,nv in zip(route[1:],route):
            g[v][nv][0] -= tf
            g[nv][v][0] += tf

def minimumCost(g,s,t,f):
    res = 0
    flow = 0
    inf = 2**64
    E = sum(len(vs) for vs in g.values())
    first = True
    while True:
        cost = defaultdict(lambda : inf)
        cost[s] = 0
        p = defaultdict(lambda : -inf)
        ptn = defaultdict(int)
        if first:
            for i in range(E):
                update = False
                for v in g:
                    for nv,(c,d) in g[v].items():
                        if c > 0 and cost[v] + d < cost[nv]:
                            update = True
                            cost[nv] = cost[v] + d
                            p[nv] = v
                if not update:
                    break
            else:
                return inf # closed loop
            first = False
        else:
            h = [(0,s)]
            cost[s] = 0
            while h:
                d,v = hq.heappop(h)
                if cost[v] < d:
                    continue
                for nv,(nc,nd) in g[v].items():
                    nd += ptn[v] - ptn[nv]
                    if nc > 0 and cost[v]+nd < cost[nv]:
                        cost[nv] = cost[v]+nd
                        hq.heappush(h,(cost[nv],nv))
                        p[nv] = v
        if cost[t] == inf:
            return -1
        for v in cost:
            cost[v] += ptn[v] - ptn[s]
            ptn[v] += cost[v]
        route = [t]
        while route[-1] != s:
            route.append(p[route[-1]])
        tf = min(g[v][nv][0] for v,nv in zip(route[1:],route))
        if flow + tf >= f:
            res += cost[t]*(f-flow)
            return res
        else:
            res += cost[t]*tf
            flow += tf
        for v,nv in zip(route[1:],route):
            g[v][nv][0] -= tf
            g[nv][v][0] += tf

def test():
    from time import perf_counter as time
    import random
    import networkx as nx
    V = 300
    F = 300
    UVCC = []
    G = nx.DiGraph()

    G.add_node(1, demand=-F)
    G.add_node(V, demand=F)
    for u in range(1,V+1):
        for v in range(u+1,V+1):
            c = random.randint(0,10)
            d = random.randint(0,10)
            UVCC.append((u,v,c,d))
            G.add_edge(u,v,weight=d, capacity=c)

    g = defaultdict(dict)
    g2 = defaultdict(dict)
    gc = MinimumCost(V+1)
    for s,t,cp,cs in UVCC:
        g[s][t] = [cp,cs]
        g[t][s] = [0,-cs]
        g2[s][t] = [cp,cs]
        g2[t][s] = [0,-cs]
        gc.add(s,t,cp,cs)

    start = time()
    f = minimumCost(g,1,V,F)
    print(f"first djy: {time() - start}s")
    print(f)

    #start = time()
    #f = minimumCost2(g2,1,V,F)
    #print(f"only bellman : {time() - start}s")
    #print(f)

    start = time()
    f = gc.minimumCost(1,V,F)
    print(f"{time() - start}s")
    print(f)

    start = time()
    fc, _ = nx.network_simplex(G)
    print(f"{time() - start}s")
    print(fc)

if __name__=='__main__':
    test()
