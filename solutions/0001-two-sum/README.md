# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Find the indices of two distinct numbers in an array that sum up to a specified target value.

---

## 💡 Intuition

To find two numbers that sum up to the target, we can exhaustively test every possible pair of elements in the array until we find the pair that matches.

---

## 🧠 Algorithmic Pattern

> **Brute Force**

---

## 🚀 Approach

1. Initialize an integer array `arr` of size 2 to hold the result indices.
2. Iterate through the array with an outer loop index `i` from 0 to `nums.length - 1`.
3. For each `i`, iterate through subsequent elements with an inner loop index `j` from `i + 1` to `nums.length - 1` to avoid pairing an element with itself.
4. Check if the sum `nums[i] + nums[j]` equals `target`.
5. If a match is found, assign `i` to `arr[0]` and `j` to `arr[1]`.
6. Return `arr` containing the matching pair of indices.

---

## ✅ Why This Works

The algorithm uses two nested loops to check all unique pairs of indices `(i, j)` where `i < j`. Since the problem guarantees exactly one valid pair exists, exhaustively checking every pair ensures that the target sum will be detected and its indices recorded.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `52` |
| Memory | `47024000` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

While a brute force approach with nested loops guarantees finding the solution by testing all O(n^2) pairs in O(1) extra space, this problem can be optimized to O(n) time using a hash map.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
