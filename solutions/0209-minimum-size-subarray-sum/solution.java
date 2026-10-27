class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int minDis=Integer.MAX_VALUE;
        int left=0;
        int right=0;
        int runSum=0;

        while(right <nums.length){
            runSum += nums[right];
            while(runSum >= target){
                minDis=Math.min(minDis,right - left +1);
                runSum -= nums[left];
                left++;
            }
        right++;
        }
        return minDis == Integer.MAX_VALUE ? 0 : minDis;
    }
}