# 🧩 189. Rotate Array

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Math · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/rotate-array/)

---

## 📝 Problem

Given an integer array nums , rotate the array to the right by k steps, where k is non-negative.

---

## 💡 Intuition

Two positions are maintained so the algorithm can eliminate unnecessary comparisons while scanning the input.

---

## 🧠 Algorithmic Pattern

> **👉 Two Pointers**

---

## 🚀 Approach

1. Initialize the two pointers.
2. Compare the values at the current positions.
3. Move the appropriate pointer according to the problem condition.
4. Continue until the search space is exhausted or the answer is found.

---

## ✅ Why This Works

The pointers move through the input without repeatedly revisiting eliminated candidates.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `8 ms` |
| Memory | `268.7 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The main idea is to recognize the 👉 Two Pointers pattern and understand how the submitted implementation applies it to this problem.

---

---
### 🔀 Solution 2 — Two Pointers

> **Language:** Java  
> **Runtime:** `5 ms`  
> **Memory:** `268.6 MB`

#### 💡 Intuition

Rotating an array to the right by k steps means the last k elements move to the front, and the first n - k elements shift to the back. Since k can be larger than the array length n, rotating by k is equivalent to rotating by k % n; if k % n is 0, the array remains unchanged. Reversing the entire array moves the last k elements to the front and the first n - k elements to the back, but leaves both groups in reverse order. Reversing the first k elements restores their original relative order, and reversing the remaining n - k elements restores theirs, achieving the right rotation in-place without extra memory.

#### 🧠 Algorithmic Pattern

> **Two Pointers**

#### 🚀 Approach

1. Determine the array length n = nums.length.
2. Check if k % n == 0; if true, returning early leaves the array unchanged since full cycles result in the same array.
3. Update k to k % n to handle cases where k is greater than n.
4. Call the helper function rev(nums, 0, n - 1) to reverse the entire array in-place using two pointers start and end.
5. Call rev(nums, 0, k - 1) to reverse the first k elements, placing them in their correct rotated order.
6. Call rev(nums, k, n - 1) to reverse the remaining n - k elements, restoring their original relative order at the back of the array.

#### ✅ Why This Works

Reversing the whole array swaps the suffix of length k (originally from index n - k to n - 1) into the prefix positions [0, k - 1], and the prefix of length n - k into positions [k, n - 1], though both sections end up internally inverted. Reversing the prefix [0, k - 1] flips the first k elements back to their original left-to-right order, and reversing the suffix [k, n - 1] flips the remaining elements back to their original order, successfully completing the right rotation.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The three reversal passes process at most 2n elements in total, which runs in O(n) time.** |
| Space | **O(1) — All element swaps are performed directly on the input array using a few primitive variables, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/rotate-array/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
