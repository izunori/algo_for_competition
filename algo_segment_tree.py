from collections import defaultdict, deque
# Segment Tree
class SegmentTree:
    def __init__(self,data,op,default):
        N = len(data)
        self.N = N
        self.op = op
        self.default = default
        self.l = 2**((N-1).bit_length())
        self.data = [default]*self.l + data + [default]*(self.l-N)
        for i in range(self.l-1,0,-1):
            self.data[i] = op(self.data[2*i], self.data[2*i+1])
    def set(self,i,val):
        i += self.l
        self.data[i] = val
        i = i//2
        while i > 0:
            self.data[i] = self.op(self.data[2*i], self.data[2*i+1])
            i = i//2
    def get(self,i,j):
        i += self.l
        j += self.l
        s = self.default 
        while j-i > 0:
            if i & 1:
                s = self.op(s,self.data[i])
                i += 1
            if j & 1:
                s = self.op(s,self.data[j-1])
                j -= 1
            i, j = i//2, j//2
        return s
    

    # under construction
    def findMinimumLessThan(self,l,r,f):
        v = self.default
        j = r+self.l
        fail = False
        while j > 0:
            if f(self.op(v,self.data[j-1])):
                if j & 1:
                    v = self.op(self.data[j-1],v)
                    j -= 1
                else:
                    if not fail:
                        j //= 2
                    else:
                        v = self.op(self.data[j-1],v)
                        j -= 1
            else:
                if self.l < j:
                    return max(l,j - self.l)
                fail = True
                j *= 2
                if j == self.L:
                    return max(l,0)
        return l


    def get_data(self, i=None):
        if i is None:
            return self.data[self.l:self.l + self.N]
        else:
            return self.data[self.l+i]


    ## extra
    def get_recur(self,i,j):
        def g(self,i,j,k,s,t):
            if t <= i or j <= s: # out of range
                return self.default # unit element
            if i <= s and t <= j: # has intersection
                return self.data[k]
            # left + right
            return self.op(g(self,i,j,2*k,s,(s+t)//2),g(self,i,j,2*k+1,(s+t)//2,t))
        return g(self,i,j,1,0,self.l)

def test():
    data = list(range(8))
    seg = SegmentTree(data, lambda x,y:x+y, 0)
    seg.set(0,10)
    seg.set(7,-1)
    print(seg.get(0,1),10) # 10
    print(seg.get(5,8),10) # 5+6-1
    print(seg.get(0,8),30) # 10+1+2+3+4+5+6-1
    print(seg.get_recur(0,8),30) # 10+1+2+3+4+5+6-1

def test2():
    data = list(range(6))
    seg = SegmentTree(data, min, 10**18)
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 0))
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 1))
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 2))
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 3))
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 4))
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 5))
    print(seg.findMinimumLessThan(2,6,lambda x : x >= 6))

def perf():
    import random
    from time import perf_counter as time
    N,M = 2*10**5, 2*10**5
    samples = [random.randint(0,10) for i in range(M)]
    indexes = [random.randint(0,N-1) for i in range(M)]
    data = [0]*N
    seg = SegmentTree(data, lambda x,y:x+y, 0)
    start=time()
    for i,s in zip(indexes, samples):
        seg.set(i,s)
    print(f"{time()-start}") 
    

if __name__ == '__main__':
    perf()
