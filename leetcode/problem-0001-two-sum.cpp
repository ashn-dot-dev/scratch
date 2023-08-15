#include <cassert>
#include <cstdio>
#include <vector>

std::vector<int>
two_sum(std::vector<int>& nums, int target)
{
    for (size_t i = 0; i < nums.size(); ++i) {
        for (size_t j = i + 1; j < nums.size(); ++j) {
            if (nums[i] + nums[j] == target) {
                std::vector<int> result;
                result.push_back(i);
                result.push_back(j);
                return result;
            }
        }
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
