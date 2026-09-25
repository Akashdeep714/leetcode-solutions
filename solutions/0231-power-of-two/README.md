# 🧩 231. Power of Two

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · Bit Manipulation · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/power-of-two/)

---

## 📝 Problem

Determine whether a given integer n is a power of two.

---

## 💡 Intuition

A positive integer is a power of two if repeatedly dividing it by 2 yields 1 without encountering any odd factor greater than 1.

---

## 🧠 Algorithmic Pattern

> **Iterative Division / Math**

---

## 🚀 Approach

1. Return false immediately if n <= 0, as non-positive numbers cannot be powers of two.
2. Iteratively divide n by 2 as long as n is even (n % 2 == 0).
3. After loop termination, check if the remaining value of n is 1.
4. Return true if n == 1; otherwise, return false.

---

## ✅ Why This Works

Any positive integer can be represented as n = 2^x * m, where m is an odd number. Repeatedly dividing by 2 strips the 2^x factor. If m equals 1, then original n was purely a power of two.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n) — In the worst case, n is divided by 2 in each iteration, running at most log2(n) times.** |
| Space | **O(1) — The algorithm operates using only a constant number of primitive state variables without extra memory allocation.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `42.7 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Repeated division reduces the input size exponentially each step, leading to logarithmic time execution without extra memory.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
