# 🧩 350. Intersection of Two Arrays II

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Two Pointers · Binary Search · Sorting  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/intersection-of-two-arrays-ii/)

---

## 📝 Problem

Find the intersection of two arrays where each element appears as many times as it shows in both arrays.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Hash Table

> **Language:** Java
> **Runtime:** `3 ms`  
> **Memory:** `44.9 MB`

#### 💡 Intuition

By storing element occurrences from the first array in a frequency map, we can check if elements from the second array exist with a positive count. Each matched element is added to the result and its frequency count is decremented.

#### 🧠 Algorithmic Pattern

> **Hash Table**

#### 🚀 Approach

1. Traverse `nums1` and populate a hash map storing the frequency of each integer.
2. Iterate through `nums2`, checking if the current element exists in the map with a count greater than 0.
3. If a valid count exists, add the element to the output array and decrement its stored count by 1.
4. Trim the output array to the exact length of added intersection elements using `Arrays.copyOfRange`.

#### ✅ Why This Works

Decrementing element frequencies ensures each number is added to the intersection at most as many times as it appears in both input arrays.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N + M) — Building the frequency map for `nums1` takes O(N) time where N is `nums1.length`. Iterating through `nums2` takes O(M) time where M is `nums2.length`. Total time complexity is O(N + M).** |
| Space | **O(min(N, M)) — Storing element counts in a hash map requires space proportional to the unique elements in `nums1`. Optimally building the map on the smaller array uses O(min(N, M)) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Hash maps enable O(1) average lookup and update times, providing a linear-time solution for frequency-matching problems.

---

### 🧠 Solution 2 — Two Pointers

> **Language:** Java
> **Runtime:** `6 ms`  
> **Memory:** `45.3 MB`

#### 💡 Intuition

If both arrays are sorted, we can traverse them concurrently using two pointers. Comparing elements at both pointers indicates whether to record a match or advance the pointer pointing to the smaller element.

#### 🧠 Algorithmic Pattern

> **Two Pointers**

#### 🚀 Approach

1. Sort `nums1` and `nums2` in non-decreasing order.
2. Initialize pointer `i = 0` for `nums1` and `j = 0` for `nums2`.
3. Loop while `i < nums1.length` and `j < nums2.length`:
4. If `nums1[i] == nums2[j]`, store the element, then increment both `i` and `j`.
5. If `nums1[i] < nums2[j]`, increment `i` to search for a larger value in `nums1`.
6. If `nums1[i] > nums2[j]`, increment `j` to search for a larger value in `nums2`.
7. Copy and return the slice of the populated result array.

#### ✅ Why This Works

Sorting aligns matching values sequentially in both arrays. Advancing the pointer associated with the smaller element guarantees no candidate matching values are skipped.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N log N + M log M) — Sorting `nums1` takes O(N log N) time and sorting `nums2` takes O(M log M) time. The two-pointer traversal takes O(N + M) time. The overall runtime is dominated by sorting: O(N log N + M log M).** |
| Space | **O(1) — Ignoring the space used by primitive quicksort implementations (O(log N + log M) stack space), the approach operates in O(1) auxiliary space beyond the output container.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Sorting simplifies multi-array comparison into a single linear scan, which is ideal if inputs are already sorted or memory is constrained.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-arrays-ii/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
