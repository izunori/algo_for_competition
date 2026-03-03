#include "player.hpp"
#include <random>
#include <iostream>

class RandomPlayer : public IPlayer {
private:
    std::mt19937 rng;
    std::string name;

public:
    RandomPlayer(const std::string& player_name, unsigned int seed = std::random_device{}())
        : rng(seed), name(player_name) {}

    std::string get_name() const override {
        return name;
    }

    Move select_move(const GameState& state, const std::vector<PieceShape>& pieces) override {
        std::vector<Move> valid_moves;

        // 全ての可能な手を列挙
        for (int piece_id = 0; piece_id < PieceLibrary::NUM_PIECES; piece_id++) {
            if (state.used_pieces[state.current_player][piece_id]) {
                continue; // 既に使用済み
            }

            const auto& piece = pieces[piece_id];

            // 全ての位置、回転、反転を試す
            for (int y = 0; y < BOARD_SIZE; y++) {
                for (int x = 0; x < BOARD_SIZE; x++) {
                    for (int rotation = 0; rotation < 4; rotation++) {
                        for (int flip = 0; flip < 2; flip++) {
                            Move move(piece_id, rotation, flip != 0, Coord(y, x));
                            if (state.is_valid_move(move, pieces)) {
                                valid_moves.push_back(move);
                            }
                        }
                    }
                }
            }
        }

        // 有効な手がない場合はパス
        if (valid_moves.empty()) {
            return Move(); // パス
        }

        // ランダムに手を選択
        std::uniform_int_distribution<int> dist(0, valid_moves.size() - 1);
        return valid_moves[dist(rng)];
    }
};
