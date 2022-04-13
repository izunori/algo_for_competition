import random

## omake
y = 2463534242
def xorShift():
    global y
    y = y ^ ((y << 13) & 0xffffffff)
    y = y ^ ((y >> 17) & 0xffffffff)
    y = y ^ ((y << 5) & 0xffffffff)
    return y

class Treap:
    class Node:
        __slots__ = ['l','r','key','pri','cnt','sum','depth']
        def __init__(self, key):
            self.l, self.r = None, None
            self.key = key
            self.pri = xorShift()
            self.cnt = 1
            self.sum = key
            self.depth = 0
        def __str__(self):
            return f"{str(self.key)}->({self.l},{self.r})"
    def __init__(self, t = None):
        self.root = t
    def update(self, t):
        t.cnt = (t.r.cnt if t.r else 0) + (t.l.cnt if t.l else 0) + 1
        t.sum = (t.r.sum if t.r else 0) + (t.l.sum if t.l else 0) + t.key
        t.depth = max((t.r.depth if t.r else 0), (t.l.depth if t.l else 0))+1
        return t
    def merge(self, a, b):
        pairs = []
        while not (a is None or b is None):
            if a.pri > b.pri:
                pairs.append((True,a))
                a,b = a.r, b
            else:
                pairs.append((False,b))
                a,b = a, b.l
        t = a if b is None else b
        while pairs:
            is_a,x = pairs.pop()
            self.update(t)
            if is_a:
                x.r,t = t,x
            else:
                x.l,t = t,x
        return self.update(t)
    def split(self, t, k): # (:k)[k:)
        pairs = []
        while t is not None:
            if k <= t.key:
                pairs.append((True,t))
                t = t.l
            else:
                pairs.append((False,t))
                t = t.r
        s = (None, None)
        while pairs:
            is_l,t = pairs.pop()
            if is_l:
                l,t.l = s
                s = (l,t)
            else:
                t.r,r = s
                s = (t,r)
        return s
    def insert(self, k):
        lt, rt = self.split(self.root, k)
        self.root = self.merge(self.merge(lt, self.Node(k)), rt)
        return self
    def remove(self, k):
        lt,rt = self.split(self.root, k)
        _,rt = self.split(rt, k+1)
        self.root = self.merge(lt, rt)
    def search(self, k):
        t = self.root
        while True:
            if t is None:
                return False
            if t.key == k:
                return True
            t = (t.r if t.key < k else t.l)
    def findEqualOrGreaterThan(self, x):
        t = self.root
        res = None
        while t is not None:
            if x <= t.key:
                res = t.key
                t = t.l
            else:
                t = t.r
        return res
    def findEqualOrLessThan(self, x):
        t = self.root
        res = None
        while t is not None:
            if t.key <= x:
                res = t.key
                t = t.r
            else:
                t = t.l
        return res
    def findGreaterKth(self,x,k):
        _,rt = self.split(self.root, k)
        c = 0
        nk = k
        while c < k:
            lt,rt = self.split(rt,nk+1)
            if rt is None:
                return None
            if lt is not None:
                c += lt.cnt
            nk += 1
        return nk-1
    def findKthSmallest(self,k,than=None): # 0-index
        if than is None:
            x = self.root
        else:
            lt,rt = self.split(self.root, than)
            x = rt
        st = [(x,0)]
        while st and k >= 0:
            x,s = st.pop()
            if x is None:
                continue
            if s == 0:
                st.append((x,1))
                st.append((x.l,0))
            elif s == 1:
                k -= 1
                st.append((x,2))
                st.append((x.r,0))
        if than:
            self.root = self.merge(lt,rt)
        if not st:
            return None
        return x.key

    # for debug
    def findKthSmallestRecursive(self,k):
        self.k = k
        t = self._findKthSmallestRecursive(self.root)
        return t.key if t else None
    def _findKthSmallestRecursive(self,x):
        if x is None:
            return None
        left = self._findKthSmallestRecursive(x.l)
        if left is not None:
            return left
        self.k -= 1
        if self.k == 0:
            return x
        return self._findKthSmallestRecursive(x.r)
    def show(self):
        from collections import deque
        if self.root is None:
            print(None)
        dq = deque([self.root])
        while dq:
            t = dq.popleft()
            vs = []
            if t.l:
                dq.append(t.l)
                vs.append(t.l.key)
            else:
                vs.append(None)
            if t.r:
                dq.append(t.r)
                vs.append(t.r.key)
            else:
                vs.append(None)
            print(t.key,"->",vs)

def test():
    print("---TEST")
    trp = Treap()
    trp.insert(5)
    trp.insert(10)
    trp.insert(20)
    trp.insert(20)
    trp.insert(40)
    trp.insert(-10)
    trp.remove(20)
    trp.remove(10)
    trp.show() # -10,5,40
    print(trp.findEqualOrGreaterThan(4),5)
    print(trp.findEqualOrGreaterThan(5),5)
    print(trp.findEqualOrGreaterThan(6),40)
    print(trp.findEqualOrGreaterThan(39),40)
    print(trp.findEqualOrGreaterThan(40),40)
    print(trp.findEqualOrGreaterThan(41),None)
    print(trp.findEqualOrLessThan(39),5)
    print(trp.findEqualOrLessThan(40),40)
    print(trp.findEqualOrLessThan(41),40)
    print(trp.findKthSmallest(0),-10)
    print(trp.findKthSmallest(1,5),40)

def perf():
    print("---PERF")
    import random
    from time import perf_counter as time
    K = 10**9
    N = 2*10**5
    samples = [random.randint(-K,K) for _ in  range(N)]

    trp = Treap()

    start = time()
    for s in samples:
        trp.insert(s)
    print(f"{time() - start}")

    start = time()
    for s in samples:
        trp.search(s)
    print(f"{time() - start}")

    print(trp.root.cnt)
    print(trp.root.l.cnt,trp.root.r.cnt)
    print(trp.root.l.l.cnt,trp.root.l.r.cnt, trp.root.r.l.cnt,trp.root.r.r.cnt)

    print(trp.root.depth)
    print(trp.root.l.depth,trp.root.r.depth)
    print(trp.root.l.l.depth,trp.root.l.r.depth, trp.root.r.l.depth,trp.root.r.r.depth)

def testRandom():
    import random
    N = 100
    K = 100
    samples = [random.randint(-K,K) for i in range(N)]
    treap = Treap()
    for s in samples:
        treap.insert(s)
    samples.sort()
    for i,s in enumerate(samples):
        a = treap.findKthSmallestRecursive(i+1)
        b = treap.findKthSmallest(i)
        if len(set([a,b,s])) > 1:
            print("ERROR")

def testPerf():
    import random
    from time import perf_counter as time
    N = 2*10**5
    K = 10**9
    samples = [random.randint(-K,K) for i in range(N)]
    ks = [random.randint(1,10) for i in range(N)]
    treap = Treap()
    for s in samples:
        treap.insert(s)
    samples.sort()
    start = time()
    for k in ks:
        treap.findKthSmallestRecursive(k)
    print(f"{time() - start}")

    start = time()
    for k in ks:
        treap.findKthSmallest(k)
    print(f"{time() - start}")

if __name__=='__main__':
    #testRandom()
    #testPerf()
    test()
    #perf()
