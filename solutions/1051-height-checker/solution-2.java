class Solution {
    public int heightChecker(int[] heights) {
        int [] countArray=new int[101];

        for(int h:heights){
            countArray[h]++;
        }

        int count=0;
        int currHeight=1;

        for(int i=0;i<heights.length;i++){
            while(countArray[currHeight] == 0){
                currHeight++;
            }
            if(heights[i] != currHeight){
                count++;
            }
            countArray[currHeight]--;
        }
        return count;
    }
}