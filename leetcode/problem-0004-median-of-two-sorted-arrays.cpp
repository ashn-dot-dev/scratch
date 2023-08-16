#include <algorithm>
#include <cstdio>
#include <vector>

double find_median_sorted_arrays(std::vector<int>& nums1, std::vector<int>& nums2) {
    std::vector<int> nums;
    nums.insert(nums.end(), nums1.begin(), nums1.end());
    nums.insert(nums.end(), nums2.begin(), nums2.end());
    std::sort(nums.begin(), nums.end());

    if (nums.size() % 2 == 0) {
        auto lo = nums[nums.size() / 2 - 1];
        auto hi = nums[nums.size() / 2];
        return (double)(lo + hi) / 2;
    }

    return nums[nums.size() / 2];
}

int main(void)
{
    auto test = [](std::vector<int> nums1, std::vector<int> nums2) {
        std::printf("%f\n", find_median_sorted_arrays(nums1, nums2));
    };
    test({1, 3}, {2});
    test({1, 2}, {3, 4});
}
