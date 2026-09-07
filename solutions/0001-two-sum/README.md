# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Find the indices of two numbers in an array that add up to a given target value.

---

## 💡 Intuition

Check every possible pair of elements in the array one by one using a brute-force approach until finding the pair that sums to the target.

---

## 🧠 Algorithmic Pattern

> **Brute Force / Nested Loops**

---

## 🚀 Approach

1. Initialize an integer array of size 2 to hold the resulting pair of indices.
2. Start an outer loop with index i going from 0 to the end of the array.
3. Start an inner loop with index j going from i + 1 to the end of the array to pair nums[i] with every subsequent element.
4. Check if nums[i] + nums[j] is equal to target.
5. If the sum matches target, assign index i to the first element and index j to the second element of the result array.
6. Return the result array containing the matching indices after the loops finish.

---

## ✅ Why This Works

The algorithm uses nested loops to exhaustively evaluate every unique pair of indices (i, j) where j > i. Since the problem guarantees that exactly one solution exists, this exhaustive search is guaranteed to find the pair that sums to the target.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `52 ms` |
| Memory | `47024000 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The brute-force approach requires no extra space (O(1)), but checking all pairs results in O(n^2) time complexity. This can be optimized to O(n) time using a Hash Map.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
