class Solution {
    public void reverse(char[] arr,int start,int end){
        while(start < end){
            char temp=arr[start];
            arr[start]=arr[end];
            arr[end]=temp;
            start++;
            end--;
        }
    }
    public String reverseWords(String s) {
        char[] charArr=s.toCharArray();

        int start=0;
        int end=0;

        while(start < charArr.length){
            while(end < charArr.length && charArr[end] != ' '){
                end++;
            }

            reverse(charArr,start,end - 1);
            start= end + 1;
            end= end + 1;
        }
        return new String(charArr);
    }
}