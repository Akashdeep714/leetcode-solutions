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

---
### 🔀 Solution 2 — Hash Table / Frequency Counting

> **Language:** Java  
> **Runtime:** `3 ms`  
> **Memory:** `44.9 MB`

#### 💡 Intuition

To handle duplicate elements correctly, we need to track how many times each number appears in the first array and decrement that available count whenever a match is found in the second array. A hash map allows us to store the frequency of each element in `nums1` in linear time. As we traverse `nums2`, any element present in the map with a non-zero count is added to our result set, ensuring each common number appears in the intersection exactly $\min(\text{count}_1, \text{count}_2)$ times.

#### 🧠 Algorithmic Pattern

> **Hash Table / Frequency Counting**

#### 🚀 Approach

1. Initialize a hash map `map` to store the frequency of each integer in `nums1`.
2. Iterate through `nums1` and increment the count for each number in `map` using `map.put(num, map.getOrDefault(num, 0) + 1)`.
3. Allocate an integer array `res` of size `nums1.length` to hold result elements, and initialize index pointer `k = 0`.
4. Iterate through each number `num` in `nums2`.
5. Retrieve the remaining count of `num` from `map`; if the count is greater than 0, place `num` into `res[k]`, increment `k`, and decrement the count of `num` in `map` by 1.
6. Return the trimmed sub-array `Arrays.copyOfRange(res, 0, k)` containing only the filled intersection elements.

#### ✅ Why This Works

By recording the exact count of each element in `nums1` and decrementing the frequency in `map` every time a match is found in `nums2`, the code guarantees that no element is added to the result array more times than it appears in either `nums1` or `nums2`. This correctly computes the multiset intersection based on element frequencies.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m + n) — Populating the hash map takes $O(m)$ average time for `nums1` of length $m$, and scanning `nums2` of length $n$ takes $O(n)$ average time, yielding $O(m + n)$ total time.** |
| Space | **O(m) — The hash map stores up to $m$ unique elements from `nums1`, requiring $O(m)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-arrays-ii/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
