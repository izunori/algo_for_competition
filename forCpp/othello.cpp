#include<tuple>
#include<iostream>
#include<map>
#include<bit>
#include<vector>
#include<memory>
#include<random>
#include<map>
#include<chrono>
std::random_device rd{};
std::mt19937 mt(rd());
namespace othello{
    static const int GAME_SIZE = 8;
    using btype = uint64_t;
    using Board = std::array<btype, 2>;
    using Result = std::pair<bool, Board>;
    static std::array<btype, GAME_SIZE*GAME_SIZE> buf;
    static Board null = Board{0,0};
    using State = std::tuple<btype, int, int, Board>;

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
        int nturn = othello::next(turn);
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
                    res.emplace_back(getBit(x,y),nb,nw,nbw);
                }
            }
        }
        return res;
    }

    class Player{
        public:
        virtual Result move(const Board& bw, int turn) = 0;
        virtual void print(){};
        virtual void reset(){};
    };

    int game(std::shared_ptr<Player> player1, std::shared_ptr<Player> player2, bool show = false){
        player1->reset();
        player2->reset();
        auto bw = generate();
        bool game_end = false;
        double elapsed1 = 0.0;
        double elapsed2 = 0.0;
        while(!game_end){
            game_end = true;
            //auto start = std::chrono::system_clock::now();
            auto [ok, nbw] = player1->move(bw, 0);
            //auto end = std::chrono::system_clock::now();
            //elapsed1 += std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
            if(ok){
                bw = nbw;
                game_end = false;
                if(show) othello::printBoard(bw);
            }
            //start = std::chrono::system_clock::now();
            auto [ok2, nbw2] = player2->move(bw, 1);
            //end = std::chrono::system_clock::now();
            //elapsed2 += std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
            if(ok2){
                bw = nbw2;
                game_end = false;
                if(show) othello::printBoard(bw);
            }
        }
        //std::cout << elapsed1 << "," << elapsed2 << std::endl;
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
        auto& [pos,nb,nw,nbw] = states[num];
        return {true, nbw};
    }
};

class MiniMaxPlayer : public othello::Player {
    int search_depth;
    int my_turn = 0;
    int coeff = 0;
    using scoreBoard = std::tuple<int, othello::Board>;

    int _move(const othello::Board& bw, int turn, int depth){
        auto states = othello::nextStatesOf(bw, turn);
        count[search_depth - depth] += 1;
        if(states.empty() || depth == 0){
            auto [nb, nw] = othello::count(bw);
            int score = (nb-nw) * coeff;
            return score;
        }
        if(turn == my_turn){
            int max_score = -100;
            for(const auto& state : states){
                auto& [pos,nb,nw,nbw] = state;
                auto score = _move(nbw, othello::next(turn), depth-1);
                if(score > max_score) max_score = score;
            }
            return max_score;
        } else {
            int min_score = 100;
            for(const auto& state : states){
                auto& [pos,nb,nw,nbw] = state;
                int score = _move(nbw, othello::next(turn), depth-1);
                if(score < min_score) min_score = score;
            }
            return min_score;
        }
    }

    public:
    MiniMaxPlayer(int depth = 1):search_depth(depth){};
    std::map<int, int> count;
    void print(){
        for(int i = 0; i < search_depth; i++){
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }

    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1;

        auto states = othello::nextStatesOf(bw, turn);
        if(states.empty()) return {false, bw};

        std::shuffle(states.begin(), states.end(), mt);

        othello::Board result;
        int score = -100;
        for(const auto& state : states){
            auto& [pos,nb,nw,nbw] = state;
            int tscore = _move(nbw, othello::next(turn), search_depth-1);
            if(score < tscore){
                score = tscore;
                result = std::move(nbw);
            }
        }
        return {true, result};
    }
};

class AlphaBetaPlayer : public othello::Player {
    int search_depth;
    int my_turn = 0;
    int coeff = 0;
    public:
    AlphaBetaPlayer(int depth = 1):search_depth(depth){};
    std::map<int, int> count;
    void print(){
        for(int i = 0; i < search_depth; i++){
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }

    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1;

        auto states = othello::nextStatesOf(bw, turn);
        if(states.empty()) return {false, bw};

        std::shuffle(states.begin(), states.end(), mt);

        othello::Board result;
        int score = -100;
        for(const auto& state : states){
            auto& [pos,nb,nw,nbw] = state;
            int tscore = move(nbw, othello::next(turn), search_depth-1, -100, 100);
            if(score < tscore){
                score = tscore;
                result = std::move(nbw);
            }
        }
        
        return {true, result};
    }

