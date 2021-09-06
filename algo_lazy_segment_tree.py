# op : main operator
# eval_ : given opration to interval
# lazy_op : parameters use in eval_ (this value is delaed with eval_)
# lazy_up : 
# input_down : 
# lazy_default: default_value of eval_ ( maybe None)
class LazySegmentTree:
    def __init__(self,data,op,default,eval_,lazy_op,lazy_default,lazy_up=None,input_down=None):
        N = len(data)
        self.N = N
        self.op = op
        self.default = default
        self.eval_ = eval_
        self.lazy_op = lazy_op
        id_ = lambda x : x
        self.lazy_up = id_ if lazy_up is None else lazy_up
        self.input_down = id_ if input_down is None else input_down
        self.lazy_default = lazy_default
        self.L = 2**((N-1).bit_length())
        self.data = [default]*self.L + data + [default]*(self.L-N)
        self.lazy = [lazy_default for i in range(self.L * 2)]
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

    def get(self,i,j):
        i += self.L
        j += self.L
        ti = i // (i & -i)
        tj = j // (j & -j)
        upper = self.upper(ti,tj-1)
        l,r = self.default, self.default
        for u in upper[::-1]:
            self.update(u)
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


if __name__ == '__main__':
    #test()
    test2()


