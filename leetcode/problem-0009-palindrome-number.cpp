#include <cstdio>
#include <string>

bool
is_palindrome(int x)
{
    auto s = std::to_string(x);
    size_t lo = 0;
    size_t hi = s.size() - 1;
    while (lo < hi) {
        if (s[lo] != s[hi]) {
            return false;
        }

        lo += 1;
        hi -= 1;
    }

    return true;
}

int
main(void)
{
    auto test = [](int x) {
        auto s = std::to_string(x);
        std::printf(
            "\"%s\" => %s\n", s.c_str(), is_palindrome(x) ? "true" : "false");
    };

    test(0);
    test(1);
    test(121);
    test(123);
    test(1221);
    test(1223);
}
