from collections import defaultdict, deque
from functools import reduce
from heapq import heappop, heappush

# Euler Tour
def EulerTour(g,s):
    n = len(g)
    dq = [s]
    ls = [-1]*(n+1)
    rs = [-1]*(n+1)
    vtour = []
    etour = []
    depth = [-1]*(n+1)
    parent = [False]*(n+1)
    visited = [False]*(n+1)
    def dfs(v,d):
        depth[v] = d
        visited[v] = True
        ls[v] = len(vtour)
        vtour.append(v)
        etour.append(v)
        for nv in g[v]:
            if not visited[nv]:
                parent[nv] = v
                dfs(nv,d+1)
        rs[v] = len(vtour)
        etour.append(-v)
        vtour.append(parent[v])
    dfs(s,0)
    return ls,rs,etour,vtour,parent,depth

def EulerTour2():
    g = { 1:[2,3], 2:[1,4], 3:[1], 4:[2,5,6], 5:[4], 6:[4] }
    N = 6
    visited = [False]*(N+1)
    dq = [1]
    while dq:
        print(dq)
        v = dq.pop()
        print(v)
        visited[v] = True
        for nv in g[v]:
            if not visited[nv]:
                dq.append(nv)
            
print("TEST")
print(EulerTour2())
print("TEST END")
def EulerTourSample():
    print("Euler Tour")
    g = {1:[2],2:[1,3,5],3:[2,4,6],4:[3],5:[2],6:[3,7,8],7:[6],8:[6]}
    ls,rs,etour,vtour,parent,depth = EulerTour(g,1)
    print("in",ls) # when enter the node from 0.
    print("out",rs) # when return the node. 
    print("etour",etour) # minus is inverse
    print("vtour",vtour)
    print("parent",parent)
    print("depth",depth) # first is 0

# Network Flow
# graph, capacity, start, terminal
def FordFulkerson(g,c,s,t):
    Gf = {k:v[:] for k,v in g.items()}
    Gf = defaultdict(list,Gf)
    cap = {k:v for k,v in c.items()}
    # inverse path
    for v in g.keys():
        for nv in g[v]:
            Gf[nv].append(v)
            cap[(nv,v)] = 0
    N = len(g)
    res = 0
    while True:
        visited = [False]*(N+1)
        prev = [-1]*(N+1)
        dq = [s]
        while dq:
            v = dq.pop()
            if v == t:
                break
            visited[v] = True
            for nv in Gf[v]:
                if not visited[nv] and cap[(v,nv)] > 0:
                    dq.append(nv)
                    prev[nv] = v
        else:
            return res 
        route = [t]
        while route[-1] != s:
            route.append(prev[route[-1]])
        f = min([cap[(v,nv)] for v,nv in zip(route[1:],route)])
        res += f
        for v,nv in zip(route[1:],route):
            cap[(v,nv)] -= f
            cap[(nv,v)] += f
    return res

# under construction
def Dinic(g,c,s,t):
    Gf = {k:v[:] for k,v in g.items()}
    Gf = defaultdict(list,Gf)
    cap = {k:v for k,v in c.items()}
    # inverse path
    for v in g.keys():
        for nv in g[v]:
            Gf[nv].append(v)
            cap[(nv,v)] = 0
    N = len(g)
    res = 0
    while True:
        visited = [False]*(N+1)
        prev = [-1]*(N+1)
        dq = [s]
        while dq:
            v = dq.pop()
            if v == t:
                break
            visited[v] = True
            for nv in Gf[v]:
                if not visited[nv] and cap[(v,nv)] > 0:
                    dq.append(nv)
                    prev[nv] = v
        else:
            return res 
        route = [t]
        while route[-1] != s:
            route.append(prev[route[-1]])
        f = min([cap[(v,nv)] for v,nv in zip(route[1:],route)])
        res += f
        for v,nv in zip(route[1:],route):
            cap[(v,nv)] -= f
            cap[(nv,v)] += f
    return res

# Topological Sort

# Rerooting (example. max depth)
def Rerooting(g):
    N = len(g)
    memo = {}
    vtour = []
    visited = [False]*(N+1)
    dq = deque([(0,1)])
    while dq:
        p, v = dq.pop()
        vtour.append((p,v))
        visited[v] = True
        for nv in g[v]:
            if not visited[nv]:
                dq.append((v,nv))
    for p, v in vtour[::-1]:
        d = 0
        for nv in g[v]:
            if nv == p:
                continue
            d = max(d, memo[(v,nv)])
        memo[(p,v)] = d + 1
    visited = [False]*(N+1)
    dq = deque([1])
    while dq:
        v = dq.popleft()
        visited[v] = True
        seq = []
        for nv in g[v]:
            if not visited[nv]:
                dq.append(nv)
            seq.append(memo[(v,nv)])
        L = [0]
        for s in seq[:-1]:
            L.append(max(L[-1],s))
        R = [0]
        for s in seq[-1:0:-1]:
            R.append(max(R[-1],s))
        R = R[::-1]
        memo[(0,v)] = max(L[-1], seq[-1]) + 1
        for nv,l,r in zip(g[v],L,R):
            memo[(nv,v)] = max(l,r) + 1
    return {i:memo[(0,i)] for i in g.keys()}


if __name__=='__main__':
    g = {
        1:[2,3], 2:[3,4,5], 3:[5], 4:[6], 5:[4,6], 6:[]
    }
    c = {
        (1,2):9, (1,3):9, (2,3):1, (2,4):3, (2,5):7, (3,5):8, (5,4):5, (4,6):9, (5,6):9
    }
    maxf = FordFulkerson(g,c,1,6)
    print(maxf)
    ts = TopologicalSort(g)
    print(ts)
    EulerTourSample()
    t = {1:[2],2:[1,3,5],3:[2,4,6],4:[3],5:[2],6:[3,7,8],7:[6],8:[6]}
    print("--- rerooting")
    print(Rerooting(t))
    g = {1:[2,4],2:[1,3],3:[2,4],4:[1,3]}
    c = {(1,4):3,(4,1):3,(3,4):1,(4,3):1,(2,3):1,(3,2):1,(1,2):3,(2,1):3}






