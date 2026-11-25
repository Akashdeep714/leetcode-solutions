class Solution {
    public int sumOfSquaresOfDigits(int n){
        int sum = 0;
        while(n != 0){
            int digit = n % 10;
            n = n / 10;
            sum = sum +(digit * digit);
        }
        return sum;
    }

    public boolean isHappy(int n) {
        // approach 1
        Set <Integer> set = new HashSet<>();

        while(n != 1){
            if(set.contains(n)){
                return false;
            }
            set.add(n);

            n = sumOfSquaresOfDigits(n); 
        }
        return true;
    }
}