def match_bipartial(g,A,B):
    m = {v:-1 for v in A+B}
    cnt = 0
    def find_and_match(a):
        for b in g[a]:
            if m[b] == -1:
                m[a],m[b] = b,a
                return True
        return False
    for a in A:
        if find_and_match(a):
            cnt += 1
            continue
        for b in g[a]:
            na = m[b]
            if find_and_match(na):
                m[a],m[b] = b,a
                cnt += 1
                break
    return cnt 

def test():
    g = {
            1:[4,5,6],2:[4],3:[5],
            4:[1,2],5:[1,3],6:[1]
        }
    print(match_bipartial(g,[1,2,3],[4,5,6]))

if __name__=='__main__':
    test()
