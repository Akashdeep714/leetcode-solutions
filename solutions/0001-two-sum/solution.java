class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();

        for (int i = 0; i < nums.length; i = i + 1){
        int lookupNumber = target - nums[i];

        if (map.containsKey(lookupNumber)){
            return new int[] {
                i,
                map.get(lookupNumber)
            };
        }
        map.put(nums[i], i);
        }
        return new int[] {-1, -1};   
    }
}