# 🧩 217. Contains Duplicate

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/contains-duplicate/)

---

## 📝 Problem

Determine if an integer array contains any duplicate values, returning true if any element appears at least twice and false if all elements are unique.

---

## 💡 Intuition

In an unsorted array, duplicate elements can appear at any arbitrary distance from each other. By sorting the array first, identical values are forced into adjacent positions. This observation simplifies the duplicate check: instead of comparing every element against all others or using additional memory to store seen values, we only need to check if any element matches its immediate neighbor in a single pass.

---

## 🧠 Algorithmic Pattern

> **Sorting**

---

## 🚀 Approach

1. Sort the input array `nums` in ascending order using `Arrays.sort(nums)`.
2. Iterate through the array from index `i = 0` up to `nums.length - 2`.
3. In each iteration, check if the current element `nums[i]` is equal to the adjacent element `nums[i + 1]`.
4. If `nums[i] == nums[i + 1]`, immediately return `true` as a duplicate is found.
5. If the loop finishes without finding any matching adjacent pairs, return `false`.

---

## ✅ Why This Works

Sorting establishes a non-decreasing order across the array, guaranteeing that equal values occupy contiguous memory locations. If any number appears two or more times in `nums`, at least one pair of duplicate values will end up at adjacent indices `i` and `i + 1`. Consequently, a linear comparison of consecutive elements after sorting is mathematically guaranteed to detect duplicates if they exist.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n log n)** |
| Space | **O(log n)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `26 ms` |
| Memory | `81.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Sorting reorganizes data so that identical elements are adjacent, simplifying pair comparisons. While a Hash Set can solve this problem in O(n) time, sorting offers an in-place alternative with minimal extra memory overhead.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/contains-duplicate/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
