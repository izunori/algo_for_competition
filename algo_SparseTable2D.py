from itertools import product
class SparseTable2D:
    def __init__(self,data,op):
        H = len(data)
        W = len(data[0])
        N = H*W
        self.H,self.W,self.N = H,W,N
        self.op = op
        self.nrows = H.bit_length()
        self.ncols = W.bit_length()
        self.pow = [2**p for p in range(max(self.nrows,self.ncols))]
        self.table = [0]*(self.H*self.W*self.nrows*self.ncols)
        for row in range(self.nrows):
            off = N * (self.ncols if row else 1)
            for col in range(self.ncols):
                if row == col == 0:
                    for x,y in product(range(H),range(W)):
                        self.table[y+W*x] = data[x][y]
                    continue
                i = N*(col+self.ncols*row)
                for x in range(H):
                    for y in range(W):
                        j = y + W*x
                        if row == 0:
                            nj = min(y+self.pow[col-1],W-1) + W*x
                        else:
                            nj = y + W * min(x+self.pow[row-1],H-1)
                        self.table[i+j] = op(self.table[i+j-off], self.table[i+nj-off])
    def get(self,lx,ly,rx,ry):
        px = (rx-lx).bit_length()-1
        py = (ry-ly).bit_length()-1
        pos = self.N * (px*self.ncols + py)
        wx = self.pow[px] # 2**p
        wy = self.pow[py] # 2**p
        t1 = self.op(self.table[pos+lx*self.W+ly],self.table[pos+lx*self.W+(ry-wy)])
        t2 = self.op(self.table[pos+(rx-wx)*self.W+ly],self.table[pos+(rx-wx)*self.W+(ry-wy)])
        return self.op(t1,t2)

def test():
    from time import perf_counter as time
    import random
    H = 5
    W = 4
    data = [[random.randint(0,10) for i in range(W)] for _ in range(H)]
    #[print(row) for row in data]
    spt = SparseTable2D(data,min)
    for lx in range(H):
        for ly in range(W):
            for rx in range(lx+1,H+1):
                for ry in range(ly+1,W+1):
                    mn = 100
                    for x,y in product(range(lx,rx),range(ly,ry)):
                        mn = min(data[x][y],mn)
                    res = spt.get(lx,ly,rx,ry)
                    if mn != res:
                        print('NG')
                        print(lx,ly,rx,ry)
                        print("expected:",mn)
                        print("actual:",res)
                        return
    print('OK')

def perf():
    from time import perf_counter as time
    import random
    H = 300
    W = 300
    random.seed(0)
    data = [[random.randint(0,10) for i in range(W)] for _ in range(H)]
    start = time()
    spt = SparseTable2D(data,min)
    print(f"{time()-start}") 

if __name__=='__main__':
    test()
    perf()
