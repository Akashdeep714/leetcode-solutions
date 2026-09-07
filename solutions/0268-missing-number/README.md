# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Find the one missing value from an array containing distinct numbers chosen from the range 0 through n.

---

## 💡 Intuition

XOR cancels equal values. Combine the expected range with the values in the array so every present number cancels itself, leaving only the missing number.

---

## 🧠 Algorithmic Pattern

> **🔀 XOR**

---

## 🚀 Approach

1. Initialize the XOR accumulator with the required range state.
2. Traverse the array and XOR each present value into the accumulator.
3. Also XOR the corresponding range values.
4. Let equal values cancel each other through XOR.
5. Return the value left in the accumulator.

---

## ✅ Why This Works

Because x ^ x = 0 and x ^ 0 = x, every value that exists in both the range and the array cancels. The only value without a matching partner is the missing number.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `47.1 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

XOR is a useful way to find one missing value without extra storage.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
