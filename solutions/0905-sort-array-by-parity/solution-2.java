class Solution {
    public int[] sortArrayByParity(int[] nums) {
        int [] res=new int[nums.length];
        int idx=0;
        for(int i=0;i<nums.length;i++){
            if(nums[i]%2==0){
                res[idx]=nums[i];
                idx++;
            }
        }
        for(int i=0;i<nums.length;i++){
            if(nums[i]%2==1){
                res[idx]=nums[i];
                idx++;
            }
        }
        return res;
    }
}