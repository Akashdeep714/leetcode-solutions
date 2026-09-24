class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();

        for (int i = 0; i < nums.length; i = i + 1) {
            map.put(nums[i], i);
        }

        for (int i = 0; i < nums.length; i = i + 1) {
            int lookupNumber = target - nums[i];

            if (map.containsKey(lookupNumber) && map.get(lookupNumber) != i) {
                return new int[] {
                    map.get(lookupNumber),
                    i
                };
            }
        }

        return new int[] {-1, -1};
    }
}