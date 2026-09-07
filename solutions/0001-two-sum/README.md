# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Find the indices of two numbers in an array that add up to a specified target value.

---

## 💡 Intuition

This is a brute-force approach that tests every possible pair of numbers in the array. By systematically checking all pairs, it guarantees finding the two numbers that sum up to the target.

---

## 🧠 Algorithmic Pattern

> **Brute Force**

---

## 🚀 Approach

1. Initialize an integer array `arr` of size 2 to store the target indices.
2. Iterate through the array with an outer loop index `i` from 0 to `nums.length - 1`.
3. Iterate through the remaining elements with an inner loop index `j` starting from `i + 1` to `nums.length - 1`.
4. Check if `nums[i] + nums[j]` equals `target` for the current pair.
5. If the sum matches the target, assign `i` to `arr[0]` and `j` to `arr[1]`.
6. After completing the iterations, return the array `arr` containing the found indices.

---

## ✅ Why This Works

The nested loops check every unique pair of elements `(nums[i], nums[j])` where `i < j`. Since the problem guarantees exactly one valid solution exists, checking all combinations ensures that the matching pair will be found and its indices recorded.

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

While a brute-force double loop solves the problem in O(1) auxiliary space, checking all pairs results in O(n^2) time complexity. Using a hash map can optimize this to O(n) time by storing seen values during a single pass.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
