#pragma once

#include <vector>
#include <array>
#include <string>
#include <algorithm>
#include <iostream>

// ボードサイズ
constexpr int BOARD_SIZE = 14;

// プレイヤー番号
enum Player : int {
    PLAYER_NONE = 0,
    PLAYER_1 = 1,
    PLAYER_2 = 2
};

// 座標
struct Coord {
    int y, x;

    Coord(int y = 0, int x = 0) : y(y), x(x) {}

    bool operator==(const Coord& other) const {
        return y == other.y && x == other.x;
    }

    Coord operator+(const Coord& other) const {
        return Coord(y + other.y, x + other.x);
    }
};

// ピースの形状（相対座標のリスト）
struct PieceShape {
    std::vector<Coord> cells;
    int size() const { return cells.size(); }
};

// 手の情報
struct Move {
    int piece_id;      // ピース番号（0-20）
    int rotation;      // 回転（0-3: 0度, 90度, 180度, 270度）
    bool flip;         // 反転
    Coord position;    // 配置位置（基準点）

    Move() : piece_id(-1), rotation(0), flip(false), position(0, 0) {}
    Move(int pid, int rot, bool flp, Coord pos)
        : piece_id(pid), rotation(rot), flip(flp), position(pos) {}

    bool is_pass() const { return piece_id == -1; }
};

// 21個のポリオミノピース定義
class PieceLibrary {
public:
    static constexpr int NUM_PIECES = 21;

    static std::vector<PieceShape> create_pieces() {
        std::vector<PieceShape> pieces;

        // 1マス (piece 0)
        pieces.push_back({{Coord(0,0)}});

        // 2マス (piece 1)
        pieces.push_back({{Coord(0,0), Coord(0,1)}});

        // 3マス (pieces 2-3)
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2)}}); // I3
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(1,0)}}); // L3

        // 4マス (pieces 4-8)
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(0,3)}}); // I4
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(1,0), Coord(1,1)}}); // O
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,1)}}); // T4
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,0)}}); // L4
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(1,1), Coord(1,2)}}); // Z4

        // 5マス (pieces 9-20)
        pieces.push_back({{Coord(0,1), Coord(1,0), Coord(1,1), Coord(1,2), Coord(2,1)}}); // F
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(0,3), Coord(0,4)}}); // I5
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(0,3), Coord(1,0)}}); // L5
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(1,1), Coord(1,2), Coord(1,3)}}); // N
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,0), Coord(1,1)}}); // P
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,1), Coord(2,1)}}); // T5
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(0,2), Coord(1,0), Coord(1,2)}}); // U
        pieces.push_back({{Coord(0,0), Coord(1,0), Coord(2,0), Coord(2,1), Coord(2,2)}}); // V
        pieces.push_back({{Coord(0,0), Coord(1,0), Coord(1,1), Coord(2,1), Coord(2,2)}}); // W
        pieces.push_back({{Coord(0,1), Coord(1,0), Coord(1,1), Coord(1,2), Coord(2,1)}}); // X
        pieces.push_back({{Coord(0,1), Coord(1,0), Coord(1,1), Coord(1,2), Coord(1,3)}}); // Y
        pieces.push_back({{Coord(0,0), Coord(0,1), Coord(1,1), Coord(2,1), Coord(2,2)}}); // Z5

        return pieces;
    }
};

// ボード状態
class Board {
private:
    std::array<std::array<int, BOARD_SIZE>, BOARD_SIZE> grid;

public:
    Board() {
        for (auto& row : grid) {
            row.fill(PLAYER_NONE);
        }
    }

    int get(int y, int x) const {
        if (y < 0 || y >= BOARD_SIZE || x < 0 || x >= BOARD_SIZE) {
            return -1; // 範囲外
        }
        return grid[y][x];
    }

    int get(const Coord& c) const {
        return get(c.y, c.x);
    }

    void set(int y, int x, int player) {
        if (y >= 0 && y < BOARD_SIZE && x >= 0 && x < BOARD_SIZE) {
            grid[y][x] = player;
        }
    }

    void set(const Coord& c, int player) {
        set(c.y, c.x, player);
    }

    // ASCII表示
    void display() const {
        std::string line = "  ";
        for (int x = 0; x < BOARD_SIZE; x++) {
            line += std::to_string(x % 10);
        }
        std::cout << line << "\n";

        for (int y = 0; y < BOARD_SIZE; y++) {
            std::cout << (y < 10 ? " " : "") << y;
            for (int x = 0; x < BOARD_SIZE; x++) {
                switch (grid[y][x]) {
                    case PLAYER_NONE: std::cout << "."; break;
                    case PLAYER_1: std::cout << "X"; break;
                    case PLAYER_2: std::cout << "O"; break;
                }
            }
            std::cout << "\n";
        }
    }

