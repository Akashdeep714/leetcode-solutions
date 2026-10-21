class Solution {
    public String addBinary(String a, String b) {
        if(a.length() < b.length()){
            return addBinary(b,a);
        }

        int m= a.length();
        int n= b.length();
        int carry=0;

        StringBuilder res=new StringBuilder();
        for(int i= m-1, j= n-1; i>=0; i--,j--){
            int sum = carry;
            if(a.charAt(i)=='1'){
                sum += 1;
            }
            if(j>=0 && b.charAt(j)=='1'){
                sum += 1;
            }
            res.append(sum % 2);
            carry=sum/2;
        }
        if(carry == 1){
            res.append(1);
        }
        res.reverse();
        return res.toString();
    }
}