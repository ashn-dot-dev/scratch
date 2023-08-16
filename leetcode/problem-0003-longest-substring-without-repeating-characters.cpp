#include <algorithm>
#include <cstdio>
#include <string>
#include <map>

int
length_of_longest_substring(std::string s)
{
    int max = 0;
    std::map<char, size_t> map;
    size_t lo = 0;
    size_t hi = 0;
    while (hi < s.size()) {
        auto [iter, inserted] = map.insert({s[hi], hi});
        if (inserted) {
            hi += 1;
            continue;
        }

        max = std::max(max, (int)map.size());

        size_t idx = iter->second;
        for (size_t i = lo; i <= idx; ++i) {
            map.erase(s[i]);
        }
        lo = idx + 1;
        continue;
    }

    return std::max(max, (int)map.size());
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
