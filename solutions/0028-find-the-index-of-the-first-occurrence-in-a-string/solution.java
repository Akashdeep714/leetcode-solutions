class Solution {
    public int strStr(String haystack, String needle) {
        if(haystack.length() < needle.length()){
            return -1;
        }

        for(int i=0; i <haystack.length(); i++){
            int j=0;

            while(j< needle.length()  && (i+j) < haystack.length()){
                if(needle.charAt(j) != haystack.charAt(i+j)){
                    break;
                }
                j++;
            }
            if(j == needle.length()){
                return i;
            }
        }
        return -1;
    }
}