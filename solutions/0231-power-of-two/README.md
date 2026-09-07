# 🧩 231. Power of Two

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · Bit Manipulation · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/power-of-two/)

---

## 📝 Problem

Determine whether an integer is a power of two.

---

## 💡 Intuition

Powers of two can be reduced by dividing by two repeatedly. A valid power reaches 1 without leaving a remainder at any step.

---

## 🧠 Algorithmic Pattern

> **🔁 Repeated Division / Recursion**

---

## 🚀 Approach

1. Reject values that are not positive.
2. Repeatedly reduce the value according to the submitted implementation.
3. Check that each required division is valid.
4. Accept the number when the process reaches the valid base case.

---

## ✅ Why This Works

Every positive power of two can be reduced to 1 by repeatedly dividing by two exactly, while any other positive integer eventually leaves a remainder or fails the base condition.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n)** |
| Space | **O(1)** |

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

Repeated division works because the exponent determines how many times the value can be divided by two before reaching 1.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
