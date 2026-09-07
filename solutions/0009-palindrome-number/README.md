# 🧩 9. Palindrome Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Determine if a given integer reads the same forwards and backwards.

---

## 💡 Intuition

A number is a palindrome if reversing its digits yields the original number. Negative numbers are automatically not palindromes due to the negative sign. By repeatedly extracting the last digit of the number using modulo operations, we can construct the reversed number mathematically.

---

## 🧠 Algorithmic Pattern

> **Math / Digit Manipulation**

---

## 🚀 Approach

1. Check if the input integer x is negative; if so, return false immediately.
2. Create a variable n initialized to x to keep track of the remaining digits without modifying x.
3. Initialize revNum to 0 to store the accumulating reversed number.
4. Enter a loop that runs while n is greater than 0.
5. Extract the last digit of n using d = n % 10.
6. Append d to revNum by calculating revNum = revNum * 10 + d.
7. Truncate the last digit from n using integer division n = n / 10.
8. After the loop, compare revNum with the original x and return true if equal, false otherwise.

---

## ✅ Why This Works

The operation `n % 10` extracts the rightmost digit (least significant). Multiplying `revNum` by 10 shifts all existing digits in the reversed number one position to the left, making room to add the extracted digit. Repeating this process until `n` reaches 0 successfully reverses all digits. Comparing the reversed number back to `x` verifies if the number is symmetric.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log10(x)) where x is the input integer. The number of iterations in the loop corresponds directly to the total number of digits in x.** |
| Space | **O(1) auxiliary space, as the algorithm only uses a constant number of primitive integer variables (n, revNum, d).** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `4` |
| Memory | `46080000` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Digits of an integer can be processed from right to left mathematically using modulo (`% 10`) for extraction and integer division (`/ 10`) for removal, avoiding the need for string conversion.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
