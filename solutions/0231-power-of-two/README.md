# 🧩 231. Power of Two

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · Bit Manipulation · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/power-of-two/)

---

## 📝 Problem

Determine if a given integer is a power of two.

---

## 💡 Intuition

Any positive power of two can be repeatedly halved until it equals 1. If a number stops being divisible by 2 before reaching 1, it contains an odd factor and cannot be a power of two.

---

## 🧠 Algorithmic Pattern

> **Iterative Division**

---

## 🚀 Approach

1. Check if n is less than 1; if so, return false because non-positive numbers cannot be powers of two.
2. Check if n is equal to 1; if so, return true immediately as 2^0 = 1.
3. Repeatedly divide n by 2 in a loop while n is even (n % 2 == 0).
4. Once n is no longer divisible by 2, check if n has been reduced to 1.
5. Return true if n equals 1, or false otherwise.

---

## ✅ Why This Works

A power of two consists exclusively of prime factors of 2. By repeatedly dividing n by 2 while n is even, all factors of 2 are stripped away. If n was originally a power of two, this reduction will always leave 1. If n had any odd prime factors, the loop terminates early with n > 1.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n) because the value of n is halved in each step of the loop when n is a power of two.** |
| Space | **O(1) auxiliary space, as the reduction is performed directly on the input variable using no additional memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1` |
| Memory | `42724000` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

To test if a number is a power of a base k iteratively, continuously divide out factors of k while divisible and check if the final result is 1.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
