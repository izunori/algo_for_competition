from collections import defaultdict, deque
class SegmentTree2D:
    def __init__(self,data,op,default):
        H = len(data)
        W = len(data[0])
        self.H = 2**(H-1).bit_length()
        self.W = 2**(W-1).bit_length()
        self.op = op
        self.default = default
        self.L = 4 * self.H * self.W
        self.data = [0]*self.L
        # right down
        W2 = self.W*2
        for x in range(H):
            for y in range(W):
                p = W2*(x+self.H)+(y+self.W)
                self.data[p] = data[x][y]
        # left down
        for x in range(self.H):
            for y in range(self.W-1,0,-1):
                p = W2*(x+self.H)
                self.data[p+y] = op(self.data[p+2*y], self.data[p+2*y+1])
        # right up
        for x in range(self.H-1,0,-1):
            for y in range(self.W):
                p = y+self.W
                self.data[p+W2*x] = op(self.data[p+W2*2*x], self.data[p+W2*(2*x+1)])
        # left up
        for x in range(self.H):
            for y in range(self.W-1,0,-1):
                p = W2*x
                self.data[p+y] = op(self.data[p+2*y], self.data[p+2*y+1])
    def set(self,x,y,val):
        x += self.H
        y += self.W
        W2 = self.W*2
        self.data[W2*x + y] = val
        # left down
        ny = y>>1
        p = W2*x
        while ny > 0:
            self.data[p+ny] = self.op(self.data[p+2*ny], self.data[p+2*ny+1])
            ny = ny>>1
        # right up
        nx = x>>1
        p = y
        while nx > 0:
            self.data[p+W2*nx] = self.op(self.data[p+W2*2*nx], self.data[p+W2*(2*nx+1)])
            nx = nx>>1
        # left up
        nx = x>>1
        ny = y>>1
        while nx > 0:
            nny = ny
            p = W2*nx
            while nny > 0:
                self.data[p+nny] = self.op(self.data[p+2*nny], self.data[p+2*nny+1])
                nny = nny>>1
            nx = nx>>1
    def get(self,x0,y0,x1,y1):
        x0 += self.H
        x1 += self.H
        y0 += self.W
        y1 += self.W
        s = self.default 
        W2 = self.W*2
        while x1-x0 > 0 and y1-y0 > 0:
            if x0 & x1 & 1:
                p0 = W2*x0
                p1 = W2*(x1-1)
                ty0,ty1 = y0,y1
                while ty1-ty0 > 0:
                    if ty0 & 1:
                        s = self.op(s, self.data[p0+ty0])
                        s = self.op(s, self.data[p1+ty0])
                        ty0 += 1
                    if ty1 & 1:
                        s = self.op(s, self.data[p0+ty1-1])
                        s = self.op(s, self.data[p1+ty1-1])
                    ty0, ty1 = ty0>>1, ty1>>1
            elif x0 & 1:
                p = W2*x0
                ty0,ty1 = y0,y1
                while ty1-ty0 > 0:
                    if ty0 & 1:
                        s = self.op(s, self.data[p+ty0])
                        ty0 += 1
                    if ty1 & 1:
                        s = self.op(s, self.data[p+ty1-1])
                    ty0, ty1 = ty0>>1, ty1>>1
            elif x1 & 1:
                p = W2*(x1-1)
                ty0,ty1 = y0,y1
                while ty1-ty0 > 0:
                    if ty0 & 1:
                        s = self.op(s, self.data[p+ty0])
                        ty0 += 1
                    if ty1 & 1:
                        s = self.op(s, self.data[p+ty1-1])
                    ty0, ty1 = ty0>>1, ty1>>1
            if y0 & y1 & 1 :
                tx0,tx1 = x0+(x0&1),x1-(x1&1)
                while tx1-tx0 > 0:
                    if tx0 & 1:
                        s = self.op(s, self.data[W2*tx0+y0])
                        s = self.op(s, self.data[W2*tx0+y1-1])
                        tx0 += 1
                    if tx1 & 1:
                        s = self.op(s, self.data[W2*(tx1-1)+y0])
                        s = self.op(s, self.data[W2*(tx1-1)+y1-1])
                    tx0, tx1 = tx0>>1, tx1>>1
            elif y0 & 1:
                tx0,tx1 = x0+(x0&1),x1-(x1&1)
                while tx1-tx0 > 0:
                    if tx0 & 1:
                        s = self.op(s, self.data[W2*tx0+y0])
                        tx0 += 1
                    if tx1 & 1:
                        s = self.op(s, self.data[W2*(tx1-1)+y0])
                    tx0, tx1 = tx0>>1, tx1>>1
            elif y1 & 1:
                tx0,tx1 = x0+(x0&1),x1-(x1&1)
                while tx1-tx0 > 0:
                    if tx0 & 1:
                        s = self.op(s, self.data[W2*tx0+y1-1])
                        tx0 += 1
                    if tx1 & 1:
                        s = self.op(s, self.data[W2*(tx1-1)+y1-1])
                    tx0, tx1 = tx0>>1, tx1>>1
            x0,y0,x1,y1 = x0+(x0&1),y0+(y0&1),x1-(x1&1),y1-(y1&1)
            x0,y0,x1,y1 = x0>>1,y0>>1,x1>>1,y1>>1
        return s
    def debug_print(self):
        print()
        p = 0
        for x in range(2*self.H):
            print(*[self.data[p+i] for i in range(2*self.W)])
            p += 2*self.W

def test():
    H = 2
    W = 4
    A = [[0]*W for i in range(H)]
    for i in range(H*W):
        y = i % W
        x = (i-y)//W
        A[x][y] = i+1
    add = lambda x,y:x+y
    seg = SegmentTree2D(A, add, 0)
    seg.debug_print()
    for x0 in range(H):
        for y0 in range(W):
            for x1 in range(x0,H+1):
                for y1 in range(y0,W+1):
                    ans = 0
                    for x in range(x0,x1):
                        for y in range(y0,y1):
                            ans += A[x][y]
                    res = ans == seg.get(x0,y0,x1,y1)
                    if not res:
                        print(x0,y0,x1,y1,ans,seg.get(x0,y0,x1,y1),res)

def perf():
    import random
    from time import perf_counter as time
    H = 100
    W = 100
    K = 10**9
    A = [[random.randint(0,K) for j in range(W)] for i in range(H)]
    add = lambda x,y:x+y
    seg = SegmentTree2D(A, add, 0)
    N = 2*10**5
    samples_set = [
            (random.randint(0,H), random.randint(0,W), random.randint(0,K))
            for i in range(N)
        ]
    start=time()
    for x,y,v in samples_set:
        seg.set(x,y,v)
    print(f"set : {time()-start}") 

    samples_get = [
            sorted([random.randint(0,H),random.randint(0,H)])
            + sorted([random.randint(0,W),random.randint(0,W)])
            for i in range(N)
            ]
    start=time()
    for x0,x1,y0,y1 in samples_get:
        seg.get(x0,y0,x1,y1)
    print(f"get : {time()-start}") 


if __name__=='__main__':
    test()
    perf()

