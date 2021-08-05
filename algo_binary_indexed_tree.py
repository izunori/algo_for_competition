# Binary Indexed Tree
class BinaryIndexedTree:
    def __init__(self,data,op,default):
        self.op = op
        self.default = default
        N = len(data)
        self.l = 2**((N-1).bit_length())
        self.data = [default]*(self.l+1)
        for i in range(1,N+1):
            v = data[i-1]
            while i <= self.l:
                self.data[i] = self.op(self.data[i], v)
                i += i & -i
    def add(self,i,v):
        i += 1
        while i <= self.l:
            self.data[i] = self.op(self.data[i], v)
            i += i & -i

    # WARNING : return sum of 0<=x<i
    def get(self,i):
        res = 0
        while i > 0:
            res = self.op(res, self.data[i])
            i -= i & -i
        return res

def test():
    bit = BinaryIndexedTree([1,2,3,4,5,6,7],lambda x,y:x+y,0)
    bit.add(2,10)
    print(bit.get(1),1)
    print(bit.get(2),3)
    print(bit.get(3),16)
    print(bit.get(4),20)

if __name__=='__main__':
    test()
