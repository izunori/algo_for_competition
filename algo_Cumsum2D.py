# data : 0-indexed 2d array
# All values at 0-index must be 0
class Cumsum2d:
    def __init__(self, data, padding=False):
        self.data = data
        self.H, self.W = len(self.data), len(self.data[0])
        for x in range(self.H):
            for y in range(self.W-1):
                self.data[x][y+1] += self.data[x][y]
        for y in range(self.W):
            for x in range(self.H-1):
                self.data[x+1][y] += self.data[x][y]
    def get(self, ltx, lty, rbx, rby):
        res = self.data[rbx-1][rby-1]
        res -= self.data[rbx-1][lty-1]
        res -= self.data[ltx-1][rby-1]
        res += self.data[ltx-1][lty-1]
        return res

def test():
    data = [
            [0,0,0,0],
            [0,1,0,2],
            [0,3,0,4],
            [0,0,1,0]
            ]
    cs2 = Cumsum2d(data)
    print(cs2.get(1,1,4,4), 11)
    print(cs2.get(1,1,3,4), 10)
    print(cs2.get(1,2,3,4), 6)

if __name__=='__main__':
    test()

