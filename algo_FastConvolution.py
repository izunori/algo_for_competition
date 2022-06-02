# i in S <=> (1<<i) & S is True
def FastConvoltionOnSet(F, op):
    n = (len(F)-1).bit_length()
    for j in range(n):
        b = 1<<j
        for i in range(2**n):
            if i&b:
                F[i] = op(F[i],F[i^b]) # i^bはiの(右から)jビット目が少ない状態

def test():
    F = [0]*8
    F[1] = 1
    F[2] = 2
    F[4] = 4
    FastConvoltionOnSet(F, lambda x,y : x+y)
    print(F)

if __name__=='__main__':
    test()
