def determinant(mat):
    n = len(mat)
    memo = [0]*2**n
    memo[0] = 1
    for i in range(1,2**n):
        nb = bin(i).count('1')
        j = i
        d = 0
        sign = 1
        while j:
            b = -j & j
            d += sign*mat[nb-1][n-b.bit_length()]*memo[i^b]
            j ^= b
            sign = -sign
        memo[i] = d
    return memo[2**n-1]

def test():
    print(determinant([[1,2],[3,4]]), -2)
    print(determinant([[1,3,4],[2,3,5],[1,2,4]]), -3)
    print(determinant([[1,3,4,7],[2,3,5,34],[1,2,4,33],[4,-23,3,0]]), 2060)
    pass

def perf():
    import random
    from time import perf_counter as time
    N = 14
    mat = [[random.randint(0,10) for i in range(N)] for j in range(N)]
    start = time()
    det = determinant(mat)
    print(f"{time() - start}")
    print(det)

if __name__=='__main__':
    test()
    perf()
