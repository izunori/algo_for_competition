from collections import defaultdict, deque

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
        self.c[v][u] = -c
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
        st = [s]
        p = [-1]*self.N
        while st:
            v = st.pop()
            if v == t:
                break
            for nv in self.g[v]:
                if not (self.c[v][nv] > 0 and self.d[v] < self.d[nv]):
                    continue
                p[nv] = v
                st.append(nv)
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
    # sample : https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
    UVC = [
            (0,1,16),
            (0,2,13),
            (1,2,10),
            (2,1,4),
            (1,3,12),
            (3,2,9),
            (2,4,14),
            (4,3,7),
            (3,5,20),
            (4,5,4)
            ]
    g = defaultdict(dict)
    g2 = defaultdict(list)
    cap = defaultdict(int)
    gr = MaximumFlow(21)
    for u,v,c in UVC:
        g[u][v] = c
        g[v][u] = 0
        g2[u].append(v)
        g2[v].append(u)
        cap[(u,v)] = c
        gr.add(u,v,c)
    print(FordFulkerson(g,0,5), 23)
    print(FordFulkerson2(g2,cap,0,5), 23)
    print(EdmondsKarp(g,cap,0,5), 23)
    print(gr.maxFlow(0,5))

if __name__=='__main__':
    test()
