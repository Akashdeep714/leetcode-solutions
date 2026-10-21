# 🧩 242. Valid Anagram

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · String · Sorting  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/valid-anagram/)

---

## 📝 Problem

Determine whether string t is a permutation (anagram) of string s.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Frequency Counting / Fixed Bucketing

> **Language:** Java
> **Runtime:** `3 ms`  
> **Memory:** `44.3 MB`

#### 💡 Intuition

Since the inputs consist solely of lowercase English letters, a fixed 26-element array can directly map each character to its offset relative to 'a'. Incrementing counts for s and decrementing for t leaves all elements at 0 if and only if the strings are anagrams.

#### 🧠 Algorithmic Pattern

> **Frequency Counting / Fixed Bucketing**

#### 🚀 Approach

1. Initialize a fixed-size integer array of length 26 to store character frequencies.
2. Traverse string s and increment the array count at index c - 'a' for each character.
3. Traverse string t and decrement the array count at index c - 'a' for each character.
4. Check the frequency array; if any entry is non-zero, return false. If all entries are zero, return true.

#### ✅ Why This Works

An anagram requires identical character frequencies. By incrementing counts for s and decrementing for t, any mismatch results in a non-zero entry in the frequency array.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Iterating over both strings of length n takes O(n) time. Inspecting the 26-element array takes constant O(1) time, resulting in overall O(n) time complexity.** |
| Space | **O(1) — The frequency array size is strictly fixed to 26 elements regardless of input string length, using O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

When the alphabet size is small and fixed (such as lowercase English letters), an array-based lookup table avoids hash map overhead and yields O(1) auxiliary space.

---

### 🧠 Solution 2 — Hash Table Frequency Counting

> **Language:** Java
> **Runtime:** `14 ms`  
> **Memory:** `46.1 MB`

#### 💡 Intuition

Using a Hash Map dynamically links characters to their net frequencies. This approach requires no assumptions about alphabet boundaries and gracefully handles arbitrary character sets like Unicode.

#### 🧠 Algorithmic Pattern

> **Hash Table Frequency Counting**

#### 🚀 Approach

1. First compare string lengths; if s.length() != t.length(), return false immediately.
2. Initialize a HashMap<Character, Integer> to record net frequencies.
3. Iterate through s, incrementing the map entry for each character.
4. Iterate through t, decrementing the map entry for each character.
5. Iterate over the map keys; if any frequency is non-zero, return false. Otherwise, return true.

#### ✅ Why This Works

By tracking net frequency in a map, matching characters cancel out. If any net count remains non-zero, the two strings do not share identical character counts.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Iterating through strings of length n takes O(n) time. Each hash map operation runs in average O(1) time. Checking the distinct keys takes O(k) where k <= n, making the total time complexity O(n).** |
| Space | **O(k) — The map stores up to k unique characters from the input strings, requiring O(k) auxiliary space, where k is bounded by the alphabet size.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Using a Hash Map provides flexibility for unbounded character sets (such as Unicode), trading slight memory overhead for generality.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/valid-anagram/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
