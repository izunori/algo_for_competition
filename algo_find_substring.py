from algo_suffix_array import ManberMyers

def findSubString(S,T):
    P = S+'$'+T
    sa = ManberMyers(P)
    for i,s in enumerate(sa):
        print(i,P[s:])
    l = 0
    r = len(P)
    x = 0
    while r-l > 1:
        if P[sa[x]:] <= T:
            l = x
        else:
            r = x
        x = (l+r)//2
    result = []
    # omit l (P[sa[l]:] is just T)
    for i in range(l+1,len(P)):
        if T == P[sa[i]:][:len(T)]:
            result.append(sa[i])
        else:
            break
    return result
            

def test():
    S = 'abcaabbcab'
    T = 'a'
    result = findSubString(S,T)
    print(result)

if __name__=='__main__':
    test()
