class Solution {
    public boolean isAnagram(String s, String t) {
        int [] freq= new int[26];

        for(char c :s.toCharArray()){
            int idx= c -'a';
            freq[idx]=freq[idx]+1;
        }

        for(char c:t.toCharArray()){
            int idx= c -'a';
            freq[idx]=freq[idx]-1;
        }

        for(int i=0; i<26;i++){
            if(freq[i] !=0){
                return false;
            }
        }
        return true;
    }
}