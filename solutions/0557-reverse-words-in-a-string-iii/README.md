# 🧩 557. Reverse Words in a String III

> **Difficulty:** 🟢 Easy  
> **Topics:** Two Pointers · String  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/reverse-words-in-a-string-iii/)

---

## 📝 Problem

Reverse the characters of each word in a space-delimited sentence while preserving space characters and word order.

---

## 💡 Intuition

Since words are separated by spaces and stay in their original relative positions, we can process each word independently. Converting the string into a mutable character array allows us to locate each word's start and end boundaries using two pointers, then reverse the characters in that specific sub-range in-place before constructing the final string.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Convert the input string `s` into a character array `charArr` and initialize both `start` and `end` pointers to index `0`.
2. Iterate through `charArr` with a outer `while` loop that runs as long as `start` is within array bounds.
3. Advance `end` using an inner `while` loop until it encounters a space character `' '` or reaches the end of the array, defining the current word boundary.
4. Call the `reverse` helper method to swap characters in `charArr` from index `start` to `end - 1` using a two-pointer approach that moves inward.
5. Advance both `start` and `end` to `end + 1` to skip the space character and position the pointers at the beginning of the next word.
6. Construct and return a new `String` from the modified `charArr` after all words have been reversed.

---

## ✅ Why This Works

By using `end` to find the delimiting space, the interval `[start, end - 1]` strictly bounds a single word. Applying a standard two-pointer character reversal on this precise sub-array guarantees that each character within the word is mirrored around its midpoint, reversing the word while leaving spaces and the order of surrounding words unchanged.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Each character in the string is visited a constant number of times—once to locate word boundaries and at most once during the character reversal process.** |
| Space | **O(n) — Creating the character array `charArr` and the resulting string requires auxiliary memory proportional to the length of the string `s`.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `3 ms` |
| Memory | `46.1 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

To reverse segments of a string separated by a delimiter, use dynamic pointer bounds to isolate each segment and apply localized two-pointer reversals.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/reverse-words-in-a-string-iii/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
