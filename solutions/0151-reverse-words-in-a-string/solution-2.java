class Solution {
    public String reverseWords(String s) {
        // approach 2
        // "  hello world "
        int left=0;
        int right=s.length()-1;

        while(left < s.length() && s.charAt(left) == ' '){
            left++;
        }

        while(right >= 0 && s.charAt(right) == ' '){
            right--;
        }
        // "  hello world  "
        //    l         r
        // sB=hello
        StringBuilder sB= new StringBuilder();

        while(left <= right){
            if(s.charAt(left) != ' '){
                sB.append(s.charAt(left));
            }else if(sB.charAt(sB.length()-1) != ' '){
                    sB.append(s.charAt(left));
            }

            left++;
        }
        // sB=hello world
        int i=0;
        int j=sB.length()-1;
        
        while(i<j){
            char temp=sB.charAt(i);
            sB.setCharAt(i,sB.charAt(j));
            sB.setCharAt(j,temp);

            i++;
            j--;
        }
        // sB=dlrow olleh
        //    s
        //         e

        int start=0;
        int end=0;

        while(start < sB.length()){
            while(end <sB.length() && sB.charAt(end) != ' '){
                end++;
            }
            // reverse between  s and e-1
            i= start;
            j= end - 1;
            while(i<j){
                char temp=sB.charAt(i);
                sB.setCharAt(i,sB.charAt(j));
                sB.setCharAt(j,temp);

                i++;
                j--;
            }

            start=end + 1;
            end=end + 1;
        }
        
        return sB.toString();
    }
}