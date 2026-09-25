# 🧩 9. Palindrome Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Determine whether an integer reads the same forward and backward without converting it to a string.

---

## 💡 Intuition

A number is a palindrome if reversing its digits yields the exact same integer. We can extract each digit from the right using modulo division by 10 and build up the reversed integer step by step.

---

## 🧠 Algorithmic Pattern

> **Math / Modulo & Integer Arithmetic**

---

## 🚀 Approach

1. Check if the integer x is negative; if so, return false immediately because the minus sign breaks palindromic symmetry.
2. Initialize a variable revNum to 0 to store the reversed value, and create a working copy n = x.
3. Iteratively extract the last digit of n using d = n % 10, append it to revNum via revNum = revNum * 10 + d, and remove the last digit from n using n = n / 10.
4. After n reaches 0, compare revNum with the original x and return true if equal, false otherwise.

---

## ✅ Why This Works

Reconstructing the integer in reverse order captures the exact value reading from right to left. Comparing this reconstructed value against the original x directly determines if the number is symmetric.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log10(x)) — The while loop executes once for every digit in the decimal representation of x, resulting in O(log10(x)) operations (or O(1) bounded by 10 digits for a 32-bit integer).** |
| Space | **O(1) — Only a constant number of primitive variables (n, revNum, d) are allocated, maintaining O(1) auxiliary space complexity.** |

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

Digits of an integer can be extracted from right to left using modulo (% 10) and truncated using integer division (/ 10), enabling in-place reversal without string allocation.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
