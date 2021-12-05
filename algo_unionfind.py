# Union Find
from collections import defaultdict
class UnionFind:
    def __init__(self,nodes):
        self.parents = {node : node for node in nodes}
        self.num = {node : 1 for node in self.parents.keys()}
    def root(self,x):
        if x == self.parents[x]:
            return x
        else:
            rt = self.root(self.parents[x])
            self.parents[x] = rt
            return rt
    def find(self,x,y):
        return self.root(x) == self.root(y)
    def union(self,x,y):
        rx = self.root(x)
        ry = self.root(y)
        if rx == ry:
            return False
        if self.num[ry] >= self.num[rx]:
            self.num[ry] += self.num[rx]
            self.parents[rx] = ry
        else:
            self.num[rx] += self.num[ry]
            self.parents[ry] = rx
        return True
    def get(self):
        res = defaultdict(list)
        for node in self.parents:
            res[self.root(node)].append(node)
        return list(res.values())

def test():
    samples = range(10)
    uf = UnionFind(samples)
    uf.union(0,8)
    uf.union(0,7)
    uf.union(1,5)
    print(uf.find(8,7))
    print(uf.get())

if __name__=='__main__':
    test()
