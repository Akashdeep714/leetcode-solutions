# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Find the indices of two distinct elements in an array that add up to a specified target integer.

---

## 💡 Intuition

Check every possible pair of elements in the array one by one until you find the combination whose sum equals the target.

---

## 🧠 Algorithmic Pattern

> **Brute Force / Nested Loops**

---

## 🚀 Approach

1. Initialize an integer array of size 2 to hold the pair of result indices.
2. Start an outer loop with index `i` running from `0` to the end of the array.
3. Start an inner loop with index `j` running from `i + 1` to the end of the array to avoid picking the same element twice.
4. Check if the sum of `nums[i]` and `nums[j]` is equal to `target`.
5. If a match is found, record `i` and `j` into the result array.
6. Return the result array containing the two indices once the iterations complete.

---

## ✅ Why This Works

The algorithm systematically evaluates every unique pair of indices `(i, j)` where `i < j`. Because the problem guarantees exactly one valid pair exists, testing all unique pairs ensures that the correct indices will be evaluated, saved, and returned.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n²), where n is the length of the `nums` array. The nested loops perform n * (n - 1) / 2 total additions and comparisons in the worst case.** |
| Space | **O(1) auxiliary space, as only a fixed-size array of length 2 is allocated regardless of the input size.** |

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

The brute force approach guarantees finding the solution by exhaustively testing all pairs in O(n²) time. It serves as a simple starting baseline before applying optimizations like hash maps to reduce time complexity to O(n).

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
