from collections import defaultdict, deque
from algo_segment_tree import SegmentTree
N = 8

class LCA:
    N = N
    GN = 4
    def __init__(self, g, pv=1):
        g = defaultdict(list,g)
        self.g = g
        self.pv = pv

        # ancester
        self.parent = [0]*self.N
        for p,cs in g.items():
            for c in cs:
                self.parent[c] = p
        self.ancestor = [self.parent]
        for i in range(self.GN):
            temp = [0]*N
            for v in range(self.N):
                temp[v] = self.ancestor[-1][self.ancestor[-1][v]]
            self.ancestor.append(temp)

        self.depth = [-1]*N
        self.depth[pv] = 0
        dq = deque([pv])
        while dq:
            v = dq.popleft()
            for nv in g[v]:
                if self.depth[nv] == -1:
                    self.depth[nv] = self.depth[v] + 1
                    dq.append(nv)

    def find(self,u,v):
        if self.depth[u] > self.depth[v]:
            u,v = v,u
        diff = self.depth[v] - self.depth[u]
        for i,ancestor in enumerate(self.ancestor):
            if diff & (1<<i):
                v = self.ancestor[i][v]
        for ancestor in self.ancestor[::-1]:
            if ancestor[u] != ancestor[v]:
                u,v = map(lambda x : ancestor[x], (u,v))
        return self.ancestor[0][u]

class LCA2:
    N = N
    def __init__(self, g, pv=1):
        l = [pv]
        euler = []
        visited = [False]*N
        while l:
            v = l.pop()
            if visited[v]
                euler.append(v)
                continue
            euler.append(v)
            l.append(-v)
            for nv in g[v]:

def test():
    g = {1:[2,3],2:[4],3:[5,6],6:[7]}
    lca = LCA(g)
    print(lca.find(4,6),1)
    print(lca.find(2,6),1)
    print(lca.find(5,6),3)
    print(lca.find(5,7),3)

if __name__=='__main__':
    test()
