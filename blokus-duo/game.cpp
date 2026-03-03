#include "player.hpp"
#include "random_player.cpp"
#include <iostream>
#include <memory>
#include <iomanip>

class Game {
private:
    GameState state;
    std::vector<PieceShape> pieces;
    std::unique_ptr<IPlayer> player1;
    std::unique_ptr<IPlayer> player2;
    bool verbose;

public:
    Game(std::unique_ptr<IPlayer> p1, std::unique_ptr<IPlayer> p2, bool verbose = true)
        : player1(std::move(p1)), player2(std::move(p2)), verbose(verbose) {
        pieces = PieceLibrary::create_pieces();
    }

    void display_game_state() const {
        std::cout << "\n========================================\n";
        std::cout << "Turn: " << state.turn << "\n";
        std::cout << "Current Player: " << (state.current_player == PLAYER_1 ? "Player 1 (X)" : "Player 2 (O)") << "\n";
        std::cout << "========================================\n";
        state.board.display();
        std::cout << "\n";

        // 使用済みピースの表示
        std::cout << "Player 1 remaining pieces: ";
        int p1_remaining = 0;
        for (int i = 0; i < PieceLibrary::NUM_PIECES; i++) {
            if (!state.used_pieces[PLAYER_1][i]) p1_remaining++;
        }
        std::cout << p1_remaining << "/" << PieceLibrary::NUM_PIECES << "\n";

        std::cout << "Player 2 remaining pieces: ";
        int p2_remaining = 0;
        for (int i = 0; i < PieceLibrary::NUM_PIECES; i++) {
            if (!state.used_pieces[PLAYER_2][i]) p2_remaining++;
        }
        std::cout << p2_remaining << "/" << PieceLibrary::NUM_PIECES << "\n\n";
    }

    void display_move(const Move& move, const std::string& player_name) const {
        if (move.is_pass()) {
            std::cout << player_name << " passes.\n";
        } else {
            std::cout << player_name << " plays piece " << move.piece_id
                      << " at (" << move.position.y << "," << move.position.x << ")"
                      << " rotation=" << move.rotation
                      << " flip=" << (move.flip ? "yes" : "no") << "\n";
        }
    }

    void play() {
        std::cout << "\n";
        std::cout << "╔══════════════════════════════════════╗\n";
        std::cout << "║       Blokus Duo Game Start!        ║\n";
        std::cout << "╚══════════════════════════════════════╝\n";
        std::cout << "\n";
        std::cout << "Player 1 (X): " << player1->get_name() << "\n";
        std::cout << "Player 2 (O): " << player2->get_name() << "\n";
        std::cout << "\n";
        std::cout << "Player 1 starts at (4,4)\n";
        std::cout << "Player 2 starts at (9,9)\n";

        if (verbose) {
            display_game_state();
        }

        int max_turns = 1000; // 無限ループ防止
        int turn_count = 0;

        while (!state.is_game_over() && turn_count < max_turns) {
            IPlayer* current = (state.current_player == PLAYER_1) ? player1.get() : player2.get();

            Move move = current->select_move(state, pieces);

            if (!state.is_valid_move(move, pieces)) {
                std::cerr << "Invalid move from " << current->get_name() << "! Forcing pass.\n";
                move = Move(); // パスに変更
            }

            if (verbose) {
                display_move(move, current->get_name());
            }

            state.apply_move(move, pieces);

            if (verbose && !state.is_game_over()) {
                display_game_state();
            }

            turn_count++;
        }

        // ゲーム終了
        std::cout << "\n";
        std::cout << "╔══════════════════════════════════════╗\n";
        std::cout << "║           Game Over!                ║\n";
        std::cout << "╚══════════════════════════════════════╝\n";
        std::cout << "\n";

        state.board.display();
        std::cout << "\n";

        int score1 = state.get_score(PLAYER_1);
        int score2 = state.get_score(PLAYER_2);

        std::cout << "Final Scores:\n";
        std::cout << "  " << player1->get_name() << " (X): " << score1 << " squares\n";
        std::cout << "  " << player2->get_name() << " (O): " << score2 << " squares\n";
        std::cout << "\n";

        if (score1 > score2) {
            std::cout << "🏆 Winner: " << player1->get_name() << "!\n";
        } else if (score2 > score1) {
            std::cout << "🏆 Winner: " << player2->get_name() << "!\n";
        } else {
            std::cout << "🤝 It's a tie!\n";
        }

        std::cout << "\n";
        std::cout << "Total turns: " << state.turn << "\n";
    }
};

int main(int argc, char* argv[]) {
    bool verbose = true;

    // コマンドライン引数で詳細表示を制御
    if (argc > 1 && std::string(argv[1]) == "--quiet") {
        verbose = false;
    }

    // ランダムプレイヤー同士で対戦
    auto player1 = std::make_unique<RandomPlayer>("Random Player 1", 42);
    auto player2 = std::make_unique<RandomPlayer>("Random Player 2", 123);

    Game game(std::move(player1), std::move(player2), verbose);
    game.play();

    return 0;
}
