# 🧩 28. Find the Index of the First Occurrence in a String

> **Difficulty:** 🟢 Easy  
> **Topics:** Two Pointers · String · String Matching · Z Algorithm · Knuth–Morris–Pratt Algorithm · Boyer–Moore String-Search Algorithm  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)

---

## 📝 Problem

Find the index of the first occurrence of needle in haystack, or return -1 if needle is not present.

---

## 💡 Intuition

Try every starting index in haystack and check character by character if needle matches starting at that position.

---

## 🧠 Algorithmic Pattern

> **Brute Force / Sliding Window**

---

## 🚀 Approach

1. Check if haystack is shorter than needle; if so, return -1 immediately.
2. Iterate over possible starting indices i in haystack.
3. For each index i, compare characters of needle with haystack sequentially using a second pointer j.
4. If a character mismatch occurs, stop checking the current position and move to the next starting index i.
5. If all characters of needle match (j reaches needle.length()), return the starting index i.
6. If the loops terminate without finding a match, return -1.

---

## ✅ Why This Works

Checking every candidate starting index exhaustively guarantees that the first matching position will be discovered if it exists.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N * M) — Let N be haystack.length() and M be needle.length(). In the worst case, the outer loop runs up to N times and the inner loop checks M characters, yielding O(N * M) time complexity.** |
| Space | **O(1) — Only a few primitive loop variables are used, operating directly on the input strings without allocating auxiliary memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `191 ms` |
| Memory | `42.7 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The naive string search approach requires no additional memory, but worst-case performance is quadratic when many partial matches occur.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