    const auto& get_grid() const { return grid; }
};

// ゲーム状態
class GameState {
public:
    Board board;
    std::array<std::vector<bool>, 3> used_pieces; // [player][piece_id]
    int current_player;
    int turn;
    std::array<bool, 3> first_move; // 各プレイヤーの初手かどうか
    std::array<bool, 3> passed; // 連続パスの検出

    GameState() : current_player(PLAYER_1), turn(0) {
        for (int i = 0; i < 3; i++) {
            used_pieces[i].resize(PieceLibrary::NUM_PIECES, false);
            first_move[i] = true;
            passed[i] = false;
        }
    }

    // ピースを変換（回転・反転）して実座標を取得
    std::vector<Coord> get_transformed_piece(const PieceShape& piece, int rotation, bool flip, const Coord& pos) const {
        std::vector<Coord> result;
        for (const auto& cell : piece.cells) {
            int y = cell.y;
            int x = cell.x;

            // 反転
            if (flip) {
                x = -x;
            }

            // 回転
            for (int r = 0; r < rotation; r++) {
                int tmp = y;
                y = -x;
                x = tmp;
            }

            result.push_back(Coord(pos.y + y, pos.x + x));
        }
        return result;
    }

    // 手が合法かチェック
    bool is_valid_move(const Move& move, const std::vector<PieceShape>& pieces) const {
        if (move.is_pass()) return true;

        if (move.piece_id < 0 || move.piece_id >= PieceLibrary::NUM_PIECES) return false;
        if (used_pieces[current_player][move.piece_id]) return false;

        const auto& piece = pieces[move.piece_id];
        auto coords = get_transformed_piece(piece, move.rotation, move.flip, move.position);

        bool has_corner_connection = false;
        bool has_edge_connection = false;

        // 各セルをチェック
        for (const auto& c : coords) {
            // 範囲チェック
            if (c.y < 0 || c.y >= BOARD_SIZE || c.x < 0 || c.x >= BOARD_SIZE) {
                return false;
            }

            // 既に埋まっているかチェック
            if (board.get(c) != PLAYER_NONE) {
                return false;
            }

            // 辺の接続チェック（同じ色の辺が接してはいけない）
            for (auto [dy, dx] : std::vector<std::pair<int,int>>{{-1,0}, {1,0}, {0,-1}, {0,1}}) {
                int ny = c.y + dy, nx = c.x + dx;
                if (board.get(ny, nx) == current_player) {
                    has_edge_connection = true;
                }
            }

            // 角の接続チェック
            for (auto [dy, dx] : std::vector<std::pair<int,int>>{{-1,-1}, {-1,1}, {1,-1}, {1,1}}) {
                int ny = c.y + dy, nx = c.x + dx;
                if (board.get(ny, nx) == current_player) {
                    has_corner_connection = true;
                }
            }
        }

        // 初手の場合、特定の位置に配置する必要がある
        if (first_move[current_player]) {
            Coord start_pos = (current_player == PLAYER_1) ? Coord(4, 4) : Coord(9, 9);
            bool covers_start = false;
            for (const auto& c : coords) {
                if (c == start_pos) {
                    covers_start = true;
                    break;
                }
            }
            return covers_start;
        }

        // 2手目以降：角接続が必要で、辺接続は禁止
        return has_corner_connection && !has_edge_connection;
    }

    // 手を適用
    void apply_move(const Move& move, const std::vector<PieceShape>& pieces) {
        if (move.is_pass()) {
            passed[current_player] = true;
        } else {
            const auto& piece = pieces[move.piece_id];
            auto coords = get_transformed_piece(piece, move.rotation, move.flip, move.position);

            for (const auto& c : coords) {
                board.set(c, current_player);
            }

            used_pieces[current_player][move.piece_id] = true;
            first_move[current_player] = false;
            passed[current_player] = false;
        }

        current_player = (current_player == PLAYER_1) ? PLAYER_2 : PLAYER_1;
        turn++;
    }

    // ゲーム終了判定
    bool is_game_over() const {
        return passed[PLAYER_1] && passed[PLAYER_2];
    }

    // スコア計算（配置したマス数）
    int get_score(int player) const {
        int score = 0;
        for (int y = 0; y < BOARD_SIZE; y++) {
            for (int x = 0; x < BOARD_SIZE; x++) {
                if (board.get(y, x) == player) {
                    score++;
                }
            }
        }
        return score;
    }
};

// プレイヤーインターフェース
class IPlayer {
public:
    virtual ~IPlayer() = default;
    virtual Move select_move(const GameState& state, const std::vector<PieceShape>& pieces) = 0;
    virtual std::string get_name() const = 0;
};
