# op : main operator
# eval_ : given opration to interval
# lazy_op : parameters use in eval_ (this value is delaed with eval_)
# lazy_up : 
# input_down : 
# lazy_default: default_value of eval_ ( maybe None)
class LazySegmentTree:
    def __init__(self,data,op,default,eval_,lazy_op,lazy_default,lazy_up,input_down):
        N = len(data)
        self.N = N
        self.op = op
        self.default = default
        self.eval_ = eval_
        self.lazy_op = lazy_op
        self.lazy_up = lazy_up
        self.input_down = input_down
        self.lazy_default = lazy_default
        self.L = 2**((N-1).bit_length())
        self.data = [default]*self.L + data + [default]*(self.L-N)
        self.lazy = [lazy_default for i in range(self.L * 2)]
        self.updated = [0]*self.L*2
        self.history = []
        for i in range(self.L-1,0,-1):
            self.data[i] = op(self.data[2*i], self.data[2*i+1])
    def upper(self,l,r):
        l,r = l>>1, r>>1
        res = []
        while l != r:
            if l < r:
                res.append(r)
                r >>= 1
            else:
                res.append(l)
                l >>= 1
        while l:
            res.append(l)
            l >>= 1
        return res
    def update(self,u):
        if not self.lazy[u] == self.lazy_default:
            if u < self.L:
                up = self.lazy_up(self.lazy[u])
                self.lazy[2*u] = self.lazy_op(up, self.lazy[2*u])
                self.lazy[2*u+1] = self.lazy_op(up, self.lazy[2*u+1])
            self.data[u] = self.eval_(self.lazy[u], self.data[u])
            self.lazy[u] = self.lazy_default
    def set(self,i,j,f):
        i += self.L
        j += self.L
        ti = i // (i & -i)
        tj = j // (j & -j)
        while self.history:
            self.updated[self.history.pop()] = 0
        upper = self.upper(ti,tj-1)
        for u in upper[::-1]:
            if not self.lazy[u] == self.lazy_default:
                up = self.lazy_up(self.lazy[u])
                self.lazy[2*u] = self.lazy_op(up, self.lazy[2*u])
                self.lazy[2*u+1] = self.lazy_op(up, self.lazy[2*u+1])
                self.lazy[u] = self.lazy_default
        while j-i > 0:
            if i & 1:
                self.lazy[i] = self.lazy_op(f, self.lazy[i])
                i += 1
            if j & 1:
                self.lazy[j-1] = self.lazy_op(f, self.lazy[j-1])
                j -= 1
            i, j = i>>1, j>>1
            f = self.input_down(f)
        for u in upper:
            self.update(2*u)
            self.update(2*u+1)
            self.data[u] = self.op(self.data[2*u], self.data[2*u+1])
    def update_uppers(self,p):
        uppers = []
        while self.updated[p] == 0 and p > 0:
            uppers.append(p)
            p >>= 1
        while uppers:
            u = uppers.pop()
            self.update(u)
            self.updated[u] = 1
            self.history.append(u)
    def get(self,i,j):
        i += self.L
        j += self.L
        self.update_uppers(i)
        self.update_uppers(j-1)
        l,r = self.default, self.default
        while j-i > 0:
            if i & 1:
                self.update(i)
                l = self.op(l, self.data[i])
                i += 1
            if j & 1:
                self.update(j-1)
                r = self.op(self.data[j-1], r)
                j -= 1
            i, j = i>>1, j>>1
        return self.op(l,r)

    # under construction
    def findMinimumLessThan(self,l,r,f):
        v = self.default
        j = r+self.L
        upper = self.upper(l,r)
        for u in upper[::-1]:
            self.update(u)
        fail = False
        while j > 0:
            self.update(j-1)
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
                if self.L < j:
                    return max(l,j - self.L)
                fail = True
                j *= 2
                if j == self.L:
                    return max(l,0)
        return l

    def findMaximumLessOrEqualThan(self,l,r,f):
        v = self.default
        i = l + self.L
        upper = self.upper(l,r)
        for u in upper[::-1]:
            self.update(u)
        fail = False
        while i > 0:
            self.update(i)
            if f(self.op(v,self.data[i])):
                if i & 1:
                    v = self.op(self.data[i],v)
                    i += 1
                else:
                    if not fail:
                        i //= 2
                    else:
                        v = self.op(self.data[i],v)
                        i += 1
            else:
                if self.L <= i:
                    return min(r, i-self.L)
                fail = True
                i *= 2
        return r


def test():
    data = [1]*16
    seg = LazySegmentTree(data, max, 0, lambda x,p : p, lambda p,q : q, None)
    print(seg.data)
    seg.set(0, 4, 10)
    print(seg.data)
    print("CHEK")
    print(seg.get(0, 1))
    print(seg.get(2, 3))
    print(seg.lazy)
    print(seg.data)

def test2():
    from itertools import combinations
    from random import choice
    from random import randint as ri
    from operator import add
    N = 10
    M = 10
    samples = [(choice(list(combinations(range(0,N+1),r=2))),ri(-M,M)) for i in range(M)]
    data = [0]*N
    for (l,r),v in samples:
        for x in range(l,r):
            data[x] += v
    seg = LazySegmentTree([0]*N, add, 0, add, add, 0, lambda x:x//2, lambda x:x*2)
    for (l,r),v in samples:
        seg.set(l,r,v)

    samples = [choice(list(combinations(range(0,N+1),r=2))) for i in range(M)]
    for l,r in samples:
        print(sum(data[l:r]), seg.get(l,r))

def test3():
    from itertools import combinations
    from random import choice
    from random import randint as ri
    from operator import add
    N = 10
    M = 10
    add = lambda x,y : x+y
    put = lambda x,y : x
    seg = LazySegmentTree([0]*N, add, 0, put, put, 0, lambda x: x//2, lambda x:x*2)

    samples = [(choice(list(combinations(range(0,N+1),r=2))),ri(-M,M)) for i in range(M)]
    data = [0]*N
    for (l,r),v in samples:
        for x in range(l,r):
            data[x] = v
    for (l,r),v in samples:
        seg.set(l,r,v)

    samples = [choice(list(combinations(range(0,N+1),r=2))) for i in range(M)]
    for l,r in samples:
        print(sum(data[l:r]), seg.get(l,r))

def test4():
    from itertools import combinations
    from random import choice
    from random import randint as ri
    from operator import add
    N = 8
    M = 8
    add = lambda x,y : x+y
    seg = LazySegmentTree([0]*N, add, 0, add, add, 0, lambda x: x//2, lambda x:x*2)

    for i in range(6):
        seg.set(0,i+1,1)
    seg.set(6,7,100)
    seg.set(7,8,1000)
    print(seg.findMinimumLessThan(0,8,lambda x : x < 1001))
    print(seg.findMinimumLessThan(0,8,lambda x : x < 1122))
    print(    [seg.get(i,i+1) for i in range(8)])



if __name__ == '__main__':
    #test()
    test2()
    #est4()



