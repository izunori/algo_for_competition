class SlidingWindowAggregation:
    def __init__(self,op):
        self.front = []
        self.front_sum = []
        self.back = []
        self.back_sum = []
        self.op = op
    def fold_all(self):
        if self.front and self.back:
            return self.op(self.front_sum[-1],self.back_sum[-1])
        elif self.front:
            return self.front_sum[-1]
        elif self.back:
            return self.back_sum[-1]
        else:
            return None
    def push(self,x):
        self.back.append(x)
        if self.back_sum:
            self.back_sum.append(self.op(self.back_sum[-1],x))
        else:
            self.back_sum.append(x)
    def pop(self):
        if not self.front:
            while self.back:
                self.front.append(self.back.pop())
            self.back_sum.clear()
            self.front_sum.append(self.front[0])
            for v in self.front[1:]:
                self.front_sum.append(self.op(self.front_sum[-1],v))
        if self.front:
            self.front_sum.pop()
            return self.front.pop()
        return None
    def debug(self):
        print("front   :",self.front)
        print("frontsum:",self.front_sum)
        print("back    :",self.back)
        print("backsum :",self.back_sum)

def test():
    swa = SlidingWindowAggregation(lambda x,y : x+y)
    for i in range(1,11):
        swa.push(i)
    swa.debug()
    print(swa.pop(),1)
    swa.debug()
    print(swa.pop(),2)
    swa.debug()
    print(swa.pop(),3)
    swa.debug()
    swa.push(10)
    swa.debug()
    print(swa.fold_all(),59)
    swa.debug()
    swa.push(100)
    swa.debug()
    print(swa.fold_all(),159)
    swa.debug()
    for i in range(7):
        swa.pop()
    swa.debug()
    swa.pop()
    swa.debug()
    print(swa.fold_all(),100)


if __name__=='__main__':
    test()

