import bisect
from algo_segment_tree import *


def LIS(A):
    inf = 1 << 60 
    # L[i]は長さiの部分増加列の最小の最大値(infなら実現不可能)
    L = [inf] * len(A)
    for a in A:
        # L[n-1]はa未満、L[n]はa以上
        n = bisect.bisect_left(L,a) # 狭義単調増加
        #n = bisect.bisect_right(L,a) # 広義単調増加 (L[n-1]はa以下、L[n]はaより大きい)
        L[n] = a # aを使えば長さnの部分増加列の最小最大値を更新できる。inf->aなら最大の長さの更新になる
    print(L)
    print(bisect.bisect_left(L,inf)) # 実現可能な最大値(0-indexに注意)

def LIS2(A):
    # max演算によるSegment tree (第三引数はデフォルト値)
    # i番目の値は"A[i]を最後の値とする部分増加列の最大長"
    seg = SegmentTree([0]*len(A),max,0)

    index = sorted([(s,i) for i,s in enumerate(A)]) # 狭義単調増加
    #index = sorted([(s,i) for i,s in enumerate(A)]), key=lambda x : (x[0],-x[1])) # 広義単調増加

    for _, i in index: # インデックスのみ使用
        # A[i]が小さい値のiから順番に決定されていく
        seg.set(i, seg.get(0,i) + 1)
    print(seg.get(0,len(A)))

def test():
    import random
    N = 10
    M = 10
    A = [random.randint(1,M) for _ in range(N)]

    print(A)
    LIS(A)
    LIS2(A)



if __name__=='__main__':
    test()
