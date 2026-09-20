class Solution {
    public int findNumbers(int[] nums) {
        int evenCount=0;
        for(int num:nums){
            int len=String.valueOf(num).length();
            
            if(len %2==0){
                evenCount++;
            }
        }
        return evenCount;
    }
}