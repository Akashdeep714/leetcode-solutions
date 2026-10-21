# 🧩 387. First Unique Character in a String

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · String · Queue · Counting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/first-unique-character-in-a-string/)

---

## 📝 Problem

Find the index of the first character in a string that appears exactly once, or return -1 if every character repeats.

---

## 💡 Intuition

To determine whether a character is unique, we must count its total occurrences across the entire string, which cannot be determined in a single pass without knowing future characters. By storing the frequency of every character in a hash map during a first pass, we can perform a second pass from left to right and inspect the frequency of each character in its original order, returning the index of the very first character whose stored count is 1.

---

## 🧠 Algorithmic Pattern

> **Frequency Counting / Hash Table**

---

## 🚀 Approach

1. Initialize an empty hash map `map` where keys are characters and values are their frequency counts.
2. Convert the string `s` into a character array and iterate through each character `c`.
3. Update `map` by incrementing the count for `c` using `map.getOrDefault(c, 0) + 1`.
4. Iterate through the string `s` by index `i` from `0` to `s.length() - 1`.
5. For each character `s.charAt(i)`, retrieve its frequency count from `map`.
6. If the frequency count equals `1`, immediately return the current index `i`.
7. If the loop completes without finding any character with a count of `1`, return `-1`.

---

## ✅ Why This Works

The first pass builds a complete frequency table for all characters in the string. The second pass processes the string in strict left-to-right order, ensuring that the first character evaluated with a count of 1 is mathematically guaranteed to be the first non-repeating character in the string.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm iterates through the string of length n twice and performs constant-time hash map insertions and lookups on average.** |
| Space | **O(1) — The hash map stores at most 26 key-value pairs because the string consists solely of lowercase English letters, using O(1) auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `33 ms` |
| Memory | `46.8 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a two-pass approach—where the first pass gathers global frequencies and the second pass preserves original sequence order—is an effective pattern for order-sensitive unique element lookups.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/first-unique-character-in-a-string/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
