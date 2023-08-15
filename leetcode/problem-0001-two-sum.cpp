#include <cassert>
#include <cstdio>
#include <unordered_map>
#include <vector>

std::vector<int>
two_sum(std::vector<int>& nums, int target)
{
    std::unordered_map<int, size_t> map{};

    for (size_t i = 0; i < nums.size(); ++i) {
        auto found = map.find(target - nums[i]);
        if (found != map.end()) {
            return {(int)found->second, (int)i};
        }
        map[nums[i]] = i;
    }

    assert(false);
}

int
main(void)
{
    auto test = [](std::vector<int> nums, int target) {
        for (size_t i = 0; i < nums.size(); ++i) {
            if (i != 0) {
                std::printf(", ");
            }
            std::printf("%d", nums[i]);
        }
        auto result = two_sum(nums, target);
        std::printf(
            " summing to %d => indices %d and %d\n",
            target,
            result[0],
            result[1]);
    };

    test(std::vector<int>{2, 7, 11, 15}, 9);
    test(std::vector<int>{3, 2, 4}, 6);
}
