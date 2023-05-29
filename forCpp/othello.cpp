#include<tuple>
#include<iostream>
#include<map>
#include<bit>
#include<vector>
#include<memory>
#include<random>
#include<map>
#include<chrono>
#include<queue>
std::random_device rd{};
std::mt19937 mt(rd());
namespace othello {
    static const int GAME_SIZE = 8;
    using btype = uint64_t;
    using Board = std::array<btype, 2>;
    using Result = std::pair<bool, Board>;
    static std::array<btype, GAME_SIZE* GAME_SIZE> buf;
    static Board null = Board{ 0,0 };
    using State = std::tuple<btype, int, int, Board>;

    btype getBit(int x, int y) {
        return btype(1) << (GAME_SIZE * x + y);
    }

    bool isNull(const Board& bw) {
        return bw[0] == 0 && bw[1] == 0;
    }

    int next(int turn) {
        return (turn + 1) & 1;
    }

    std::tuple<int, int> count(const Board& bw) {
        int nb = std::popcount(bw[0]);
        int nw = std::popcount(bw[1]);
        return { nb,nw };
    }

    void printBoard(const Board& bw) {
        for (int x = 0; x < GAME_SIZE; x++) {
            for (int y = 0; y < GAME_SIZE; y++) {
                btype pos = getBit(x, y);
                if (bw[0] & pos) {
                    std::cout << 'B';
                } else if (bw[1] & pos) {
                    std::cout << 'W';
                } else {
                    std::cout << '-';
                }
            }
            std::cout << std::endl;
        }
        auto [nb, nw] = count(bw);
        std::cout << "b:" << nb << " w:" << nw << std::endl;
    }

    Board generate() {
        int size = GAME_SIZE;
        int half = size / 2;
        btype b = 0;
        btype w = 0;
        b |= getBit(half - 1, half);
        b |= getBit(half, half - 1);
        w |= getBit(half - 1, half - 1);
        w |= getBit(half, half);
        return { b,w };
    }

