#include <algorithm>
#include <cstdio>
#include <vector>

double find_median_sorted_arrays(std::vector<int>& nums1, std::vector<int>& nums2) {
    std::vector<int> nums;
    size_t i1 = 0;
    size_t i2 = 0;
    while (i1 < nums1.size() && i2 < nums2.size()) {
        if (nums1[i1] < nums2[i2]) {
            nums.push_back(nums1[i1++]);
        }
        else {
            nums.push_back(nums2[i2++]);
        }
    }
    while (i1 < nums1.size()) {
            nums.push_back(nums1[i1++]);
    }
    while (i2 < nums2.size()) {
            nums.push_back(nums2[i2++]);
    }

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