    int move(const othello::Board& bw, int turn, int depth, int alpha, int beta){
        auto states = othello::nextStatesOf(bw, turn);
        count[search_depth - depth] += 1;
        if(states.empty() || depth == 0){
            auto [nb, nw] = othello::count(bw);
            int score = (nb-nw) * coeff;
            return score;
        }
        if(turn == my_turn){
            for(const auto& state : states){
                auto& [pos,nb,nw,nbw] = state;
                alpha = std::max(alpha, move(nbw, othello::next(turn), depth-1, alpha, beta));
                if(alpha >= beta) break;
            }
            return alpha;
        } else {
            for(const auto& state : states){
                auto& [pos,nb,nw,nbw] = state;
                beta = std::min(beta, move(nbw, othello::next(turn), depth-1, alpha, beta));
                if(alpha >= beta) break;
            }
            return beta;
        }
    }
};


class BeamSearch : public othello::Player {
    int search_depth;
    int my_turn = 0;
    int coeff = 0;
    int limit = 300000;
    public:
    BeamSearch(int depth = 1):search_depth(depth){};
    std::map<int, int> count;
    void print(){
        for(int i = 0; i < search_depth; i++){
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }

    void reset(){
        count.clear();
    }

    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1;

        auto states = othello::nextStatesOf(bw, turn);
        std::shuffle(states.begin(), states.end(), mt);
        if(states.empty()) return {false, bw};

        std::shuffle(states.begin(), states.end(), mt);

        othello::Board result;
        int score = -100;
        for(const auto& state : states){
            auto& [pos,nb,nw,nbw] = state;
            int tscore = move(nbw, othello::next(turn), search_depth-1, -100, 100);
            if(score < tscore){
                score = tscore;
                result = std::move(nbw);
            }
        }
        
        return {true, result};
    }

    int move(const othello::Board& bw, int turn, int depth, int alpha, int beta){
        auto states = othello::nextStatesOf(bw, turn);
        count[search_depth - depth] += 1;
        if(states.empty() || depth == 0){
            auto [nb, nw] = othello::count(bw);
            int score = (nb-nw) * coeff;
            return score;
        }
        if(turn == my_turn){
            if(count[depth] > limit) return alpha;
            for(const auto& state : states){
                auto& [pos,nb,nw,nbw] = state;
                alpha = std::max(alpha, move(nbw, othello::next(turn), depth-1, alpha, beta));
                if(alpha >= beta) break;
            }
            return alpha;
        } else {
            if(count[depth] > limit) return beta;
            for(const auto& state : states){
                auto& [pos,nb,nw,nbw] = state;
                beta = std::min(beta, move(nbw, othello::next(turn), depth-1, alpha, beta));
                if(alpha >= beta) break;
            }
            return beta;
        }
    }
};


void debug(){
    auto bw = othello::generate();
    std::shared_ptr<othello::Player> player = std::make_shared<MiniMaxPlayer>(2);
    player->move(bw, 0);
}

int main(){
    //debug();
    //return 0;
    std::shared_ptr<othello::Player> player1 = std::make_shared<RandomPlayer>();
    //std::shared_ptr<othello::Player> player2 = std::make_shared<RandomPlayer>();
    std::shared_ptr<othello::Player> player2 = std::make_shared<MiniMaxPlayer>(2);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<MiniMaxPlayer>(5);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<MiniMaxPlayer>(6);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<BeamSearch>(8);
    int N = 500;
    bool show = false;
    std::map<int,int> result;
    auto start = std::chrono::system_clock::now();
    for(int i = 0; i < N; i++){
        int res = othello::game(player1, player2, show);
        result[res] += 1;
        res = othello::game(player2, player1, show);
        res = (res == -1 ? res : ((res+1)&1));
        result[res] += 1;
        //std::cout << "p1:" << result[0] << ", p2:" << result[1] << ", draw:" << result[-1] << std::endl;
    }
    std::cout << "p1:" << result[0] << ", p2:" << result[1] << ", draw:" << result[-1] << std::endl;
    auto end = std::chrono::system_clock::now();
    double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
    std::cout << "elapsed: " << elapsed << "ms" << std::endl ;
    player2->print();
    return 0;
}
