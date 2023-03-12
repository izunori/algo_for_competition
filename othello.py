from collections import Counter
from itertools import product, chain

GAME_SIZE = 6

def printBoard(bw):
    board = decompress(bw)
    marks = {-1:'W',1:'B',0:'-'}
    res = ' abcdefgh'[:GAME_SIZE+1] + '\n'
    for i,row in enumerate(board):
        temp = str(i+1)+"".join(map(lambda x : marks[x], row))
        res += temp+'\n'
    nb,nw = count(bw)
    res += f" {marks[1]}:{nb} {marks[-1]}:{nw}\n"
    print(res)

def count(bw):
    b,w = bw
    nb = bin(b).count('1')
    nw = bin(w).count('1')
    return nb, nw

def generate():
    size = GAME_SIZE
    half_size = size//2
    board = [[0]*size for _ in range(size)]
    board[half_size-1][half_size-1] = -1 # white
    board[half_size][half_size-1] = 1 # black
    board[half_size-1][half_size] = 1
    board[half_size][half_size] = -1
    return compress(board)

def move(bw, turn, pos, inplace=True):
    x, y = pos
    board = decompress(bw)
    if not board[x][y] == 0:
        return None
    dirs = [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]
    cnt = 0
    rvs = []
    for dx, dy in dirs:
        temp = 0
        trvs = []
        nx,ny = x+dx,y+dy
        while 0<=nx<GAME_SIZE and 0<=ny<GAME_SIZE:
            if board[nx][ny] == -turn:
                trvs.append((nx,ny))
                temp += 1
            elif board[nx][ny] == turn:
                rvs.extend(trvs)
                cnt += temp
                break
            else: # 0
                break
            nx,ny = nx+dx,ny+dy
    if cnt == 0:
        return None
    if inplace == True:
        board[x][y] = turn 
        for tx,ty in rvs:
            board[tx][ty] = turn
    return compress(board)

def nextStateOf(bw, turn):
    size = GAME_SIZE
    result = []
    for x in range(size):
        for y in range(size):
            res = move(bw, turn, (x,y))
            if res is not None:
                ncnt = count(res)
                result.append((res, ncnt))
    return result

def compress(board):
    b,w = 0,0
    for i,c in enumerate(chain(*board)):
        if c == 1:
            b |= 1<<i
        elif c == -1:
            w |= 1 <<i
    return b,w

def decompress(bw):
    b,w = bw
    size = GAME_SIZE
    board = [[0]*size for _ in range(size)]
    for x,y in product(range(size), repeat=2):
        if b % 2 == 1:
            board[x][y] = 1
        elif w % 2 == 1:
            board[x][y] = -1
        b >>= 1
        w >>= 1
    return board

if __name__=='__main__':
    bw = generate()
    printBoard(bw)
    for nbw, ncnt in nextStateOf(bw, 1):
        printBoard(nbw)
        print(ncnt)
    bw = nbw
    for nbw, ncnt in nextStateOf(bw, -1):
        printBoard(nbw)
        print(ncnt)

