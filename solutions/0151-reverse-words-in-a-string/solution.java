class Solution {
    public String reverseWords(String s) {
        // approach 1
        // "   hello world  "
        String trim= s.trim();
        // "hello world"
        String [] arrStr=trim.split("\\s+");
        // ["hello","world"]
        List <String> listStr= Arrays.asList(arrStr);
        // <"hello","world">
        Collections.reverse(listStr);
        // <"world",:"hello">
        return String.join(" ",listStr);
    }
}