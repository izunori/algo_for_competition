from collections import defaultdict, deque

# graph : no direction
def FordFulkerson(graph,capacity,start,terminal):
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
    g = defaultdict(list)
    cap = defaultdict(int)
    for u,v,c in UVC:
        g[u].append(v)
        g[v].append(u)
        cap[(u,v)] = c
    print(FordFulkerson(g,cap,0,5), 23)

if __name__=='__main__':
    test()
