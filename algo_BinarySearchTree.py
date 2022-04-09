from algo_binary_indexed_tree import BinaryIndexedTree

# multiset
# need compression
class BinarySearchTree:
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



def test():
    bst = BinarySearchTree(100)
    bst.insert(10)
    bst.insert(20)
    print(bst.find(9),False)
    print(bst.find(10),True)
    print(bst.find(11),False)
    print(bst.findEqualOrLessThan(0),None)
    print(bst.findEqualOrLessThan(5),None)
    print(bst.findEqualOrLessThan(15),10)
    print(bst.findEqualOrLessThan(10),10)
    print(bst.findEqualOrLessThan(20),20)
    print(bst.findEqualOrGreaterThan(15),20)
    print(bst.findEqualOrGreaterThan(10),10)
    print(bst.findEqualOrGreaterThan(20),20)
    print(bst.findEqualOrGreaterThan(30),None)
    print(bst.findEqualOrGreaterThan(99),None)
    bst.insert(0)
    bst.insert(99)
    print(bst.findEqualOrLessThan(0),0)
    print(bst.findEqualOrLessThan(1),0)
    print(bst.findEqualOrLessThan(99),99)
    print(bst.findEqualOrGreaterThan(0),0)
    print(bst.findEqualOrGreaterThan(98),99)
    print(bst.findEqualOrGreaterThan(99),99)

if __name__=='__main__':
    test()

    
