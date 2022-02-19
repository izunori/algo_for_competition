from collections import defaultdict
class SmallestPrimeFactor:
    def __init__(self, n):
        self.n = n
        self.spf = [1]*(n+1)
        for i in range(2,n+1):
            if self.spf[i] != 1:
                continue
            for j in range(i,n+1,i):
                if self.spf[j] == 1:
                    self.spf[j] = i
    def factor(self,n):
        res = defaultdict(int)
        while self.spf[n] != 1:
            d = self.spf[n]
            res[d] += 1
            n //= d
        if n != 1:
            res[n] += 1
        return res
    def getPrimes(self):
        return [p for i,p in enumerate(self.spf[2:],2) if i == p]

def test():
    spf = SmallestPrimeFactor(10**3)
    print(spf.factor(2*3*11))
    print(spf.getPrimes())

if __name__=='__main__':
    test()

