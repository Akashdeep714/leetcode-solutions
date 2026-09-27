# 🧩 349. Intersection of Two Arrays

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Two Pointers · Binary Search · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/intersection-of-two-arrays/)

---

## 📝 Problem

Find the unique common elements present in both integer arrays nums1 and nums2.

---

## 💡 Intuition

Set data structures automatically handle duplicate removal and enable average O(1) time complexity for element lookups. Storing elements in hash sets allows us to easily check if an element from one array exists in the other without checking duplicates multiple times.

---

## 🧠 Algorithmic Pattern

> **Hash Table / Hash Set**

---

## 🚀 Approach

1. Insert all elements from nums1 into a hash set s1 to deduplicate them.
2. Insert all elements from nums2 into a hash set s2 to deduplicate them.
3. Iterate over each unique element in s1 and check if it exists in s2.
4. Collect all intersecting elements into an output array and return it.

---

## ✅ Why This Works

Iterating over deduplicated elements guarantees that every common value is added to the result array exactly once, while hash set membership tests confirm existence in constant average time.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N + M) — Populating the sets takes O(N) for nums1 and O(M) for nums2. Checking membership for each element of the set takes average O(1) time per element, leading to an overall runtime of O(N + M).** |
| Space | **O(N + M) — In the worst case, hash sets store up to N unique elements from nums1 and up to M unique elements from nums2, requiring O(N + M) auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `3 ms` |
| Memory | `45.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution-2.java)

---

## 🎯 Key Takeaway

Hash Sets convert array intersection into fast set-membership checks, handling both uniqueness and constant-time search simultaneously.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-arrays/)
- [My Solution](./solution-2.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
