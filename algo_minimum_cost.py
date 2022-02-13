from collections import defaultdict, deque
import heapq as hq
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
    random.seed(10)
    V = 300
    F = 300
    UVCC = []
    G = nx.DiGraph()

    G.add_node(1, demand=-F)
    G.add_node(V, demand=F)
    for u in range(1,V+1):
        for v in range(u+1,V+1):
            c = random.randint(0,10)
            d = random.randint(1,10)
            UVCC.append((u,v,c,d))
            G.add_edge(u,v,weight=d, capacity=c)

    g = defaultdict(dict)
    g2 = defaultdict(dict)
    for s,t,cp,cs in UVCC:
        g[s][t] = [cp,cs]
        g[t][s] = [0,-cs]
        g2[s][t] = [cp,cs]
        g2[t][s] = [0,-cs]

    start = time()
    f = minimumCost(g,1,V,F)
    print(f"{time() - start}s")
    print(f)

    start = time()
    f = minimumCost2(g2,1,V,F)
    print(f"{time() - start}s")
    print(f)

    start = time()
    fc, _ = nx.network_simplex(G)
    print(f"{time() - start}s")
    print(fc)

def test2():
    UVCC = [
            (0,1,2,1),
            (0,2,1,2),
            (1,2,1,1),
            (1,3,1,3),
            (2,3,2,1),
            ]
    g = defaultdict(dict)
    for s,t,cp,cs in UVCC:
        g[s][t] = [cp,cs]
        g[t][s] = [0,-cs]
    print(minimumCost(g,0,3,2), 6)

if __name__=='__main__':
    test()
