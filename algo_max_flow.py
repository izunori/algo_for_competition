from collections import defaultdict, deque

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
    for u,v,c in UVC:
        g[u][v] = c
        g[v][u] = 0
        g2[u].append(v)
        g2[v].append(u)
        cap[(u,v)] = c
    print(FordFulkerson(g,0,5), 23)
    print(FordFulkerson2(g2,cap,0,5), 23)
    print(EdmondsKarp(g,cap,0,5), 23)

if __name__=='__main__':
    test()
