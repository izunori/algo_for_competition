import array as ar
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
            self.B.append(ar.array('b',((t&th)==th for t in self.T)))
            L,R = [],[]
            for t,b in zip(self.T, self.B[-1]):
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
    # return data[i]
    def access(self, i):
        res = 0
        th = 1 << self.l
        for c0, row in zip(self.cnt0,self.B):
            if row[i]:
                res += th
                i = c0 + self._rank(row, i+1, 1) - 1
            else:
                i = self._rank(row, i+1, 0) - 1 
            th >>= 1
        return res

    def _rank(self, row, i, x):
        return row[:i].count(x)
    def _select(self, row, i, x):
        cnt = 0
        for res, r in enumerate(row):
            if r == x:
                if cnt == i:
                    return res
                cnt += 1
    # count x in data[:i]
    def rank(self, i, x):
        i -= 1
        th = 1 << self.l
        for c0, row in zip(self.cnt0,self.B):
            if th&x:
                i = c0 + self._rank(row, i+1, 1) - 1
            else:
                i = self._rank(row, i+1, 0) - 1
            th >>= 1
        return i-self.index[x]+1
    # find i-th x (0-index)
    def select(self, i, x):
        i = self.index[x] + i
        th = 1
        for c0, row in zip(self.cnt0[::-1],self.B[::-1]):
            if x&th:
                i = self._select(row, i-c0, 1)
            else:
                i = self._select(row, i, 0)
            th <<= 1
        return i
    def quantile(self, l, r, i):
        th = 1 << self.l
        for c0, row in zip(self.cnt0,self.B):
            n0 = self._rank(row,r,0) - self._rank(row,l,0)
            n1 = self._rank(row,r,1) - self._rank(row,l,1)
            if n0 <= i:
                i -= n0
                l = c0+self._rank(row,l,1)
                r = c0+self._rank(row,r,1)
            else:
                l = self._rank(row,l,0)
                r = self._rank(row,r,0)
            th >>= 1
        return self.T[r-1]


if __name__=='__main__':
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

