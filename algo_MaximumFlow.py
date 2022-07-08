from collections import defaultdict, deque
from time import perf_counter as time

class MaximumFlow:
    def __init__(self, N):
        self.N = N
        self.g = [[] for _ in range(N)]
        self.c = [[0]*N for _ in range(N)]
        self.inf = 2**64
    def add(self,u,v,c):
        self.g[u].append(v)
        self.g[v].append(u)
        self.c[u][v] = c # Be careful about multiple edges
        self.c[v][u] = 0
    def bfs(self,s):
        dq = deque([s])
        self.d = [self.inf]*self.N
        self.d[s] = 0
        while dq:
            v = dq.popleft()
            for nv in self.g[v]:
                if not self.c[v][nv] > 0:
                    continue
                if self.d[v]+1 < self.d[nv]:
                    self.d[nv] = self.d[v]+1
                    dq.append(nv)
    def dfs(self,s,t):
        st = [(s,self.index[s])]
        p = [-1]*self.N
        while st:
            v,i = st.pop()
            if v == t:
                break
            if i == len(self.g[v]):
                continue
            nv = self.g[v][i]
            if not (self.c[v][nv] > 0 and self.d[v] < self.d[nv]):
                self.index[v] += 1
                st.append((v,self.index[v]))
                continue
            p[nv] = v
            self.index[v] += 1
            st.append((v,self.index[v]))
            st.append((nv,self.index[nv]))
        else:
            return 0
        route = [t]
        while route[-1] != s:
            t = p[t]
            route.append(t)
        route.reverse()
        f = min(self.c[u][v] for u,v in zip(route,route[1:]))
        for u,v in zip(route,route[1:]):
            self.c[u][v] -= f
            self.c[v][u] += f
        return f
    def maxFlow(self,s,t):
        flow = 0
        while True:
            self.bfs(s)
            if self.d[t] == self.inf:
                return flow
            self.index = [0]*self.N
            while True:
                f = self.dfs(s,t)
                if f > 0:
                    flow += f
                else:
                    break

def FordFulkerson(g,s,t):
    flow = 0
    while True:
        p = defaultdict(int)
        visited = defaultdict(bool)
        st = [s]
        visited[s] = True
        while st:
            v = st.pop()
            if v == t:
                break
            for nv,nc in g[v].items():
                if nc > 0 and not visited[nv]:
                    visited[nv] = True
                    p[nv] = v
                    st.append(nv)
        else:
            return flow 
        route = [t]
        while route[-1] != s:
            route.append(p[route[-1]])
        tf = min(g[v][nv] for v,nv in zip(route[1:],route))
        flow += tf
        for v,nv in zip(route[1:],route):
            g[v][nv] -= tf
            g[nv][v] += tf
    return flow 


def FordFulkerson2(graph,capacity,start,terminal):
    cap = defaultdict(int, capacity)
    flow = 0
    while True:
        prev = defaultdict(int)
        visited = defaultdict(bool)
        dq = [start]
        visited[start] = True
        while dq:
            v = dq.pop()
            if v == terminal:
                break
            for nv in graph[v]:
                if not visited[nv] and cap[(v,nv)] > 0:
                    visited[nv] = True
                    prev[nv] = v
                    dq.append(nv)
        else:
            return flow 
        route = [terminal]
        while route[-1] != start:
            route.append(prev[route[-1]])
        tf = min(cap[(v,nv)] for v,nv in zip(route[1:],route))
        flow += tf
        for v,nv in zip(route[1:],route):
            cap[(v,nv)] -= tf
            cap[(nv,v)] += tf
    return flow 

# graph : no direction
def EdmondsKarp(graph,capacity,start,terminal):
    cap = defaultdict(int, capacity)
    flow = 0
    while True:
        prev = defaultdict(int)
        visited = defaultdict(bool)
        dq = deque([start])
        visited[start] = True
        while dq:
            v = dq.popleft()
            if v == terminal:
                break
            for nv in graph[v]:
                if not visited[nv] and cap[(v,nv)] > 0:
                    visited[nv] = True
                    prev[nv] = v
                    dq.append(nv)
        else:
            return flow 
        route = [terminal]
        while route[-1] != start:
            route.append(prev[route[-1]])
        tf = min(cap[(v,nv)] for v,nv in zip(route[1:],route))
        flow += tf
        for v,nv in zip(route[1:],route):
            cap[(v,nv)] -= tf
            cap[(nv,v)] += tf
    return flow 

def test():
    from time import perf_counter as time
    import random
    import networkx as nx

    V = 500
    UVCC = []
    G = nx.DiGraph()

    for u in range(1,V+1):
        for v in range(u+1,V+1):
            c = random.randint(0,100)
            UVCC.append((u,v,c))
            G.add_edge(u,v,capacity=c)

    g = defaultdict(dict)
    gc = MaximumFlow(V+1)
    for s,t,c in UVCC:
        g[s][t] = c
        g[t][s] = 0
        gc.add(s,t,c)

    start=time()
    f = FordFulkerson(g,1,V)
    print(f"gc:{time()-start}") 
    print(f)

    start=time()
    f = gc.maxFlow(1,V)
    print(f"gc:{time()-start}") 
    print(f)

    start=time()
    f,g = nx.maximum_flow(G,1,V)
    print(f"nx:{time()-start}") 
    print(f)

if __name__=='__main__':
    test()
