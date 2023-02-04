from collections import defaultdict, deque
from algo_segment_tree import SegmentTree
N = 8

class LCA:
    def __init__(self, g, N, pv=1, GN=20):
        g = defaultdict(list,g)
        self.N = N
        self.g = g
        self.GN = GN
        self.pv = pv
        # ancester
        self.parent = [0]*(self.N+1)
        for p,cs in g.items():
            for c in cs:
                self.parent[c] = p
        self.ancestor = [self.parent]
        for i in range(self.GN):
            temp = [0]*(N+1)
            for v in range(self.N):
                temp[v] = self.ancestor[-1][self.ancestor[-1][v]]
            self.ancestor.append(temp)

        self.depth = [-1]*(N+1)
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
    def __init__(self, g, N, pv=1):
        g = defaultdict(list, g)
        self.inf = 10**18
        self.depth = [-1]*(N+1)
        self.depth[pv] = 0
        self.euler = []
        l = [pv]
        self.inn = [self.inf]*(N+1)
        self.out = [self.inf]*(N+1)
        while l:
            v = l.pop()
            if v < 0:
                self.out[-v] = len(self.euler)
                self.euler.append(-v)
                continue
            self.inn[v] = len(self.euler)
            self.out[v] = len(self.euler)
            self.euler.append(v)
            for nv in g[v]:
                if self.depth[nv] == -1:
                    self.depth[nv] = self.depth[v]+1
                    l.append(-v)
                    l.append(nv)
        self.seg = SegmentTree([(self.depth[v],v) for v in self.euler], min, (self.inf,self.inf))
    def find(self, u,v):
        s,t = sorted([self.inn[u],self.inn[v]])
        _, c = self.seg.get(s,t+1)
        return c

def test():
    g = {1:[2,3],2:[4],3:[5,6],6:[7]}
    lca = LCA(g,7)
    print(lca.find(4,6),1)
    print(lca.find(2,6),1)
    print(lca.find(5,6),3)
    print(lca.find(5,7),3)

    lca2 = LCA2(g,7)
    print(lca2.find(4,6),1)
    print(lca2.find(2,6),1)
    print(lca2.find(5,6),3)
    print(lca2.find(5,7),3)

def perf():
    from time import perf_counter as time
    import networkx as nx
    import random
    N = 10**5
    M = 10**5
    g = nx.to_dict_of_lists(nx.random_tree(N))
    samples = random.choices(range(N), k=2*M)

    # doubling
    start = time()
    lca = LCA(g, N)
    print(f"{time() - start}s")
    for u,v in zip(samples[::2],samples[1::2]):
        lca.find(u,v)
    print(f"{time() - start}s")

    # segment tree
    start = time()
    lca2 = LCA2(g, N)
    print(f"{time() - start}s")
    for u,v in zip(samples[::2],samples[1::2]):
        lca2.find(u,v)
    print(f"{time() - start}s")

if __name__=='__main__':
    test()
    #perf()
