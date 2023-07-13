from algo_BinaryIndexedTree import BinaryIndexedTree
import bisect

# multiset
class BinarySearchTree(BinaryIndexedTree):
    def __init__(self, max_size=10**6):
        self.max_size = max_size
        super().__init__([0]*max_size, lambda x,y : x+y, 0)
    def insert(self, x):
        self.add(x, 1)
    def find(self, x):
        return self.get(x+1) - self.get(x)
    def erase(self, x):
        self.add(x, -1)
    def count(self):
        return self.get(self.max_size)
    def findLessOrEqualThan(self, t):
        s = self.get(t) # num of <= t
        if s == 0:
            return None
        L,R = -1, t 
        while R-L>1:
            x = (R+L)//2
            L,R = (L,x) if s == self.get(x) else (x,R)
        return R 
    def findGreaterOrEqualThan(self, t):
        s = self.get(t) # num of < t
        if s == self.get(self.max_size):
            return None
        L,R = t, self.max_size
        while R-L>1:
            x = (L+R)//2
            L,R = (x,R) if s == self.get(x) else (L,x)
        return R

class ForTest:
    def __init__(self):
        self.data = []
    def insert(self, x):
        bisect.insort(self.data, x)
    def erase(self,x):
        self.data.remove(x)
    def find(self,x):
        return self.data.count(x)
    def findLessOrEqualThan(self,t):
        for x in self.data[::-1]:
            if x <= t:
                return x
        return None
    def findGreaterOrEqualThan(self,t):
        for x in self.data:
            if t <= x:
                return x
        return None

def test():
    import random
    N = 10**3
    K = 10000
    M = 100
    for _ in range(N):
        samples = [random.randint(0,K) for _ in range(M)]
        queries = [random.randint(0,K) for _ in range(M)]
        t0 = ForTest()
        t1 = BinarySearchTree(K+1)
        for s,q in zip(samples, queries):
            t0.insert(s)
            t1.insert(s)
            if t0.find(q) != t1.find(q):
                print(t0.find(q),t1.find(q))
                print("ERROR")
                exit()
            if t0.findLessOrEqualThan(q) != t1.findLessOrEqualThan(q):
                print(t0.find(q),t1.find(q))
                print("ERROR")
                exit()
            if t0.findGreaterOrEqualThan(q) != t1.findGreaterOrEqualThan(q):
                print(t0.find(q),t1.find(q))
                print("ERROR")
                exit()
        for s,q in zip(samples, queries):
            t0.erase(s)
            t1.erase(s)
            if t0.find(q) != t1.find(q):
                print(t0.find(q),t1.find(q))
                print("ERROR")
                exit()
            if t0.findLessThan(q) != t1.findLessThan(q):
                print(t0.find(q),t1.find(q))
                print("ERROR")
                exit()
            if t0.findGreaterThan(q) != t1.findGreaterThan(q):
                print(t0.find(q),t1.find(q))
                print("ERROR")
                exit()


if __name__=='__main__':
    test()

    
