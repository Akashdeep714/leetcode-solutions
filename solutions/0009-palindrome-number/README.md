# 🧩 9. Palindrome Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Determine whether an integer reads the same forward and backward.

---

## 💡 Intuition

The solution works directly with the digits. It repeatedly takes the last digit and uses it to build the number in reverse, then compares the result with the original value.

---

## 🧠 Algorithmic Pattern

> **🔢 Digit Manipulation**

---

## 🚀 Approach

1. Keep the original value available for the final comparison.
2. Extract the last digit using modulo 10.
3. Append that digit to the reversed number.
4. Remove the processed digit using integer division by 10.
5. Compare the reversed number with the original value.

---

## ✅ Why This Works

Reversing all digits produces exactly the number obtained by reading the input from right to left. The two values are equal exactly when the input is a palindrome.

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
| Memory | `46.1 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Modulo and integer division are enough to inspect and reverse digits without converting the number to a string.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
