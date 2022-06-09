class BinaryTrie:
    def __init__(self,d):
        self.root= [[],[],0]
        self.bits = [2**i for i in range(d)]
        self.bits.reverse()
    def insert(self, x):
        node = self.root
        node[2] += 1
        for b in self.bits:
            i = bool(x & b)
            if node[i]:
                node[i][2] += 1
            else:
                node[i] = [[],[],1]
            node = node[i]
    def delete(self, x):
        node = self.root
        node[2] -= 1
        for b in self.bits:
            i = bool(x & b)
            if not node[i]:
                return False
            node[i][2] -= 1
            if node[i][2] == 0:
                node[i],node = [],node[i] # keep order
            else:
                node = node[i]
    def findIndex(self, x):
        node = self.root
        index = 0
        for b in self.bits:
            i = bool(x & b)
            if node[i]:
                if i == 1 and node[0]:
                    index += node[0][2]
                node = node[i]
            else:
                if i == 1 and node[0]:
                    index += node[0][2]
                return index, 0
        return index, node[2]
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
    def kthMinimum(self, k): # 0-index
        node = self.root
        k += 1
        res = 0
        for b in self.bits:
            if not node or node[2] < k:
                return None
            if node[0] and k <= node[0][2]:
                node = node[0]
            else:
                res += b
                if node[0]:
                    k -= node[0][2]
                node = node[1]
        return res
    def findGeq(self, k):
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
        print(node[0][2],node[1][2],node[2])

def test():
    import random
    import bisect
    bt = BinaryTrie(4)
    bt.insert(2)
    bt.insert(3)
    bt.insert(10)
    bt.insert(7)
    bt.delete(2)
    print(bt.minimum())
    print(bt.findIndex(2))
    print(bt.kthMinimum(1))
    print(bt.findGeq(9))

    N = 100
    M = 20
    D = 10
    K = 2**D-1
    samples = [random.randint(0,K) for _ in range(N)]
    toBeDeleted = random.sample(samples, k=M)
    ans = sorted(samples)
    for x in toBeDeleted:
        ans.remove(x)
    print(ans)

    bt = BinaryTrie(D)
    for x in samples:
        bt.insert(x)
    for x in toBeDeleted:
        bt.delete(x)

    # find
    for x in range(K):
        index = bisect.bisect_left(ans, x)
        if (index, ans.count(x)) != bt.findIndex(x):
            print(x,index, ans.count(x), bt.findIndex(x))
            print('NG in findIndex')
            break
    else:
        print('OK in findIndex')

    # kthMinimum
    for i in range(len(ans)):
        if bt.kthMinimum(i) != ans[i]:
            print('NG in kthMinimum')
    else:
        print('OK in kthMinimum')
    
    # findGeq
    for x in range(K):
        for a in ans:
            if x < a:
                break
        else:
            a = None
        if bt.findGeq(x) == a:
            print(x,bt.findGeq(x), x)
            print('NG in findGeq')
            break
    else:
        print('OK in findGeq')


def perf():
    import random
    from time import perf_counter as time
    N = 10**5
    D = 32
    K = 2**D-1
    samples = [random.randint(0,K) for _ in range(N)]
    bt = BinaryTrie(D)
    start=time()
    for s in samples:
        bt.insert(s)
    print(f"{time()-start}") 

if __name__=='__main__':
    test()
    perf()
