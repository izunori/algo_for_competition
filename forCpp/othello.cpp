#include<tuple>
#include<iostream>
#include<map>
#include<bit>
#include<vector>
#include<memory>
#include<random>
#include<map>
std::random_device rd{};
std::mt19937 mt(rd());
namespace othello{
    static const int GAME_SIZE = 8;
    using btype = uint64_t;
    using Board = std::array<btype, 2>;
    using Result = std::pair<bool, Board>;
    static std::array<btype, GAME_SIZE*GAME_SIZE> buf;
    static Board null = Board{0,0};
    using State = std::tuple<btype, btype, int, int, Board>;

    btype getBit(int x, int y){
        return btype(1) << (GAME_SIZE * x + y);
    }

    bool isNull(const Board& bw){
        return bw[0] == 0 && bw[1] == 0;
    }

    int next(int turn){
        return (turn + 1) & 1;
    }

    std::tuple<int, int> count(const Board& bw){
        int nb = std::popcount(bw[0]);
        int nw = std::popcount(bw[1]);
        return {nb,nw};
    }

    void printBoard(const Board& bw){
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

    Result move(const Board& bw, int turn, int x, int y, bool inplace=true){
        btype pos = getBit(x,y);
        if(bw[0] & pos || bw[1] & pos) return {false, bw};
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
        if(cnt == 0) return {false, bw};
        Board nbw = bw;
        nbw[turn] |= pos;
        for(int i = 0; i < cnt; i++){
            nbw[turn] |= buf[i];
            nbw[nturn] ^= buf[i];
        }
        return {true, nbw};
    }

    std::vector<State> nextStatesOf(const Board& bw, int turn){
        std::vector<State> res;
        for(int x = 0; x < GAME_SIZE; x++){
            for(int y = 0; y < GAME_SIZE; y++){
                auto [ok,nbw] = move(bw, turn, x, y);
                if(ok){
                    auto [nb,nw] = count(nbw);
                    res.emplace_back(x,y,nb,nw,nbw);
                }
            }
        }
        return res;
    }

    class Player{
        public:
        virtual Result move(const Board& bw, int turn) = 0;
    };

    int game(std::shared_ptr<Player> player1, std::shared_ptr<Player> player2, bool show = false){
        auto bw = generate();
        bool game_end = false;
        while(!game_end){
            game_end = true;
            auto [ok, nbw] = player1->move(bw, 0);
            if(ok){
                bw = nbw;
                game_end = false;
                if(show) othello::printBoard(bw);
            }
            auto [ok2, nbw2] = player2->move(bw, 1);
            if(ok2){
                bw = nbw2;
                game_end = false;
                if(show) othello::printBoard(bw);
            }
        }
        auto [nb,nw] = count(bw);
        if(nb > nw){
            return 0;
        } else if (nb < nw){
            return 1;
        } else {
            return -1;
        }
    }
};

class RandomPlayer : public othello::Player {
    othello::Result move(const othello::Board& bw, int turn) override {
        auto states = othello::nextStatesOf(bw, turn);
        if(states.empty()) return {false, bw};
        int num = mt() % states.size();
        auto& [x,y,nb,nw,nbw] = states[num];
        return {true, nbw};
    }
};

class MinMaxPlayer : public othello::Player {
    int depth = 1;
    public:
    MinMaxPlayer(int depth = 1):depth(depth){};

    othello::Result move(const othello::Board& bw, int turn) override {
        return move(bw, turn, depth);
    }

    othello::Result move(const othello::Board& bw, int turn, int depth){
        int max_score = -100;
        othello::Board fbw;
        auto states = othello::nextStatesOf(bw, turn);
        if(states.empty()) return {false, bw};

        std::shuffle(states.begin(), states.end(), mt);
        int coeff = (turn == 0) ? 1 : -1;
        for(const auto& state : states){
            int min_score = 100;
            auto& [x,y,nb,nw,nbw] = state;
            //std::cout << "depth:" << depth << std::endl;
            //othello::printBoard(nbw);
            //std::cout << std::endl;
            int tscore = (nb - nw) * coeff;
            //if(tscore < max_score) continue;
            for(const auto& nstate : othello::nextStatesOf(nbw, othello::next(turn))){
                auto& [nx,ny,nnb,nnw,nnbw] = nstate;
                int tscore = (nnb - nnw) * coeff;
                if(depth > 1){
                    auto [ok, nnnbw] = move(nnbw, turn, depth-1);
                    auto [nnnb,nnnw] = othello::count(nnnbw);
                    tscore = (nnnb - nnnw) * coeff;
                }
                if(tscore < min_score) min_score = tscore;
            }
            if(max_score < min_score){
                max_score = min_score;
                fbw = std::move(nbw);
            }
        }
        return {true, fbw};
    }
};

void debug(){
    auto bw = othello::generate();
    std::shared_ptr<othello::Player> player = std::make_shared<MinMaxPlayer>(2);
    player->move(bw, 0);
}

int main(){
    //debug();
    //return 0;
    std::shared_ptr<othello::Player> player1 = std::make_shared<RandomPlayer>();
    //std::shared_ptr<othello::Player> player2 = std::make_shared<RandomPlayer>();
    //std::shared_ptr<othello::Player> player1 = std::make_shared<MinMaxPlayer>(1);
    std::shared_ptr<othello::Player> player2 = std::make_shared<MinMaxPlayer>(2);
    int N = 1000;
    bool show = false;
    std::map<int,int> result;
    for(int i = 0; i < N; i++){
        int res = othello::game(player1, player2, show);
        result[res] += 1;
        res = othello::game(player2, player1, show);
        res = (res == -1 ? res : ((res+1)&1));
        result[res] += 1;
        std::cout << "p1:" << result[0] << ", p2:" << result[1] << ", draw:" << result[-1] << std::endl;
    }
    return 0;
}
