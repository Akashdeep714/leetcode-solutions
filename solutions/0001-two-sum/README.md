# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Given an array of integers and a target value, find the indices of two distinct numbers that add up to the target.

---

## 💡 Intuition

The most straightforward way to find the target sum is to test every possible combination of two numbers in the array until we find the pair that adds up to the target.

---

## 🧠 Algorithmic Pattern

> **Brute Force / Nested Loop Search**

---

## 🚀 Approach

1. Initialize an integer array `arr` of size 2 to store the result indices.
2. Set up an outer loop with index `i` running from `0` to `nums.length - 1` to represent the first element of the pair.
3. Set up an inner loop with index `j` starting from `i + 1` to `nums.length - 1` to represent the second distinct element.
4. Check if the sum of `nums[i]` and `nums[j]` equals `target`.
5. If the sum equals `target`, store `i` into `arr[0]` and `j` into `arr[1]`.
6. Return `arr` after searching through the pairs.

---

## ✅ Why This Works

By starting `j` at `i + 1`, the code checks every unique unordered pair of indices $(i, j)$ where $i < j$. This avoids pairing an element with itself or re-checking previously tested pairs. Since the problem guarantees exactly one valid solution exists, the condition `nums[i] + nums[j] == target` will successfully trigger for the correct pair and capture its indices.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n²) where n is the length of `nums`. The outer loop runs n times and the inner loop runs approximately n/2 times on average, performing roughly n(n - 1) / 2 comparisons in total.** |
| Space | **O(1) auxiliary space because only a fixed 2-element array is created regardless of the input size.** |

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

While a brute force nested loop approach is easy to implement and uses O(1) extra space, it takes O(n²) time complexity. Using a Hash Table can optimize this search to O(n) time.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
