import array as ar
from itertools import accumulate
import math
class SimpleBitVector:
    def __init__(self, data):
        self.n = len(data)
        self.s = int(math.log(self.n))//2
        self.l = 4*self.s**2
        self.data = data
        self.ldata = []
        self.sdata = []
        cnt = 0
        scnt = 0
        for i,x in enumerate(self.data):
            if i % self.l == 0:
                scnt = 0
                self.ldata.append(cnt)
            if i % self.s == 0:
                self.sdata.append(scnt)
            if x == 1:
                cnt += 1
                scnt += 1
    def access(self, i):
        return self.data[i]
    def rank(self, i, x):
        p = self.s * (i//self.s)
        n1 = self.ldata[i//self.l] + self.sdata[i//self.s] + sum(self.data[p:i])
        return n1 if x == 1 else i-n1
    def select(self, i, x):
        # TODO
        return 0

class BitVector:
    def __init__(self, data):
        self.n = len(data)
        self.data = ar.array('b',data)
        self.cumsum = ar.array('i',[0] + list(accumulate(data)))
    def access(self, i):
        return self.data[i]
    def rank(self, i, x):
        return self.cumsum[i] if x else i - self.cumsum[i]
    def select(self, i, x):
        l,r = 0, self.n
        while r-l > 1:
            m = (r+l)//2
            n = self.cumsum[m] if x else m - self.cumsum[m]
            if n < i+1:
                l = m
            else:
                r = m
        return l
class WaveletMatrix:
    def __init__(self, data):
        self.T = data[:]
        self.N = len(data)
        max_value = max(data)
        self.l = max_value.bit_length()-1
        th = 1 << self.l
        self.B = []
        self.cnt0 = []
        while th:
            self.B.append(BitVector(ar.array('b',((t&th)==th for t in self.T))))
            L,R = [],[]
            for t,b in zip(self.T, self.B[-1].data):
                if b:
                    R.append(t)
                else:
                    L.append(t)
            self.cnt0.append(len(L))
            self.T = L+R
            th >>= 1
        self.index = {}
        for i,t in enumerate(self.T[::-1]):
            self.index[t] = self.N-i-1
    def access(self, i):
        res = 0
        th = 1 << self.l
        for c0, row in zip(self.cnt0,self.B):
            if row.access(i):
                res += th
                i = c0 + row.rank(i+1, 1) - 1
            else:
                i = row.rank(i+1, 0) - 1 
            th >>= 1
        return res
    # count x in data[:i]
    def rank(self, i, x):
        i -= 1
        th = 1 << self.l
        for c0, row in zip(self.cnt0, self.B):
            if th&x:
                i = c0 + row.rank(i+1, 1) - 1
            else:
                i = row.rank(i+1, 0) - 1
            th >>= 1
        return i-self.index[x]+1
    # find i-th x (0-index)
    def select(self, i, x):
        i = self.index[x] + i
        th = 1
        for c0, row in zip(self.cnt0[::-1],self.B[::-1]):
            if x&th:
                i = row.select(i-c0, 1)
            else:
                i = row.select(i, 0)
            th <<= 1
        return i
    # find i-th value in [l,r)
    def quantile(self, l, r, i):
        th = 1 << self.l
        for c0, row in zip(self.cnt0,self.B):
            n0 = row.rank(r,0) - row.rank(l,0)
            n1 = row.rank(r,1) - row.rank(l,1)
            if n0 <= i:
                i -= n0
                l = c0+row.rank(l,1)
                r = c0+row.rank(r,1)
            else:
                l = row.rank(l,0)
                r = row.rank(r,0)
            th >>= 1
        return self.T[r-1]

    # deprecated
    def _rank(self, row, i, x):
        return row.data[:i].count(x)
    def _select(self, row, i, x):
        cnt = 0
        for res, r in enumerate(row.data):
            if r == x:
                if cnt == i:
                    return res
                cnt += 1

def test():
    print("- Test WaveletMatrix")
    #       0,1,2,3,4,5,6,7,8,9,0,1
    data = [5,4,5,5,2,1,5,6,1,3,5,0]
    wm = WaveletMatrix(data)
    print(wm.access(5),1)
    print(wm.rank(9,1),2)
    print(wm.select(0,5),0)
    print(wm.select(1,5),2)
    print(wm.select(2,5),3)
    print(wm.select(3,5),6)
    print(wm.select(4,5),10)
    print(wm.select(0,3),9)
    print(wm.quantile(1,11,5),5)

def test2():
    print("- Test SimpleBitVector")
    #       0,1,2,3,4,5,6,7
    data = [1,1,0,0,1,1,1,0]
    #sbv = SimpleBitVector(data)
    sbv = BitVector(data)
    print(sbv.access(1),1)
    print(sbv.rank(5,0),2)
    print(sbv.rank(5,1),3)
    print(sbv.select(0,0),2)
    print(sbv.select(1,0),3)
    print(sbv.select(2,0),7)
    print(sbv.select(0,1),0)
    print(sbv.select(1,1),1)
    print(sbv.select(2,1),4)
    print(sbv.select(3,1),5)
    print(sbv.select(4,1),6)

def perf():
    print("- Test Performance")
    from time import perf_counter as time
    import random
    N = 2*10**5
    M = 10
    data = [random.randint(0,M) for _ in range(N)]
    wm = WaveletMatrix(data)
    start = time()
    wm.select(1000,1)
    print(f"{time()-start}s")

if __name__=='__main__':
    test()
    test2()
    perf()
