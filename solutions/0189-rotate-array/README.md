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

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/rotate-array/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
