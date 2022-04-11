from algo_binary_indexed_tree import BinaryIndexedTree
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
    def findLessThan(self, t, equal=True):
        t -= (not equal)
        s = self.get(t+1) # num of <= t
        if s == 0:
            return None
        R,L = t, -1
        while R-L>1:
            x = (R+L)//2
            L,R = (L,x) if s == self.get(x+1) else (x,R)
        return R 
    def findGreaterThan(self, t, equal=True):
        t += (not equal)
        s = self.get(t) # num of < t
        if s == self.get(self.max_size):
            return None
        L,R = t-1, self.max_size
        while R-L>1:
            x = (L+R)//2
            L,R = (x,R) if s == self.get(x+1) else (L,x)
        return L+1

class BinarySearchTreeWithCompressedData(BinarySearchTree):
    def __init__(self, data):
        self.org_data = sorted(set(data))
        self.comp = {x:i for i,x in enumerate(self.org_data)}
        super().__init__(len(self.org_data))
    def insert(self, x):
        super().insert(self.comp[x])
    def erase(self, x):
        super().erase(self.comp[x])
    def find(self, x):
        if not x in self.comp:
            return 0
        return super().find(self.comp[x])
    def findLessThan(self, t, equal=True):
        if not t in self.comp:
            i = bisect.bisect_left(self.org_data, t) - 1
            equal = True
        else:
            i = self.comp[t]
        val = super().findLessThan(i, equal=equal)
        if val is not None:
            val = self.org_data[val]
        return val
    def findGreaterThan(self, t, equal=True):
        if not t in self.comp:
            i = bisect.bisect_left(self.org_data, t)
            equal = True
        else:
            i = self.comp[t]
        val = super().findGreaterThan(i, equal=equal)
        if val is not None:
            val = self.org_data[val]
        return val

class BinarySearchTree2:
    def __init__(self,max_size=10**6):
        self.max_size = max_size
        self.bit = BinaryIndexedTree([0]*max_size, lambda x,y:x+y, 0)
    def insert(self,x):
        # 0 <= x < max_size
        self.bit.add(x,1)
    def erase(self,x):
        self.bit.add(x,-1)
    def find(self,x):
        return self.bit.get(x) != self.bit.get(x+1)
    # return <=t
    def findEqualOrLessThan(self,t):
        s = self.bit.get(t+1) # num of <= t
        if s == 0:
            return None
        R,L = t, -1
        while R-L>1:
            x = (R+L)//2
            if s == self.bit.get(x+1):
                R = x
            else:
                L = x
        return R 
    # return t<=
    def findEqualOrGreaterThan(self,t):
        s = self.bit.get(t) # num of < t
        if s == self.bit.get(self.max_size):
            return None
        L,R = t-1, self.max_size
        while R-L>1:
            x = (L+R)//2
            if s == self.bit.get(x+1):
                L = x
            else:
                R = x
        return L+1

class ForTest:
    def __init__(self):
        self.data = []
    def insert(self, x):
        bisect.insort(self.data, x)
    def erase(self,x):
        self.data.remove(x)
    def find(self,x):
        return self.data.count(x)
    def findLessThan(self,t,equal=True):
        for x in self.data[::-1]:
            if (equal and x <= t) or (not equal and x < t):
                return x
        return None
    def findGreaterThan(self,t,equal=True):
        for x in self.data:
            if (equal and x >= t) or (not equal and x > t):
                return x
        return None

def test():
    print("-- Test Vanilla mode")
    bst = BinarySearchTree(100)
    bst.insert(0)
    bst.insert(10)
    bst.insert(20)
    bst.insert(99)
    print(bst.find(9),0)
    print(bst.find(10),1)
    print(bst.find(11),0)
    print(bst.find(99),1)
    print(bst.findLessThan(0, equal=False),None)
    print(bst.findLessThan(0),0)
    print(bst.findLessThan(5),0)
    print(bst.findLessThan(10),10)
    print(bst.findLessThan(10, equal=False),0)
    print(bst.findGreaterThan(15),20)
    print(bst.findGreaterThan(10),10)
    print(bst.findGreaterThan(20),20)
    print(bst.findGreaterThan(30),99)
    print(bst.findGreaterThan(99), 99)
    print(bst.findGreaterThan(99, equal=False),None)
    print(bst.findLessThan(0),0)
    print(bst.findLessThan(1),0)
    print(bst.findLessThan(99),99)
    print(bst.findGreaterThan(0),0)
    print(bst.findGreaterThan(98),99)
    print(bst.findGreaterThan(99),99)

def testComp():
    print("-- Test comp mode")
    bst = BinarySearchTreeWithCompressedData([0,20,10,99])
    bst.insert(0)
    bst.insert(10)
    bst.insert(20)
    bst.insert(99)
    print(bst.find(9),0)
    print(bst.find(10),1)
    print(bst.find(11),0)
    print(bst.find(99),1)
    print(bst.findLessThan(0, equal=False),None)
    print(bst.findLessThan(0),0)
    print(bst.findLessThan(5),0)
    print(bst.findLessThan(10),10)
    print(bst.findLessThan(10, equal=False),0)
    print(bst.findGreaterThan(15),20)
    print(bst.findGreaterThan(10),10)
    print(bst.findGreaterThan(20),20)
    print(bst.findGreaterThan(30),99)
    print(bst.findGreaterThan(99), 99)
    print(bst.findGreaterThan(99, equal=False),None)
    print(bst.findLessThan(0),0)
    print(bst.findLessThan(1),0)
    print(bst.findLessThan(99),99)
    print(bst.findGreaterThan(0),0)
    print(bst.findGreaterThan(98),99)
    print(bst.findGreaterThan(99),99)

def randomTest():
    import random
    N = 10**3
    K = 100
    M = 100
    for _ in range(N):
        samples = [random.randint(-K,K) for _ in range(M)]
        queries = [random.randint(-K,K) for _ in range(M)]
        t0 = ForTest()
        t1 = BinarySearchTreeWithCompressedData(samples)
        for s,q in zip(samples, queries):
            t0.insert(s)
            t1.insert(s)
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
    testComp()
    randomTest()

    
