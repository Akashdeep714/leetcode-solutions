# 🧩 26. Remove Duplicates from Sorted Array

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

---

## 📝 Problem

Remove duplicate values from a sorted array in-place, keeping unique elements at the start and returning the count of unique elements.

---

## 💡 Intuition

Because the array is already sorted in non-decreasing order, any duplicate values are guaranteed to be adjacent. By using a fast reader pointer to scan adjacent pairs and a slow writer pointer to place unique elements, we can compress the array in a single pass.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize a writer pointer `k = 1`, assuming the first element at index 0 is always unique.
2. Iterate a reader pointer `j` from index 1 to the end of the array.
3. Compare `nums[j]` with `nums[j - 1]` to check if a new unique value is encountered.
4. If `nums[j] != nums[j - 1]`, write `nums[j]` to `nums[k]` and increment `k`.
5. Return `k`, which represents the number of unique elements in the array.

---

## ✅ Why This Works

Contiguous duplicates are skipped by the equality check. Only the first occurrence of each unique number triggers a write to `nums[k]`, effectively overwriting older duplicate values without disturbing the relative order.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm inspects each element of the array of size `n` exactly once in a single linear loop, leading to O(n) time complexity.** |
| Space | **O(1) — The deduplication is done strictly in-place using only a few primitive integer pointer variables, requiring O(1) auxiliary space.** |

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

When modifying sorted arrays in-place to remove duplicates or filter elements, maintaining separate read and write pointers provides an efficient O(n) time and O(1) space solution.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
