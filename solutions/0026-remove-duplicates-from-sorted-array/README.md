# 🧩 26. Remove Duplicates from Sorted Array

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

---

## 📝 Problem

Remove duplicate elements in-place from a non-decreasingly sorted integer array `nums` such that each unique element appears once, and return the count $k$ of unique elements.

---

## 💡 Intuition

Because the array is already sorted, duplicate values are guaranteed to be adjacent. This allows us to detect every new unique element simply by comparing the current element with the element immediately before it. We can maintain a write pointer `k` that tracks where the next unique element should be stored in-place. Since the very first element `nums[0]` is always unique, `k` starts at index 1, and a read pointer `j` scans the array starting from index 1. Whenever `nums[j]` differs from `nums[j-1]`, we have encountered a new unique value, which we copy to `nums[k]` before advancing `k`.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize the write pointer `k = 1` because the first element `nums[0]` is always unique and remains at index 0.
2. Loop through the array using a fast read pointer `j` starting from index `1` up to `nums.length - 1`.
3. Inside the loop, check if `nums[j] != nums[j-1]` to determine if `nums[j]` is a newly encountered unique element.
4. If the condition holds, copy `nums[j]` into `nums[k]` to overwrite any existing duplicate at index `k`.
5. Increment `k` by `1` so it points to the next write position.
6. After the loop finishes, return `k`, which represents both the length of the deduplicated subarray and the total count of unique elements.

---

## ✅ Why This Works

The non-decreasing order of `nums` guarantees that equal elements form contiguous blocks. Checking `nums[j] != nums[j-1]` correctly identifies the first occurrence of each distinct number. Throughout the iteration, the algorithm maintains the invariant that `nums[0...k-1]` contains all unique elements seen so far in sorted order. Because the read pointer `j` is always greater than or equal to the write pointer `k`, writing to `nums[k]` never overwrites unprocessed elements.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `46.8 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When modifying a sorted array in-place, a two-pointer read/write strategy leverages adjacency to filter out redundant elements in linear time with $O(1)$ extra space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
