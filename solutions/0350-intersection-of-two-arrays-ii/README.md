# 🧩 350. Intersection of Two Arrays II

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Two Pointers · Binary Search · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/intersection-of-two-arrays-ii/)

---

## 📝 Problem

Given two integer arrays, return an array representing their intersection where each element appears as many times as it shows in both arrays.

---

## 💡 Intuition

When both arrays are sorted, duplicate values are grouped together and elements appear in non-decreasing order. By placing a pointer at the beginning of each array, we can compare elements side-by-side: equal elements belong in the intersection and allow both pointers to advance, while unequal elements allow us to advance the pointer corresponding to the smaller element to search for a larger, matching value. This ensures we collect every matching instance while maintaining the exact duplicate counts required.

---

## 🧠 Algorithmic Pattern

> **Two Pointers / Sorting**

---

## 🚀 Approach

1. Sort both input arrays `nums1` and `nums2` in non-decreasing order using `Arrays.sort()`.
2. Initialize a result array `res` of size `nums1.length`, a write pointer `k = 0`, and two read pointers `i = 0` for `nums1` and `j = 0` for `nums2`.
3. Loop while `i < nums1.length` and `j < nums2.length`.
4. If `nums1[i] == nums2[j]`, write `nums1[i]` into `res[k]`, then increment `k`, `i`, and `j`.
5. If `nums1[i] > nums2[j]`, increment `j` to search for a larger value in `nums2`; otherwise, increment `i`.
6. Return the truncated result array from index `0` to `k` using `Arrays.copyOfRange(res, 0, k)`.

---

## ✅ Why This Works

Sorting guarantees that elements in both arrays are monotonically non-decreasing. If `nums1[i] < nums2[j]`, then `nums1[i]` cannot match `nums2[j]` or any subsequent element in `nums2`, so advancing `i` is guaranteed not to skip any valid matches. When `nums1[i] == nums2[j]`, the pair represents one shared instance of that number, so consuming both elements by incrementing `i` and `j` accurately counts duplicates without double-counting.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n log n + m log m)** |
| Space | **O(log n + log m)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `6 ms` |
| Memory | `45.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Sorting enables a two-pointer linear scan that finds the intersection of two arrays while automatically respecting element frequencies without requiring extra hash table storage.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-arrays-ii/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
