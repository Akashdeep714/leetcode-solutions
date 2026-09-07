# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Solve the problem using the submitted implementation.

---

## 💡 Intuition

The search space is ordered, so each comparison can eliminate roughly half of the remaining candidates.

---

## 🧠 Algorithmic Pattern

> **🔍 Binary Search**

---

## 🚀 Approach

1. Define the current search boundaries.
2. Inspect the middle position.
3. Determine which half can still contain the answer.
4. Discard the other half and continue.

---

## ✅ Why This Works

Every iteration removes about half of the remaining search space.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `N/A` |
| Memory | `47100000 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Recognize the algorithmic pattern and maintain the state required by the implementation.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
