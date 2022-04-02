class Treap:
    # (key, priority, lch, rch)
    def __init__(self):
        pass
    def getPriority(self):
        import random
        return random.random()
    def merge(self,l,r):
        if l is None or r is None:
            return l if r is None else r
        if l[1] > r[1]:
            l[2] = self.merge(l[2],r)
            return l
        else:
            r[3] = self.merge(l,r[3])
            return r
    def split(self,t,k):
        if t is None:
            return (None,None)
        if t[0] <= k:
            r = t[3]
            return (t, self.split((t[3],k,r,b)))
        else:
            b = t
            return (self.split(t[2],k,a,b[2], t))

import random
class Treap2:
    class Node:
        def __init__(self, key):
            self.l, self.r = None, None
            self.key = key
            self.pri = random.random()
            self.cnt = 1
            self.sum = key
        def __str__(self):
            return f"{str(self.key)}->({self.l},{self.r})"
    def __init__(self):
        self.root = None
    def update(self, t):
        t.cnt = (t.r.cnt if t.r else 0) + (t.l.cnt if t.l else 0) + 1
        t.sum = (t.r.sum if t.r else 0) + (t.l.sum if t.l else 0) + t.key
        return t
    def merge(self, a, b):
        if a is None or b is None:
            return a if b is None else b
        if a.pri > b.pri:
            a.r = self.merge(a.r, b)
            return self.update(a)
        else:
            b.l = self.merge(a, b.l)
            return self.update(b)
    def split(self, t, k):
        if t is None:
            return (None, None)
        if k <= t.key:
            s = self.split(t.l, k)
            t.l = s[1]
            return (s[0], t)
        else:
            s = self.split(t.r, k)
            t.r = s[0]
            return t, s[1]
    def insert(self, k):
        if self.root is None:
            self.root = self.Node(k)
            return self
        lt, rt = self.split(self.root, k)
        self.root = self.merge(self.merge(lt, self.Node(k)), rt)
        return self
    def remove(self, k):
        if self.root is None:
            return
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
            t = t.r if t.key < k else t.l

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
    trp = Treap2()
    trp.insert(5)
    trp.insert(10)
    trp.insert(20)
    trp.insert(40)
    trp.insert(-10)
    trp.remove(20)
    trp.remove(10)
    trp.show()

def perf():
    print("---PERF")
    import random
    from time import perf_counter as time
    K = 10**9
    N = 2*10**4
    samples = [random.randint(-K,K) for _ in  range(N)]

    trp = Treap2()

    start = time()
    for s in samples:
        trp.insert(s)
    print(f"{time() - start}")

    start = time()
    for s in samples:
        trp.search(s)
    print(f"{time() - start}")

    print(trp.root.cnt)
    print(trp.root.l.cnt)
    print(trp.root.r.cnt)

if __name__=='__main__':
    test()
    perf()
