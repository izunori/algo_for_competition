#include<tuple>
#include<iostream>
#include<map>
#include<bit>
#include<vector>
namespace othello{
    static const int GAME_SIZE = 8;
    using btype = uint64_t;
    using Board = std::array<btype, 2>;
    static std::array<btype, GAME_SIZE*GAME_SIZE> buf;
    static Board null = Board{0,0};
    using State = std::tuple<btype, btype, int, int, Board>;

    btype getBit(int x, int y){
        return btype(1) << (GAME_SIZE * x + y);
    }

    std::tuple<int, int> count(Board& bw){
        int nb = std::popcount(bw[0]);
        int nw = std::popcount(bw[1]);
        return {nb,nw};
    }

    void printBoard(Board& bw){
        for(int x = 0; x < GAME_SIZE; x++){
            for(int y = 0; y < GAME_SIZE; y++){
                btype pos = getBit(x,y);
                if(bw[0] & pos){
                    std::cout << 'B';
                } else if(bw[1] & pos){
                    std::cout << 'W';
                } else {
                    std::cout << '-';
                }
            }
            std::cout << std::endl;
        }
        auto [nb,nw] = count(bw);
        std::cout << "b:" << nb << " w:" << nw << std::endl;
    }

    Board generate(){
        int size = GAME_SIZE;
        int half = size / 2;
        btype b = 0;
        btype w = 0;
        b |= getBit(half-1, half);
        b |= getBit(half, half-1);
        w |= getBit(half-1, half-1);
        w |= getBit(half, half);
        return {b,w};
    }

    Board move(Board& bw, int turn, int x, int y, bool inplace=true){
        btype pos = getBit(x,y);
        if(bw[0] & pos || bw[1] & pos) return null;
        int nturn = (turn + 1) & 1;
        int cnt = 0;
        for(int dx = -1; dx < 2; dx++){
            for(int dy = -1; dy < 2; dy++){
                int temp = 0;
                int nx = x + dx;
                int ny = y + dy;
                while(0<=nx && nx<GAME_SIZE && 0<=ny && ny<GAME_SIZE){
                    btype np = getBit(nx,ny);
                    if(bw[nturn] & np){
                        buf[cnt + temp] = np;
                        temp += 1;
                    } else if (bw[turn] & np){
                        cnt += temp;
                        break;
                    } else {
                        break;
                    }
                    nx += dx;
                    ny += dy;
                }
            }
        }
        if(cnt == 0) return null;
        Board nbw = bw;
        nbw[turn] |= pos;
        for(int i = 0; i < cnt; i++){
            nbw[turn] |= buf[i];
            nbw[nturn] ^= buf[i];
        }
        return nbw;
    }

    std::vector<State> nextStatesOf(Board& bw, int turn){
        std::vector<State> res;
        for(int x = 0; x < GAME_SIZE; x++){
            for(int y = 0; y < GAME_SIZE; y++){
                auto nbw = move(bw, turn, x, y);
                if(nbw[0] > 0 || nbw[1] > 0){
                    auto [nb,nw] = count(nbw);
                    res.emplace_back(x,y,nb,nw,nbw);
                }
            }
        }
        return res;
    }
};

int main(){
    othello::Board bw = othello::generate();
    othello::printBoard(bw);
    othello::Board nbw = othello::move(bw, 0, 3, 2);
    othello::printBoard(nbw);
    return 0;
}
