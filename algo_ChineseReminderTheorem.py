def chineseReminderTheorem(rs, ms):
    def extgcd(a,b):
        if b == 0:
            return 1, 0, a
        y, x, d = extgcd(b, a % b)
        y = y - (a//b) * x
        if d < 0:
            x,y,d = -x,-y,-d
        return x, y, d
    mp = ms[0]
    x = rs[0] % ms[0]
    for r,m in zip(rs[1:],ms[1:]):
        inv = extgcd(mp,m)[0] % m
        t = ((r-x)*inv) % m
        x += t*mp
        mp *= m
    return x

def test():
    rs = [2,5,6,12]
    ms = [15,14,11,13]
    x = chineseReminderTheorem(rs,ms)
    print(x)
    for r,m in zip(rs,ms):
        print(r, x % m)

if __name__ == '__main__':
    test()



