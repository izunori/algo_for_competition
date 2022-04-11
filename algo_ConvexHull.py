from algo_BinarySearchTree import BinarySearchTreeWithCompressedData
class ConvexHull:
    def __init__(self, pts):
        self.bst = BinarySearchTreeWithCompressedData(pts)
        self.sx, self.sy = 0,0
    def add(self, pt):
        if self.bst.count() < 3:
            self.bst.insert(pt)
            self.sx += pt[0]
            self.sy += pt[1]
            return
        

def Graham(pts):
    if len(pts) == 1:
        return pts
    pts.sort()
    top,btm = [pts[0],pts[1]], [pts[0],pts[1]]
    for npt in pts[2:]:
        nx,ny = npt
        while len(top) > 1:
            (px,py),(x,y) = top[-2],top[-1]
            if (x-px)*(ny-py) - (y-py)*(nx-px) >= 0:
                top.pop()
            else:
                break
        top.append(npt)
        while len(btm) > 1:
            (px,py),(x,y) = btm[-2],btm[-1]
            if (x-px)*(ny-py) - (y-py)*(nx-px) <= 0:
                btm.pop()
            else:
                break
        btm.append(npt)
    return top[:-1]+btm[:-1][::-1]

    


def test():
    pts = [
            (0,0),
            (1,0),
            (0.5,0.4),
            (0.5,0.6),
            (1,1),
            (1,-1),
            (1.5,-0.4),
            (1.5,-0.6),
            (2,0)
            ]
    ch = Graham(pts)
    print(ch)
    ch = ConvexHull(pts)
    for pt in pts:
        ch.add(pt)

if __name__=='__main__':
    test()
