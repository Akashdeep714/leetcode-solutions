# 🧩 231. Power of Two

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · Bit Manipulation · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/power-of-two/)

---

## 📝 Problem

Determine whether a given integer n can be expressed as a power of two (n = 2^x for an integer x).

---

## 💡 Intuition

A power of two consists purely of prime factor 2 (e.g., 1, 2, 4, 8, 16...). If we repeatedly divide a positive number by 2 as long as it remains even, a true power of two will eventually strip down to exactly 1. If any odd number greater than 1 remains, it is not a power of two.

---

## 🧠 Algorithmic Pattern

> **Iterative Division**

---

## 🚀 Approach

1. Check if n is less than 1; if so, return false immediately because powers of two must be positive.
2. Check if n equals 1; if so, return true because 2^0 = 1.
3. If n is greater than 1, enter a loop that runs as long as n is evenly divisible by 2 (n % 2 == 0).
4. Inside the loop, divide n by 2 (n = n / 2) to strip away factors of 2.
5. After the loop finishes, check if the remaining value of n is 1.
6. Return true if n equals 1, and false otherwise.

---

## ✅ Why This Works

Repeatedly dividing n by 2 removes all factors of 2. If n was originally a power of two (2^x), dividing by 2 exactly x times reduces n to 1. If n contained any prime factor other than 2, removing all 2s will leave an odd number greater than 1, causing n == 1 to evaluate to false.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n) because the number n is divided by 2 in each iteration, performing at most log2(n) steps.** |
| Space | **O(1) as the algorithm uses only a few integer checks and modifies the input variable in place without allocating extra memory.** |

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

Repeated division by a base is a fundamental way to check if a number is a power of that base, by continuously stripping away factors until reaching 1 or encountering an indivisible remainder.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
