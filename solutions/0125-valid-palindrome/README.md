# 🧩 125. Valid Palindrome

> **Difficulty:** 🟢 Easy  
> **Topics:** Two Pointers · String  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/valid-palindrome/)

---

## 📝 Problem

Determine if a given string is a palindrome after removing all non-alphanumeric characters and ignoring letter case.

---

## 💡 Intuition

A string is a palindrome if its valid characters match symmetrically from the outside in. Rather than spending extra space creating a cleaned, reversed copy of the string, we can process the string in place using two pointers starting at opposite ends. By skipping non-alphanumeric characters on the fly and comparing lowercase representations of valid characters, we can verify whether the string reads the same forward and backward in a single pass.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Define a helper function `isAlphaNumericCharacter(char c)` that checks whether a character `c` is a lowercase letter ('a'-'z'), uppercase letter ('A'-'Z'), or digit ('0'-'9').
2. Initialize two pointers: `i = 0` at the start of the string and `j = s.length() - 1` at the end.
3. Enter a `while` loop that runs as long as `i < j`.
4. Retrieve `c1 = s.charAt(i)` and `c2 = s.charAt(j)`. If `c1` is not alphanumeric, increment `i` and continue to the next iteration.
5. If `c2` is not alphanumeric, decrement `j` and continue to the next iteration.
6. When both pointers point to alphanumeric characters, convert `c1` and `c2` to lowercase using `Character.toLowerCase()`. If they are not equal, return `false` immediately.
7. If the characters match, increment `i` and decrement `j` to move toward the center.
8. If the loop terminates without finding any mismatch, return `true`.

---

## ✅ Why This Works

The algorithm maintains the invariant that all filtered alphanumeric pairs outside the window `[i, j]` have been checked and verified to match. By using `continue` statements to skip non-alphanumeric characters, the pointers always align on the next valid forward and backward characters respectively. Converting both to lowercase neutralizes case differences, guaranteeing an accurate check for symmetry without modifying the string or allocating additional memory.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Each character in the string is visited at most once by either pointer `i` or pointer `j` as they move toward each other.** |
| Space | **O(1) — The algorithm only uses two integer pointers and a few primitive character variables, requiring no extra auxiliary memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `43.8 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using two pointers converging from both ends allows you to filter and validate string properties in a single pass without allocating auxiliary memory.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/valid-palindrome/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
