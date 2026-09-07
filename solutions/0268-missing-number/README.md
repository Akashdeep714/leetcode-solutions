# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Given an array of n distinct numbers in the range [0, n], return the only number missing from the range.

---

## 💡 Intuition

XORing a number with itself cancels it out to 0 (A ^ A = 0), and XORing any number with 0 leaves it unchanged (A ^ 0 = A). If we XOR all expected numbers from 0 to n together with all numbers present in the array, every number that exists in the array will appear twice and cancel out, leaving only the missing number.

---

## 🧠 Algorithmic Pattern

> **Bit Manipulation**

---

## 🚀 Approach

1. Initialize a variable `xor` with `nums.length` (representing n).
2. Loop through the array using index `i` from 0 to `nums.length - 1`.
3. In each iteration, update `xor` by XORing it with both the current index `i` and the array element `nums[i]`.
4. After the loop finishes, return `xor`, which now holds the single missing number.

---

## ✅ Why This Works

The expected set of numbers is {0, 1, ..., n}. The array `nums` has indices 0 through n-1 and contains all expected values except the missing one. By initializing `xor` to n and accumulating `i ^ nums[i]` for each index, every present number is XORed exactly twice (once as an index or initial value n, and once as an array element). Due to XOR commutativity and self-cancellation, all matched pairs reduce to 0, leaving only the missing number.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n), where n is the length of `nums`. The solution performs a single linear pass over the array.** |
| Space | **O(1) auxiliary space, as it only uses a single integer variable (`xor`) to compute the result.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `N/A` |
| Memory | `47100000` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using the self-canceling property of the bitwise XOR operator allows you to detect missing or unique elements across two collections in O(n) time and O(1) space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
