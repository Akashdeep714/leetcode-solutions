class Solution {
    public String longestCommonPrefix(String[] strs) {
        int minLen=strs[0].length();

        for(String str:strs){
            minLen = Math.min(minLen,str.length());
        }

        int i=0;
        while(i<minLen){
            int j=0;
        
            while(j < strs.length){
                if(strs[0].charAt(i) != strs[j].charAt(i)){
                    return strs[0].substring(0,i);
                }
                j++;
            }
            i++;
        }
        return strs[0].substring(0,i);
    }
}