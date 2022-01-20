class SparseTable:
    def __init__(self,data,op):
        N = len(data)
        self.N = N
        self.op = op
        self.nrows = N.bit_length()
        self.pow = [2**p for p in range(self.nrows)]
        self.table = [0]*(self.N*self.nrows)
        for i in range(N):
            self.table[i] = data[i]
        step = 1
        for row in range(1, self.nrows):
            l,r = N*(row-1), N*row-1
            for i in range(N):
                self.table[l+N+i] = op(self.table[l+i], self.table[min(l+i+step,r)])
            step *= 2
    def get(self,l,r):
        p = (r-l).bit_length()-1
        row = self.N * p
        w = self.pow[p] # 2**p
        return self.op(self.table[row+l],self.table[row+r-w])

def test():
    from time import perf_counter as time
    import random
    N = 100
    data = [random.randint(0,10**9) for i in range(N)]
    start = time()
    spt = SparseTable(data,min)
    for l in range(N):
        for r in range(l+1,N):
            x,y = (min(data[l:r]), spt.get(l,r))
            if x != y:
                print(x,y)


if __name__=='__main__':
    test()
