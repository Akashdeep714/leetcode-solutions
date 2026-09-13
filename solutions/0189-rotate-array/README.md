# 🧩 189. Rotate Array

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Math · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/rotate-array/)

---

## 📝 Problem

Rotate an array of integers to the right by k steps in-place.

---

## 💡 Intuition

Rotating an array of length n to the right by k steps moves the last k elements to the front and shifts the first n - k elements to the back. Notice that if we reverse the entire array, the last k elements move to the front and the first n - k elements move to the back, but both segments end up upside down (reversed). By reversing the first k elements back and then reversing the remaining n - k elements back, each block returns to its correct relative ordering while staying in its new location. Additionally, rotating by k steps when k >= n is equivalent to rotating by k % n steps, so we simplify k first.

---

## 🧠 Algorithmic Pattern

> **Two Pointers (Array Reversal)**

---

## 🚀 Approach

1. Calculate the length n of the array nums.
2. Check if k % n == 0. If so, rotating by k steps leaves the array unchanged, so return early.
3. Update k to k % n to handle cases where k is greater than the array length.
4. Call the helper function rev(nums, 0, n - 1) to reverse the entire array from index 0 to n - 1 using two pointers (start and end) swapping elements until they meet.
5. Call rev(nums, 0, k - 1) to reverse the first k elements back into their original relative order.
6. Call rev(nums, k, n - 1) to reverse the remaining n - k elements back into their original relative order.

---

## ✅ Why This Works

When the entire array of size n is reversed, the block of elements originally at indices [n - k, n - 1] moves to indices [0, k - 1], and the block originally at indices [0, n - k - 1] moves to indices [k, n - 1]. However, within each block, elements are in reverse order. Reversing index range [0, k - 1] restores the correct relative sequence of the k elements now at the front. Reversing index range [k, n - 1] restores the correct relative sequence of the n - k elements at the end, completing the right rotation in-place without extra memory.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `5 ms` |
| Memory | `268.9 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

An array right-rotation by k steps can be achieved in O(n) time and O(1) space by reversing the entire array and then reversing the two sub-arrays [0, k - 1] and [k, n - 1] independently.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/rotate-array/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
