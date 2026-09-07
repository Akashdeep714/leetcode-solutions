# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Given an array of n distinct numbers in the range [0, n], identify and return the single number from the range that is missing.

---

## 💡 Intuition

XORing a number with itself cancels it out to 0 (A ^ A = 0), while XORing a number with 0 leaves it unchanged (A ^ 0 = A). If we XOR all full range numbers from 0 to n together with all numbers in the array, every number present in both sets will appear twice and cancel out, leaving only the missing number.

---

## 🧠 Algorithmic Pattern

> **Bit Manipulation**

---

## 🚀 Approach

1. Initialize a variable `xor` with `nums.length` (representing $n$).
2. Loop through the array with index `i` from `0` to `nums.length - 1`.
3. In each step, update `xor` by XORing it with both the index `i` and the value `nums[i]`.
4. Allow all paired numbers present in both the indices and the array values to cancel each other out.
5. Return the final value of `xor`, which is the unmatched missing number.

---

## ✅ Why This Works

The indices `0` to `n-1` combined with the initial `xor` value of `n` represent the complete set of expected numbers $[0, n]$. The array `nums` contains $n$ numbers from $[0, n]$ with exactly one missing. Because XOR is commutative and associative, all elements present in `nums` pair up with their matching range numbers and reduce to 0, leaving only the single missing number.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n), where n is the length of `nums`. The algorithm makes a single pass through the array, performing constant-time bitwise operations in each iteration.** |
| Space | **O(1) auxiliary space, as the algorithm only uses a single integer variable (`xor`) to track the result.** |

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

Using the XOR property $A \oplus A = 0$ allows us to detect missing or unique elements in a single pass using $O(1)$ extra space, avoiding any potential integer overflow issues present in summation approaches.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
