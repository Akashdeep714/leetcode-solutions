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
    // approach 2
    // floyd cycle detection algorithm
    int slow = n;
    int fast = n;

    while(true){
        slow = sumOfSquaresOfDigits(slow);
        fast = sumOfSquaresOfDigits(sumOfSquaresOfDigits(fast));
                
            if(fast == 1){
                return true;
            }

            if(slow == fast){
                return false;
            }  
        }
    }
}