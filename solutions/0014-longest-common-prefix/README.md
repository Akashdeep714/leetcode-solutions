# 🧩 14. Longest Common Prefix

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · String · Trie  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/longest-common-prefix/)

---

## 📝 Problem

Find the longest prefix shared among all strings in an array.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Horizontal Scanning / Pairwise Comparison

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `42.9 MB`

#### 💡 Intuition

The common prefix of all strings cannot be longer than the common prefix of any adjacent pair of strings. By comparing string pairs sequentially (`strs[i]` and `strs[i+1]`), we can dynamically update the maximum allowed length of the common prefix.

#### 🧠 Algorithmic Pattern

> **Horizontal Scanning / Pairwise Comparison**

#### 🚀 Approach

1. Initialize `minLen` with the length of the first string.
2. Iterate through adjacent string pairs in the array from `i = 0` to `strs.length - 2`.
3. For each pair, iterate character by character up to the minimum length of the two strings.
4. Stop matching when characters differ or `minLen` bound is reached, then update `minLen` with the matched count.
5. Return the substring of the first string from index `0` to `minLen`.

#### ✅ Why This Works

The prefix property is associative: `LCP(S1, S2, S3) = LCP(LCP(S1, S2), S3)`. Thus, continuously bounding the prefix length across adjacent string comparisons guarantees the correct overall common prefix length.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(S) — In the worst case where all strings are identical, every character in all strings is inspected once, yielding O(S) time where S is the total number of characters across all strings.** |
| Space | **O(1) — Only primitive integer variables are used for index bounds, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Sequential pairwise comparison reduces the problem to repeated two-string prefix checks, updating a single boundary variable.

---

### 🧠 Solution 2 — Vertical Scanning

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `42.8 MB`

#### 💡 Intuition

Instead of comparing entire string pairs horizontally, compare characters at column index `i` across all strings. The moment any string differs at index `i`, the prefix ends immediately.

#### 🧠 Algorithmic Pattern

> **Vertical Scanning**

#### 🚀 Approach

1. Find the minimum length among all strings to bound the search.
2. Iterate index `i` from `0` to `minLen - 1` (column by column).
3. For each index `i`, iterate through all strings `j` in the array (row by row).
4. If `strs[j].charAt(i)` does not match `strs[0].charAt(i)`, return the substring `strs[0][0...i]` immediately.
5. If the outer loop finishes without mismatch, return `strs[0][0...minLen]`.

#### ✅ Why This Works

Vertical scanning checks candidate prefix positions in ascending order. Since a common prefix requires identical characters at every column index for all strings, the first mismatch directly defines the end of the common prefix.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(S) — In the worst case, every character in every string is checked, resulting in O(S) total comparisons. In practice, early exit happens as soon as a mismatch is found.** |
| Space | **O(1) — Only constant space is used for pointer variables and loop counters.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Vertical scanning allows early exit as soon as a character mismatch occurs at any column index, making it optimal when common prefixes are short.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/longest-common-prefix/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
