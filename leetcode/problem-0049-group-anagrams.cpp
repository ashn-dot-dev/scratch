#include <algorithm>
#include <cstdio>
#include <map>
#include <string>
#include <vector>

std::vector<std::vector<std::string>>
group_anagrams(std::vector<std::string>& strs)
{
    std::map<std::string, std::vector<std::string>> anagrams;

    for (size_t i = 0; i < strs.size(); ++i) {
        auto s = strs[i];
        std::sort(s.begin(), s.end());
        anagrams[s].push_back(strs[i]);
    }

    auto result = std::vector<std::vector<std::string>>{};
    for (auto const& [key, value] : anagrams) {
        result.push_back(value);
    }
    return result;
}

int
main(void)
{
    auto test = [](std::vector<std::string> strs) {
        for (size_t i = 0; i < strs.size(); ++i) {
            if (i != 0) {
                std::printf(", ");
            }
            std::printf("\"%s\"", strs[i].c_str());
        }

        std::printf(" => ");

        auto result = group_anagrams(strs);
        std::printf("[");
        for (size_t i = 0; i < result.size(); ++i) {
            if (i != 0) {
                std::printf(", ");
            }
            std::printf("[");
            for (size_t j = 0; j < result[i].size(); ++j) {
                if (j != 0) {
                    std::printf(", ");
                }
                std::printf("\"%s\"", result[i][j].c_str());
            }
            std::printf("]");
        }
        std::printf("]\n");
    };

    test({"eat", "tea", "tan", "ate", "nat", "bat"});
}
