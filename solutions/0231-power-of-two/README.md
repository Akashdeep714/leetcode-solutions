# 🧩 231. Power of Two

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · Bit Manipulation · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/power-of-two/)

---

## 📝 Problem

Determine whether a given integer is a power of two.

---

## 💡 Intuition

A positive integer is a power of two if its only prime factor is 2. If you repeatedly divide a power of two by 2, you will eventually reach 1. If any odd factor remains that is not 1, the original number was not a power of two.

---

## 🧠 Algorithmic Pattern

> **Iterative Division**

---

## 🚀 Approach

1. Check if n is less than 1; if so, return false immediately because powers of two must be positive.
2. Check if n equals 1; if so, return true because 2^0 = 1.
3. Enter a while loop that continues as long as n is evenly divisible by 2 (n % 2 == 0).
4. In each iteration of the loop, divide n by 2.
5. After the loop finishes, check if n has been reduced to 1.
6. Return true if n is equal to 1, or false otherwise.

---

## ✅ Why This Works

Any power of two can be represented as 2^x. Dividing 2^x by 2 repeatedly x times reduces the number to 1. If a number contains any odd prime factors or is less than 1, repeated division by 2 will terminate at an odd integer greater than 1, or fail the initial condition.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n)** |
| Space | **O(1)** |

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

Repeated division allows checking factor properties iteratively, though bitwise operations can solve power-of-two checks in O(1) time without loops.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
