class Solution {
    public int arrayPairSum(int[] nums) {
        int k=10000;
        int [] countArr=new int[2*k+1];

        for(int i=0;i<nums.length;i++){
            countArr[nums[i]+k]++;
        }

        boolean isEvenIndex=true;
        int maxSum=0;

        for(int i=0;i<2*k+1;i++){
            while(countArr[i] > 0){
                maxSum=maxSum+(isEvenIndex ? (i-k) : 0);
                countArr[i]--;
                isEvenIndex = !isEvenIndex;
            }
        }
        return maxSum;
    }
}