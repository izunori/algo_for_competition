from collections import defaultdict

class Lowlink:
    def __init__(self, g, s=0):
        self.g = g
        self.low = {}
        order = {}
        parent = {}
        tour = []
        self.s = s
        st = [self.s]
        l = 0
        while st:
            v = st.pop()
            if v in order:
                continue
            tour.append(v)
            order[v] = self.low[v] = l
            l += 1
            for nv in g[v]:
                if nv in order:
                    if nv != parent[v]:
                        self.low[v] = min(self.low[v],order[nv])
                    continue
                parent[nv] = v
                st.append(nv)
        for v in reversed(tour):
            for nv in g[v]:
                if order[v] < order[nv]:
                    self.low[v] = min(self.low[v], self.low[nv])
        self.order, self.parent = order, parent
    def isBridge(self,u,v):
        u,v = (u,v) if self.order[u] < self.order[v] else (v,u)
        return not (self.low[v] <= self.order[u])
    def isJoint(self, v):
        if v == self.s:
            return len(self.g[self.s]) != 1
        return any(self.order[v] <= self.low[nv] for nv in self.g[v] if self.parent[v] != nv)


def test():
    edges = [
            [1,5], [1,8], [0,9],
            [0,1], [1,2], [2,3], [2,4], [2,5], [1,6], [6,7], [6,8], [8,9],
    ]
    g = defaultdict(list)
    for u,v in edges:
        g[u].append(v)
        g[v].append(u)
    ll = Lowlink(g)
    print(ll.low)

if __name__=='__main__':
    test()