    Result move(const Board& bw, int turn, int x, int y, bool inplace = true) {
        btype pos = getBit(x, y);
        if (bw[0] & pos || bw[1] & pos) return { false, bw };
        int nturn = othello::next(turn);
        int cnt = 0;
        for (int dx = -1; dx < 2; dx++) {
            for (int dy = -1; dy < 2; dy++) {
                int temp = 0;
                int nx = x + dx;
                int ny = y + dy;
                while (0 <= nx && nx < GAME_SIZE && 0 <= ny && ny < GAME_SIZE) {
                    btype np = getBit(nx, ny);
                    if (bw[nturn] & np) {
                        buf[cnt + temp] = np;
                        temp += 1;
                    } else if (bw[turn] & np) {
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
        if (cnt == 0) return { false, bw };
        Board nbw = bw;
        nbw[turn] |= pos;
        for (int i = 0; i < cnt; i++) {
            nbw[turn] |= buf[i];
            nbw[nturn] ^= buf[i];
        }
        return { true, nbw };
    }

    std::vector<State> nextStatesOf(const Board& bw, int turn) {
        std::vector<State> res;
        for (int x = 0; x < GAME_SIZE; x++) {
            for (int y = 0; y < GAME_SIZE; y++) {
                auto [ok, nbw] = move(bw, turn, x, y);
                if (ok) {
                    auto [nb, nw] = count(nbw);
                    res.emplace_back(getBit(x, y), nb, nw, nbw);
                }
            }
        }
        return res;
    }

    class Player {
    public:
        virtual Result move(const Board& bw, int turn) = 0;
        virtual void print() {};
        virtual void reset() {};
    };

    int game(std::shared_ptr<Player> player1, std::shared_ptr<Player> player2, bool show = false) {
        player1->reset();
        player2->reset();
        auto bw = generate();
        bool game_end = false;
        double elapsed1 = 0.0;
        double elapsed2 = 0.0;
        while (!game_end) {
            game_end = true;
            //auto start = std::chrono::system_clock::now();
            auto [ok, nbw] = player1->move(bw, 0);
            //auto end = std::chrono::system_clock::now();
            //elapsed1 += std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
            if (ok) {
                bw = nbw;
                game_end = false;
                if (show) othello::printBoard(bw);
            }
            //start = std::chrono::system_clock::now();
            auto [ok2, nbw2] = player2->move(bw, 1);
            //end = std::chrono::system_clock::now();
            //elapsed2 += std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
            if (ok2) {
                bw = nbw2;
                game_end = false;
                if (show) othello::printBoard(bw);
            }
        }
        //std::cout << elapsed1 << "," << elapsed2 << std::endl;
        auto [nb, nw] = count(bw);
        if (nb > nw) {
            return 0;
        } else if (nb < nw) {
            return 1;
        } else {
            return -1;
        }
    }
};

class RandomPlayer : public othello::Player {
    othello::Result move(const othello::Board& bw, int turn) override {
        const auto states = othello::nextStatesOf(bw, turn);
        if (states.empty()) return { false, bw };
        const auto& [pos, nb, nw, nbw] = states[mt() % states.size()];
        return { true, nbw };
    }
};

std::map<int, long> count;
class MiniMaxPlayer : public othello::Player {
    int search_depth;
    int my_turn = 0;
    int coeff = 0;
    bool find_valid = false;
    using scoreBoard = std::tuple<int, othello::Board>;

    scoreBoard _move(const othello::Board& bw, int turn, int depth) {
        auto [nb, nw] = othello::count(bw);
        int score = (nb - nw) * coeff;
        if (depth == 0) {
            return { score, bw };
        }
        auto states = othello::nextStatesOf(bw, turn);
        //count[search_depth - depth + 1] += 1;
        if (states.empty()) {
            return { score, bw };
        }
        std::shuffle(states.begin(), states.end(), mt); // 乱択性のため

        find_valid = true;
        othello::Board res;
        if (turn == my_turn) {
            int max_score = -100;
            for (const auto& state : states) {
                auto& [pos, nb, nw, nbw] = state;
                auto [score, _] = _move(nbw, othello::next(turn), depth - 1);
                if (score > max_score) {
                    max_score = score;
                    res = nbw;
                }
            }
            return { max_score, res };
        } else {
            int min_score = 100;
            for (const auto& state : states) {
                auto& [pos, nb, nw, nbw] = state;
                auto [score, _] = _move(nbw, othello::next(turn), depth - 1);
                if (score < min_score) {
                    min_score = score;
                    res = nbw;
                }
            }
            return { min_score, res };
        }
    }

public:
    MiniMaxPlayer(int depth = 1) :search_depth(depth) {};
    void print() override {
        for (int i = 0; i < search_depth + 3; i++) {
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }

    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1; // スコアに掛ける係数
        find_valid = false;

        auto [score, result] = _move(bw, turn, search_depth);
        return { find_valid, result };
    }
};


class AlphaBetaPlayer : public othello::Player {
    int search_depth;
    int my_turn = 0;
    int coeff = 0;
    bool find_valid = false;
    using scoreBoard = std::tuple<int, othello::Board>;

    scoreBoard _move(const othello::Board& bw, int turn, int depth, int alpha, int beta) {
        auto [nb, nw] = othello::count(bw);
        int score = (nb - nw) * coeff;
        if (depth == 0) {
            return { score, bw };
        }
        auto states = othello::nextStatesOf(bw, turn);
        //count[search_depth - depth + 1] += 1;
        if (states.empty()) {
            return { score, bw };
        }
        std::shuffle(states.begin(), states.end(), mt); // 乱択性のため

        find_valid = true;
        othello::Board res;
        if (turn == my_turn) {
            for (const auto& state : states) {
                auto& [pos, nb, nw, nbw] = state;
                auto [score, _] = _move(nbw, othello::next(turn), depth - 1, alpha, beta);
                if (alpha < score) {
                    alpha = score;
                    res = nbw;
                }
                if (alpha >= beta) break;
            }
            return { alpha, res };
        } else {
            for (const auto& state : states) {
                auto& [pos, nb, nw, nbw] = state;
                auto [score, _] = _move(nbw, othello::next(turn), depth - 1, alpha, beta);
                beta = std::min(beta, score);
                if (score < beta) {
                    beta = score;
                    res = nbw;
                }
                if (alpha >= beta) break;
            }
            return { beta, res };
        }
    }

public:
    AlphaBetaPlayer(int depth = 1) :search_depth(depth) {};
    void print() override {
        for (int i = 0; i < search_depth + 2; i++) {
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }

    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1; // スコアに掛ける係数
        find_valid = false;

        auto [score, result] = _move(bw, turn, search_depth, -100, 100);
        return { find_valid, result };
    }
};

class NegaScoutPlayer : public othello::Player {
    int search_depth;
    int my_turn = 0;
    int coeff = 0;
    bool find_valid = false;
    using scoreBoard = std::tuple<int, othello::Board>;

    scoreBoard _move(const othello::Board& bw, int turn, int depth, int alpha, int beta) {
        auto [nb, nw] = othello::count(bw);
        int score = (nb - nw) * coeff;
        if (depth == 0) return { score, bw };

        auto states = othello::nextStatesOf(bw, turn);
        //count[search_depth - depth + 1] += 1;
        if (states.empty()) return { score, bw };

        find_valid = true;

        std::shuffle(states.begin(), states.end(), mt); // 乱択性のため
        int mi;
        int tscore = -100;
        for(int i = 0; i < states.size(); i++){
            const auto& [pos, nb2, nw2, res] = states[i];
            if(tscore < (nb2-nw2)*coeff){
                tscore = (nb2-nw2)*coeff;
                mi = i;
            }
        }

        const auto& state = states[mi];
        auto [pos, nb2, nw2, res] = state;
        auto [v, _] = _move(res, othello::next(turn), depth - 1, -beta, -alpha);
        v = -v;
        int max_score = v;
        if (beta <= v) return { v, res };
        if (alpha < v) alpha = v;

        for (int i = 0; i < states.size(); i++) {
            if(i==mi) continue;
            const auto& state = states[i];
            auto& [pos, nb, nw, nbw] = state;
            auto [v, _] = _move(nbw, othello::next(turn), depth - 1, -alpha - 1, -alpha);
            v = -v;
            if (beta <= v) return { v, nbw };
            if (alpha < v) {
                alpha = v;
                const auto& [nv, _2] = _move(nbw, othello::next(turn), depth - 1, -beta, -alpha);
                v = -nv;
                if (beta <= v) return { v, nbw };
                if (alpha < v) alpha = v;
            }
            if (max_score < v) {
                max_score = v;
                res = nbw;
            }
        }
        return { max_score, res };
    }

public:
    NegaScoutPlayer(int depth = 1) :search_depth(depth) {};

    void print() override {
        for (int i = 0; i < search_depth + 2; i++) {
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }
    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1; // スコアに掛ける係数
        find_valid = false;

        auto [score, result] = _move(bw, turn, search_depth, -100, 100);
        return { find_valid, result };
    }
};


class BeamSearchPlayer : public othello::Player {
    int search_depth;
    int search_width;
    int my_turn = 0;
    int coeff = 0;
    bool find_valid = false;

    // ScoreState: <score, board, first_board>
    using ScoreState = std::tuple<int, othello::Board, othello::Board>;

    othello::Board _move(const othello::Board& bw, int turn, int depth, int alpha, int beta) {
        auto states = othello::nextStatesOf(bw, turn);
        if (states.empty() || depth == 0) {
            return bw;
        }

        find_valid = true;

        std::priority_queue<ScoreState> q;
        for (const auto& state : states) {
            auto& [pos, nb, nw, nbw] = state;
            int score = (nb - nw) * coeff;
            q.emplace(score, nbw, nbw);
        }

        for (int d = 0; d < depth; d++) {
            turn = othello::next(turn);
            std::priority_queue<ScoreState> nq;
            if (turn == my_turn) {
                for (int w = 0; w < search_width; w++) {
                    auto& [_, bw, fbw] = q.top();
                    q.pop();
                    auto states = othello::nextStatesOf(bw, turn);
                    for (const auto& state : states) {
                        auto& [pos, nb, nw, nbw] = state;
                        int score = (nb - nw) * coeff;
                        nq.emplace(score, nbw, fbw);
                    }
                    if (q.empty()) break;
                }
            } else {
                for (int w = 0; w < search_width; w++) {
                    auto& [_, bw, fbw] = q.top();
                    q.pop();
                    auto states = othello::nextStatesOf(bw, turn);
                    for (const auto& state : states) {
                        auto& [pos, nb, nw, nbw] = state;
                        int score = (nb - nw) * coeff;
                        nq.emplace(score, nbw, fbw);
                    }
                    if (q.empty()) break;
                }
            }
            if (nq.empty()) break;
            q = nq;
        }
        auto& [_, nbw, fbw] = q.top();
        return fbw;
    }

public:
    BeamSearchPlayer(int depth = 1, int width = 100000) :search_depth(depth), search_width(width) {};
    void print() override {
        for (int i = 0; i < search_depth + 2; i++) {
            std::cout << "depth=" << i << ", " << count[i] << std::endl;
        }
    }

    othello::Result move(const othello::Board& bw, int turn) override {
        my_turn = turn;
        coeff = (turn == 0) ? 1 : -1; // スコアに掛ける係数
        find_valid = false;

        auto result = _move(bw, turn, search_depth, -100, 100);
        return { find_valid, result };
    }
};





void debug() {
    auto bw = othello::generate();
    std::shared_ptr<othello::Player> player = std::make_shared<MiniMaxPlayer>(2);
    player->move(bw, 0);
}

int main() {
    //debug();
    //return 0;
    std::shared_ptr<othello::Player> player1 = std::make_shared<RandomPlayer>();
    //std::shared_ptr<othello::Player> player1 = std::make_shared<MiniMaxPlayer>(2);
    //std::shared_ptr<othello::Player> player1 = std::make_shared<AlphaBetaPlayer>(4);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<RandomPlayer>();
    //std::shared_ptr<othello::Player> player2 = std::make_shared<MiniMaxPlayer>(4);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<MiniMaxPlayer>(6);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<MiniMaxPlayer>(5);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<AlphaBetaPlayer>(4);
    //std::shared_ptr<othello::Player> player2 = std::make_shared<BeamSearchPlayer>(2, 2000000);
    std::shared_ptr<othello::Player> player2 = std::make_shared<NegaScoutPlayer>(4);
    int N = 500;
    bool show = false;
    std::map<int, int> result;
    auto start = std::chrono::system_clock::now();
    for (int i = 0; i < N; i++) {
        int res = othello::game(player1, player2, show);
        result[res] += 1;
        res = othello::game(player2, player1, show);
        res = (res == -1 ? res : ((res + 1) & 1));
        result[res] += 1;
        std::cout << "p1:" << result[0] << ", p2:" << result[1] << ", draw:" << result[-1] << std::endl;
    }
    std::cout << "p1:" << result[0] << ", p2:" << result[1] << ", draw:" << result[-1] << std::endl;
    auto end = std::chrono::system_clock::now();
    double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    std::cout << "elapsed: " << elapsed << "ms" << std::endl;
    player2->print();
    return 0;
}
