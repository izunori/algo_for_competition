# Binary Indexed Tree
class BinaryIndexedTree:
    def __init__(self,N,op,default):
        self.op, self.default, self.N = op, default, N
        self.data = [0]*(self.N+1)
    def add(self,i,v):
        i += 1
        while i <= self.N:
            self.data[i],i = self.op(self.data[i], v),i+(i&-i)
    # WARNING : return sum of 0<=x<i
    def get(self,i):
        res = self.default
        while i > 0:
            res,i = self.op(res, self.data[i]),i-(i&-i)
        return res

def test():
    bit = BinaryIndexedTree(7,lambda x,y:x+y,0)
    for i in range(8):
        bit.add(i,i+1)
    bit.add(2,10)
    print(bit.get(1),1)
    print(bit.get(2),3)
    print(bit.get(3),16)
    print(bit.get(4),20)
    print(bit.get(7),38)

if __name__=='__main__':
    test()
