class Solution {
    public String longestCommonPrefix(String[] strs) {
        int minLen=strs[0].length();

        for(int i=0;i< strs.length-1;i++){
            String first= strs[i];
            String second=strs[i+1];
            int j=0;
            int min=Math.min(strs[i].length(),strs[i+1].length());

            while(j<min){
                if(strs[i].charAt(j) != strs[i+1].charAt(j)){
                    break;
                }
                if(j == minLen){
                    break;
                }
                j++;
            }
            minLen=Math.min(minLen,j);
        }
        return strs[0].substring(0,minLen);
    }
}