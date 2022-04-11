class TreapTuple:
    # (key, priority, lch, rch)
    def __init__(self):
        self.root = None
    def merge(self, a, b):
        if a is None or b is None:
            return a if b is None else b
        if a[1] > b[1]:
            a[3] = self.merge(a[3],b)
            return self.update(a)
        else:
            b[2] = self.merge(a,b[2])
            return self.update(b)
    def update(self, t):
        t[4] = (t[3][4] if t[3] else 0) + (t[2][4] if t[2] else 0) + 1
        t[5] = (t[3][5] if t[3] else 0) + (t[2][5] if t[2] else 0) + t[0]
        return t
    def split(self, t, k):
        if t is None:
            return (None, None)
        if k <= t[0]:
            s = self.split(t[2], k)
            t[2] = s[1]
            return s[0], t
        else:
            s = self.split(t[3], k)
            t[3] = s[0]
            return t, s[1]
    def insert(self, k):
        lt, rt = self.split(self.root, k)
        node = [k, random.random(), None, None, 1, k]
        self.root = self.merge(self.merge(lt, node), rt)
        return self
    def remove(self, k):
        lt,rt = self.split(self.root, k)
        _,rt = self.split(rt, k+1)
        self.root = self.merge(lt, rt)

    def show(self):
        from collections import deque
        if self.root is None:
            print(None)
        dq = deque([self.root])
        while dq:
            t = dq.popleft()
            vs = []
            if t[2]:
                dq.append(t[2])
                vs.append(t[2][0])
            else:
                vs.append(None)
            if t[3]:
                dq.append(t[3])
                vs.append(t[3][0])
            else:
                vs.append(None)
            print(t[0],"->",vs)
    def search(self, k):
        t = self.root
        while True:
            if t is None:
                return False
            if t[0] == k:
                return True
            t = t[3] if t[0] < k else t[2]

import random
class TreapRecursive:
    class Node:
        def __init__(self, key):
            self.l, self.r = None, None
            self.key = key
            self.pri = random.random()
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
            l,t.l = self.split(t.l, k)
            return (l, t)
        else:
            t.r,r = self.split(t.r, k)
            return t, r
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
            t = t.r if t.key < k else t.l
    def findEqualOrGreaterThan(self, x):
        t = self.root
        res = None
        while True:
            if t is None:
                return res
            if x <= t.key:
                res = t.key
                t = t.l
            else:
                t = t.r
    def findEqualOrLessThan(self, x):
        t = self.root
        res = None
        while True:
            if t is None:
                return res
            if t.key <= x:
                res = t.key
                t = t.r
            else:
                t = t.l

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
    def split(self, t, k):
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
    trp.show()
    print(trp.findEqualOrGreaterThan(4),5)
    print(trp.findEqualOrGreaterThan(5),5)
    print(trp.findEqualOrGreaterThan(6),40)
    print(trp.findEqualOrGreaterThan(39),40)
    print(trp.findEqualOrGreaterThan(40),40)
    print(trp.findEqualOrGreaterThan(41),None)
    print(trp.findEqualOrLessThan(39),5)
    print(trp.findEqualOrLessThan(40),40)
    print(trp.findEqualOrLessThan(41),40)

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

if __name__=='__main__':
    test()
    perf()
