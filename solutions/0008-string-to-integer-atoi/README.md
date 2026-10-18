# 🧩 8. String to Integer (atoi)

> **Difficulty:** 🟡 Medium  
> **Topics:** String  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/string-to-integer-atoi/)

---

## 📝 Problem

Convert a string to a 32-bit signed integer following specific rules for whitespace, signs, non-digit stopping conditions, and range clamping.

---

## 💡 Intuition

To process the string safely without causing 32-bit integer overflow, we can parse the characters sequentially in a single pass. Before appending each digit to our running total, we verify whether multiplying the current value by 10 and adding the digit would exceed 32-bit signed integer limits.

---

## 🧠 Algorithmic Pattern

> **Linear Scan / String Parsing**

---

## 🚀 Approach

1. Skip leading whitespace characters by advancing the pointer.
2. Check for an optional sign character ('+' or '-') and record the sign modifier.
3. Iterate over digit characters, converting each character to its numerical value.
4. Before modifying the running total, check if 'num > Integer.MAX_VALUE / 10' or if 'num == Integer.MAX_VALUE / 10' with a trailing digit that would cause overflow. If overflow would occur, immediately return Integer.MAX_VALUE or Integer.MIN_VALUE depending on the sign.
5. Update the running total using 'num = num * 10 + digit' and multiply by the sign at the end if valid.

---

## ✅ Why This Works

By checking `num > MAX_VALUE / 10` before multiplying by 10, we prevent arithmetic wrap-around in a strict 32-bit signed integer environment. The single-pass state parsing correctly enforces the problem rules regarding leading spaces, signs, and early non-digit termination.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — We iterate through the input string of length N at most once, performing O(1) operations per character.** |
| Space | **O(1) — Only a few primitive variables are used to keep track of the pointer index, sign, and current numeric value, requiring O(1) auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `43.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When performing numerical string conversion without using floating-point or wider integer types, check bounds before performing arithmetic operations that could overflow.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/string-to-integer-atoi/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
