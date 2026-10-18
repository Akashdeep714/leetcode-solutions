import java.util.*;
class Solution {
    public int myAtoi(String s) {
        int i=0;
        int num=0;

        int sign=1; // default is positive , for negative -1

        // whitespaces handle
        while(i<s.length()  && s.charAt(i) == ' '){
            i=i+1;
        }

        // signedness handle
        if(i<s.length()){
            if(s.charAt(i) == '-'){
                sign=-1;
                i=i+1;
            }else if(s.charAt(i) == '+'){
                i=i+1;
            }
        }

        // rounding and conversion
        while(i<s.length() && Character.isDigit(s.charAt(i)) ){
            int digit=s.charAt(i) - '0';

            // rounding
            if(num == Integer.MAX_VALUE / 10 ){
                if(sign == 1){
                    if(digit >= 7){
                        return Integer.MAX_VALUE;
                    }
                }else if(sign == -1){
                    if(digit >= 8){
                        return Integer.MIN_VALUE;
                    }
                }
            }

            if(num > Integer.MAX_VALUE / 10){
                if(sign == 1){
                    return Integer.MAX_VALUE;
                }else{
                    return Integer.MIN_VALUE;
                }
            }

            // conversion
            num=num * 10 + digit;
            i=i+1;
        }

        return sign*num;
    }
}