# 🧩 344. Reverse String

> **Difficulty:** 🟢 Easy  
> **Topics:** Two Pointers · String  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/reverse-string/)

---

## 📝 Problem

Reverse an array of characters in-place using O(1) extra memory.

---

## 💡 Intuition

To reverse a sequence in-place, the outermost elements must swap positions, followed by the second outermost elements, moving progressively toward the middle.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize two pointers: `i` at index 0 (start) and `j` at index `s.length - 1` (end).
2. Iterate while the left pointer `i` has not passed the right pointer `j`.
3. Swap the characters at `s[i]` and `s[j]` using a temporary variable `temp`.
4. Increment `i` and decrement `j` to move both pointers toward the middle.

---

## ✅ Why This Works

Swapping the elements at index `i` and `j` exchanges the $i$-th element from the front with the $i$-th element from the back. Repeating this until the pointers meet effectively mirrors the entire array.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The loop performs $n/2$ iterations, where $n$ is the length of the string array `s`. Each iteration performs constant-time swap operations, resulting in an overall time complexity of $O(n)$.** |
| Space | **O(1) — All operations modify the input array directly in-place, using only a constant amount of extra memory for two pointer indices and one temporary character variable.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `48.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using two converging pointers is the optimal strategy for in-place array reversal, achieving O(n) time and O(1) auxiliary space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/reverse-string/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
