from collections import deque, defaultdict
def TopologicalSort(g):
    n_parent = defaultdict(int)
    res = []
    for nvs in g.values():
        for nv in nvs:
            n_parent[nv] += 1
    dq = deque([v for v in g if n_parent[v] == 0])
    while dq:
        v = dq.popleft()
        res.append(v)
        for nv in g[v]:
            n_parent[nv] -= 1
            if n_parent[nv] == 0:
                dq.append(nv)
    # if any(n_parent), g has a cycle
    return res

def test():
    g = {
        1:[2,3], 2:[3,4,5], 3:[5], 4:[6], 5:[4,6], 6:[]
    }
    print(TopologicalSort(g))
    g = {
        1:[2], 2:[3], 3:[4], 4:[1], 5:[1]
    }
    print(TopologicalSort(g)) # cycle

if __name__=='__main__':
    test()

