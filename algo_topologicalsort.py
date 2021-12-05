from collections import deque, defaultdict
def TopologicalSort(g, N):
    n_parent = [0]*(N+1)
    res = []
    for v in g:
        for nv in g[v]:
            n_parent[nv] += 1
    dq = deque([v for v in g if n_parent[v] == 0])
    while dq:
        v = dq.popleft()
        res.append(v)
        for nv in g[v]:
            n_parent[nv] -= 1
            if n_parent[nv] == 0:
                dq.append(nv)
    # if len(res) < n of v -> loop
    return res

def test():
    g = {
        1:[2,3], 2:[3,4,5], 3:[5], 4:[6], 5:[4,6], 6:[]
    }
    print(TopologicalSort(g,6))
    g = {
        1:[2], 2:[3], 3:[4], 4:[1], 5:[1]
    }
    print(TopologicalSort(g,5)) # cycle

if __name__=='__main__':
    test()

