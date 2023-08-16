#include <algorithm>
#include <array>
#include <climits>
#include <cstdio>
#include <optional>
#include <string>

int
length_of_longest_substring(std::string s)
{
    int max = 0;

    // The value `mapping[x]` is the index of character x in s.
    std::array<std::optional<size_t>, 1 << CHAR_BIT> mapping{std::nullopt};
    size_t lo = 0;
    size_t hi = 0;
    while (hi < s.size()) {
        auto optional = mapping[s[hi]];
        if (!optional.has_value()) {
            mapping[s[hi]] = hi;
            hi += 1;
            continue;
        }

        max = std::max(max, (int)(hi - lo));

        size_t idx = optional.value();
        for (size_t i = lo; i <= idx; ++i) {
            mapping[s[i]] = std::nullopt;
        }
        lo = idx + 1;
    }

    return std::max(max, (int)(hi - lo));
}

int
main(void)
{
    auto test = [](std::string s) {
        auto length = length_of_longest_substring(s);
        std::printf("\"%s\" => %d\n", s.c_str(), length);
    };
    test("abcabcbb"); // 3
    test("bbbbb"); // 1
    test("pwwkew"); // 3
    test(" "); // 1
    test("dvdf"); // 3
    test("bpfbhmipx"); // 7
}
