import numpy as np


# return s,t
# s.t. s + nt is sol for n >= 0
def all_non_nega_sol(a,b,c):
    none = (None,(-1,-1),(-1,-1))
    if a == b == 0:
        return 'inf',(0,0),(0,0) if c == 0 else none
    if a == 0:
        if (c%b != 0 or c*b<0):
            return none
        else:
            return 'inf',(0,c//b),(1,0)
    if b == 0:
        if (c % a != 0 or c*a<0):
            return none
        else:
            return 'inf',(c//a,0),(0,1)
    x,y,d = extgcd(a,b,c)
    if c % d != 0:
        return none
    k = c//d
    lcm = abs(a*b)//gcd(a,b)
    dx = abs(lcm//a)
    dy = (-a*dx)//b
    x = (k*x) % dx # >= 0 minimum
    y = (c-a*x)//b
    if dy >= 0:
        if y >= 0:
            return 'inf',(x,y),(dx,dy)
        else:
            t = -(y//dy)
            x += dx*t
            y += dy*t
            return 'inf',(x,y),(dx,dy)
    else:
        if y < 0:
            return none
        else:
            t = y//(-dy)+1
            return t,(x,y),(dx,dy)


# ax+by=c s.t. x,y>=0 and minimum
# a,b \neq 0
def non_nega_sol(a,b,c):
    x,y,d = extgcd(a,b)
    if c % d != 0:
        return None
    k = c // d
    lcm = abs(a*b)//gcd(a,b)
    dx = abs(lcm//a)
    x = (k*x) % dx # >= 0
    y = (c-a*x)//b
    # now x is minimum positive
    # return (x,y)
    if y >= 0:
        return (x,y)
    ny = (c-a*(x+dx))//b
    dy = ny-y
    if dy <= 0:
        return None
    d = abs(y//dy)
    x += d*dx
    y += d*dy
    return (x,y)

# ax + by = d
# a,b \neq 0
def extgcd(a,b):
    if b == 0:
        return 1, 0, a
    y, x, d = extgcd(b, a % b)
    y = y - (a//b) * x
    if d < 0:
        x,y,d = -x,-y,-d
    return x, y, d

def gcd(a,b):
    while b:
        a,b = b, a % b
    return a * (-1)**(a < 0)

if __name__=='__main__':
    print(non_nega_sol(4,6,-2))
    print(non_nega_sol(4,6,2))
    print(non_nega_sol(4,-6,10))
    print(non_nega_sol(8,4,4))
    print(non_nega_sol(-12,4,0))
    print(all_non_nega_sol(1,0,0))


