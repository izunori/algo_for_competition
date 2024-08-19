
def maxAreaInHistogram(A):
    stack = []
    result = 0
    for i,a in enumerate(A):
        pi = i
        while stack and stack[-1][0] > a:
            pa,pi = stack.pop()
            result = max(result, pa * (i-pi))
        stack.append((a,pi))
    while stack:
        pa,pi = stack.pop()
        result = max(result, pa * (len(A)-pi))
    return result


def test():
    import random
    N = 10
    M = 10
    A = [random.randint(0,M) for _ in range(N)]

    ans = 0
    for i in range(N):
        for j in range(i+1,N+1):
            h = min(A[i:j])
            area = h * (j-i)
            ans = max(ans, area)

    submit = maxAreaInHistogram(A)

    if ans == submit:
        print("OK")
    else:
        print("NG")
        print(A)
        print("ans:", ans)
        print("sub:", submit)
        exit()


if __name__=='__main__':
    test()

