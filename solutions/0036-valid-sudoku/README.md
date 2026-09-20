# 🧩 36. Valid Sudoku

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Hash Table · Matrix  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/valid-sudoku/)

---

## 📝 Problem

Determine if a 9 x 9 Sudoku board is valid.

---

## 💡 Intuition

The implementation stores previously seen values so that a related value can be checked quickly instead of searching the earlier elements again. This trades extra memory for faster lookups.

---

## 🧠 Algorithmic Pattern

> **🗺️ Hash Map**

---

## 🚀 Approach

1. Create the map used by the submitted implementation.
2. Traverse the input from the beginning.
3. Check the map for the value or state required by the current element.
4. Use the stored information when the required condition is met.
5. Otherwise store the current value or state and continue.

---

## ✅ Why This Works

Each lookup uses the information collected from earlier elements. Because the map represents exactly the relevant values already seen, a successful lookup identifies the condition required by the algorithm.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(n)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `46.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The main idea is to recognize the 🗺️ Hash Map pattern and understand how the submitted implementation applies it to this problem.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/valid-sudoku/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
