class BinaryTrie:
    def __init__(self,d):
        self.root= [[],[],0]
        self.bits = [2**i for i in range(d)]
        self.bits.reverse()
    def insert(self, x):
        node = self.root
        for b in self.bits:
            i = bool(x & b)
            if node[i]:
                node[2] += 1
            else:
                node[i] = [[],[],1]
            node = node[i]
    def delete(self, x):
        node = self.root
        for b in self.bits:
            node[2] -= 1
            i = bool(x & b)
            if node[2] == 0:
                node[i],node = [],node[i] # keep order
            else:
                node = node[i]
    def minimum(self): # must include one value
        node = self.root
        res = 0
        for b in self.bits:
            if not node:
                return None
            if node[0]:
                node = node[0]
            else:
                res += b
                node = node[1]
        return res
    def findGreaterThan(self, k):
        node = self.root
        res = 0
        for b in self.bits:
            if not node:
                return None
            i = bool(k & b)
            if i == 0 and node[i]:
                node = node[i]
            else:
                node = node[1]
                res += b
        return res

    def dprint(self,node):
        print(bool(node[0]),bool(node[1]),node[2])

def test():
    bt = BinaryTrie(4)
    bt.insert(2)
    bt.insert(3)
    bt.insert(7)
    bt.delete(2)
    print(bt.minimum())
    print(bt.findGreaterThan(9))
    pass

def perf():
    import random
    from time import perf_counter as time
    N = 10**5
    K = 2**32-1
    samples = [random.randint(0,K) for _ in range(N)]
    bt = BinaryTrie(32)
    start=time()
    for s in samples:
        bt.insert(s)
    print(f"{time()-start}") 

if __name__=='__main__':
    test()
    perf()
