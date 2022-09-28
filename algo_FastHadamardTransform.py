MOD = 998244353

# xor : [[1,1],[1,-1]], xor^-1 : [[1,1],[1,-1]]
# and : [[1,1],[0,1]], and^-1 : [[1,-1],[0,1]]
# or : [[1,0],[1,1]], or^-1 : [[1,0],[-1,1]]
def FastWalshHadamardTransform(a):
    k = (len(a) - 1).bit_length()
    a += [0]*(2**k - len(a))
    h = 1
    for _ in range(k):
        for i in range(0,len(a),h*2):
            for j in range(i,i+h):
                a[j],a[j+h] = (a[j]+a[j+h])%MOD,(a[j]-a[j+h])%MOD
        h *= 2

# result : overwrite X
def xorConv(X,Y):
    k = max((len(X)-1).bit_length(), (len(Y)-1).bit_length())
    X += [0]*(2**k - len(X))
    Y += [0]*(2**k - len(Y))
    FastWalshHadamardTransform(X)
    FastWalshHadamardTransform(Y)
    for i in range(len(X)):
        X[i] = (X[i]*Y[i]) % MOD
    FastWalshHadamardTransform(X)
    ik = pow(pow(2,MOD-2,MOD),k,MOD)
    for i in range(len(X)):
        X[i] = (X[i]*ik) % MOD
    return X

def xorConv2(X,Y):
    k = max((len(X)-1).bit_length(), (len(Y)-1).bit_length())
    X += [0]*(2**k - len(X))
    Y += [0]*(2**k - len(Y))
    FastWalshHadamardTransform(X)
    FastWalshHadamardTransform(Y)
    for i in range(len(X)):
        X[i] *= Y[i]
    FastWalshHadamardTransform(X)
    for i in range(len(X)):
        X[i] >>= k
    return X

def test():
    a = [1,0,1,0,0,1,1]
    FastWalshHadamardTransform(a)
    print(a)

def testXor():
    import random
    N = 2**8
    X = [random.randint(0,MOD-1) for i in range(N)]
    Y = [random.randint(0,MOD-1) for i in range(N)]
    ans = [0]*N
    for i in range(N):
        for j in range(N):
            ans[i^j] += X[i]*Y[j]
            ans[i^j] %= MOD
    xorConv(X,Y)
    if X == ans:
        print('OK')
    else:
        print('NG')

if __name__=='__main__':
    test()
    testXor()
                

