# 🧩 9. Palindrome Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Determine whether a given integer reads the same forwards and backwards.

---

## 💡 Intuition

Negative numbers cannot be palindromes because of the minus sign. For positive numbers, we can construct the reversed version of the number mathematically digit-by-digit and check if it equals the original number.

---

## 🧠 Algorithmic Pattern

> **Math / Digit Extraction**

---

## 🚀 Approach

1. Check if the input integer x is negative; if so, immediately return false.
2. Create a variable n initialized to x to manipulate during digit extraction, keeping x unchanged for the final comparison.
3. Initialize revNum to 0 to store the reversed integer.
4. Run a while loop that continues as long as n is greater than 0.
5. In each iteration, extract the last digit of n using n % 10, shift revNum left by multiplying it by 10, add the extracted digit, and drop the last digit from n using integer division (n / 10).
6. Compare the reversed number revNum with the original number x and return true if they are equal, or false otherwise.

---

## ✅ Why This Works

Extracting the least significant digit with modulo 10 and pushing it onto the accumulated reversed total constructs the number backwards. If the original number is a palindrome, its reverse will be identical to its original value.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `4 ms` |
| Memory | `46080000 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Integers can be reversed mathematically using modulo (% 10) for digit extraction and multiplication (* 10) for place-value shifting, avoiding the need for string conversion.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
