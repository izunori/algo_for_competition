from itertools import product
# K : size
def matmul(A,B):
    res = [[0]*len(B[0]) for _ in range(len(A))]
    for x,y in product(range(len(A)),range(len(B[0]))):
        res[x][y] = sum(A[x][z]*B[z][y] for z in range(len(B)))
    return res

def matv(A,v):
    return [sum(a*x for a,x in zip(row,v)) for row in A]


