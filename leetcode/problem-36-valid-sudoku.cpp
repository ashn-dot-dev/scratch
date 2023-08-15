#include <array>
#include <cassert>
#include <cstdio>
#include <vector>

// Small set.
//
// Faster than std::set and std::unordered_set for the maximum of 9 characters
// that will be inserted.
class digit_set {
    std::array<char, 9> digits = {0};

public:
    bool insert(char ch)
    {
        for (size_t i = 0; i < this->digits.size(); ++i) {
            if (this->digits[i] == 0) {
                this->digits[i] = ch;
                return true;
            }

            if (this->digits[i] == ch) {
                return false;
            }
        }

        assert(false);
    }
};

bool
is_valid_sudoku(std::vector<std::vector<char>>& board)
{
    std::array<digit_set, 9> col_digits{};
    for (size_t row = 0; row < board.size(); ++row) {
        digit_set row_digits;
        for (size_t col = 0; col < board.size(); ++col) {
            auto ch = board[row][col];
            if (ch == '.') {
                continue;
            }

            auto row_inserted = row_digits.insert(ch);
            if (!row_inserted) {
                return false;
            }

            auto col_inserted = col_digits[col].insert(ch);
            if (!col_inserted) {
                return false;
            }
        }
    }

    // Check sub-boxes.
    auto check_sub_box = [&board](size_t r, size_t c) {
        digit_set digits;
        for (size_t row = r; row < r + 3; ++row) {
            for (size_t col = c; col < c + 3; ++col) {
                auto ch = board[row][col];
                if (ch == '.') {
                    continue;
                }

                auto inserted = digits.insert(ch);
                if (!inserted) {
                    return false;
                }
            }
        }

        return true;
    };
    return check_sub_box(0, 0) && check_sub_box(0, 3) && check_sub_box(0, 6)
        && check_sub_box(3, 0) && check_sub_box(3, 3) && check_sub_box(3, 6)
        && check_sub_box(6, 0) && check_sub_box(6, 3) && check_sub_box(6, 6);
}

int
main(void)
{
    std::vector<std::vector<char>> example1 = {
        {'5', '3', '.', '.', '7', '.', '.', '.', '.'},
        {'6', '.', '.', '1', '9', '5', '.', '.', '.'},
        {'.', '9', '8', '.', '.', '.', '.', '6', '.'},
        {'8', '.', '.', '.', '6', '.', '.', '.', '3'},
        {'4', '.', '.', '8', '.', '3', '.', '.', '1'},
        {'7', '.', '.', '.', '2', '.', '.', '.', '6'},
        {'.', '6', '.', '.', '.', '.', '2', '8', '.'},
        {'.', '.', '.', '4', '1', '9', '.', '.', '5'},
        {'.', '.', '.', '.', '8', '.', '.', '7', '9'}};
    std::printf(
        "EXAMPLE 1: %s\n", is_valid_sudoku(example1) ? "true" : "false");

    std::vector<std::vector<char>> example2 = {
        {'8', '3', '.', '.', '7', '.', '.', '.', '.'},
        {'6', '.', '.', '1', '9', '5', '.', '.', '.'},
        {'.', '9', '8', '.', '.', '.', '.', '6', '.'},
        {'8', '.', '.', '.', '6', '.', '.', '.', '3'},
        {'4', '.', '.', '8', '.', '3', '.', '.', '1'},
        {'7', '.', '.', '.', '2', '.', '.', '.', '6'},
        {'.', '6', '.', '.', '.', '.', '2', '8', '.'},
        {'.', '.', '.', '4', '1', '9', '.', '.', '5'},
        {'.', '.', '.', '.', '8', '.', '.', '7', '9'}};
    std::printf(
        "EXAMPLE 2: %s\n", is_valid_sudoku(example2) ? "true" : "false");

    std::vector<std::vector<char>> test_a = {
        {'.', '.', '.', '.', '5', '.', '.', '1', '.'},
        {'.', '4', '.', '3', '.', '.', '.', '.', '.'},
        {'.', '.', '.', '.', '.', '3', '.', '.', '1'},
        {'8', '.', '.', '.', '.', '.', '.', '2', '.'},
        {'.', '.', '2', '.', '7', '.', '.', '.', '.'},
        {'.', '1', '5', '.', '.', '.', '.', '.', '.'},
        {'.', '.', '.', '.', '.', '2', '.', '.', '.'},
        {'.', '2', '.', '9', '.', '.', '.', '.', '.'},
        {'.', '.', '4', '.', '.', '.', '.', '.', '.'}};
    std::printf("TEST A: %s\n", is_valid_sudoku(test_a) ? "true" : "false");
}
