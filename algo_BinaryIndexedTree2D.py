from itertools import product
class BinaryIndexedTree2D:
    def __init__(self, H, W, op, default):
        self.H, self.W = H,W
        self.data = [[0]*(W+1) for _ in range(H+1)]
        self.op = op
        self.default = default
    def add(self,h,w,x):
        h,w = h+1,w+1
        while h <= self.H:
            nw = w
            while nw <= self.W:
                self.data[h][nw],nw = self.data[h][nw]+x, nw+(nw&-nw)
            h = h+(h&-h)
    def get(self,h,w):
        s = self.default
        while h > 0:
            nw = w
            while nw > 0:
                s,nw = self.op(s, self.data[h][nw]),nw-(nw&-nw)
            h = h-(h&-h)
        return s

def test():
    import random
    from operator import add
    H = 10
    W = 10
    N = 100
    hs = [random.randint(0,H-1) for _ in range(N)]
    ws = [random.randint(0,W-1) for _ in range(N)]
    xs = [random.randint(0,1000) for _ in range(N)]
    bit = BinaryIndexedTree2D(H,W,add,0)
    data = [[0]*W for _ in range(H)]
    for h,w,x in zip(hs,ws,xs):
        bit.add(h,w,x)
        data[h][w] += x
    for h,w in product(range(H),range(W)):
        h,w = h+1,w+1
        s2 = 0
        for nh,nw in product(range(h),range(w)):
            s2 += data[nh][nw]
        s1 = bit.get(h,w)
        if s1 != s2:
            print("NG")
            exit()
    print("OK")


if __name__=='__main__':
    test()
