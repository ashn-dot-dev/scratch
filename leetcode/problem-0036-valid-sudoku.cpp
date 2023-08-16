#include <array>
#include <bitset>
#include <cassert>
#include <cstdio>
#include <vector>

// NOTE: int is faster than std::bitset<9>
typedef int digit_set;

constexpr int
char_to_digit_set_bit(char ch)
{
    return 1 << (ch - '0');
}

bool
is_valid_sudoku(std::vector<std::vector<char>>& board)
{
    std::array<digit_set, 9> col_digits{};
    for (size_t row = 0; row < board.size(); ++row) {
        digit_set row_digits{};
        for (size_t col = 0; col < board.size(); ++col) {
            auto ch = board[row][col];
            if (ch == '.') {
                continue;
            }

            auto bit = char_to_digit_set_bit(ch);
            if (row_digits & bit) {
                return false;
            }
            row_digits |= bit;
            if (col_digits[col] & bit) {
                return false;
            }
            col_digits[col] |= bit;
        }
    }

    // Check sub-boxes.
    auto check_sub_box = [&board](size_t r, size_t c) {
        digit_set digits{};
        for (size_t row = r; row < r + 3; ++row) {
            for (size_t col = c; col < c + 3; ++col) {
                auto ch = board[row][col];
                if (ch == '.') {
                    continue;
                }

                auto bit = char_to_digit_set_bit(ch);
                if (digits & bit) {
                    return false;
                }
                digits |= bit;
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
