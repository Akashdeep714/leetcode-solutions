# 🧩 414. Third Maximum Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Sorting  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/third-maximum-number/)

---

## 📝 Problem

Find the third distinct maximum value in an array, returning the absolute maximum if fewer than three distinct values exist.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Sorting

> **Language:** Java
> **Runtime:** `7 ms`  
> **Memory:** `45.6 MB`

#### 💡 Intuition

Sorting orders all elements sequentially, placing duplicates adjacent to each other. By sorting in descending order, the maximum element sits at index 0, allowing a simple left-to-right scan to count distinct elements.

#### 🧠 Algorithmic Pattern

> **Sorting**

#### 🚀 Approach

1. Sort the array in ascending order using Java's built-in `Arrays.sort`.
2. Reverse the array in-place using two pointers to place elements in descending order.
3. Traverse the array from index 1, tracking the count of unique elements with `eleCount`.
4. Increment `eleCount` whenever `nums[k] != nums[k - 1]`.
5. If `eleCount` reaches 3, return `nums[k]`. If the loop finishes without finding 3 distinct maximums, return `nums[0]`.

#### ✅ Why This Works

Sorting guarantees that identical elements group together and elements appear in decreasing order after reversal. Counting transition points between adjacent elements yields distinct maximums in descending rank.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n log n) — Sorting the array of length `n` takes O(n log n) time. The subsequent reversal and single-pass scan take O(n) time, giving an overall time complexity of O(n log n).** |
| Space | **O(1) — The array reversal and linear scan are performed in-place using O(1) additional variable space (excluding recursion stack space used by Dual-Pivot Quicksort).** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Sorting simplifies k-th distinct value problems by aggregating duplicates and ordering elements, though it incurs an O(n log n) sorting overhead.

---

### 🧠 Solution 2 — Linear Scan / Direct Variable Tracking

> **Language:** Java
> **Runtime:** `3 ms`  
> **Memory:** `44.9 MB`

#### 💡 Intuition

Since we only need the top 3 distinct maximums, we do not need to sort the entire array. Maintaining three variables (`max1`, `max2`, `max3`) allows us to update the top 3 distinct numbers on the fly during a single traversal.

#### 🧠 Algorithmic Pattern

> **Linear Scan / Direct Variable Tracking**

#### 🚀 Approach

1. Initialize three variables (`max1`, `max2`, `max3`) to `null` (or sentinel values) to track the 1st, 2nd, and 3rd maximums.
2. Iterate through each number in `nums`.
3. If the current number is equal to any of `max1`, `max2`, or `max3`, skip it to ignore duplicates.
4. If the current number is greater than `max1` (or `max1` is unassigned), cascade values down (`max3 = max2`, `max2 = max1`, `max1 = current`).
5. Otherwise, if the number is greater than `max2` (or `max2` is unassigned), update `max3 = max2` and `max2 = current`.
6. Otherwise, if the number is greater than `max3` (or `max3` is unassigned), update `max3 = current`.
7. After scanning all numbers, return `max3` if it was set; otherwise return `max1`.

#### ✅ Why This Works

A constant set of 3 variables is sufficient to dynamically maintain the top three distinct elements. Checking for equality before comparison prevents duplicate elements from occupying multiple top positions.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm inspects each element in `nums` exactly once and performs a constant number of scalar comparisons and updates, resulting in O(n) total execution time.** |
| Space | **O(1) — Only three variables are allocated regardless of the input array size, consuming O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

When tracking top-k elements for a small, fixed k, using k tracking variables achieves optimal O(n) time and O(1) space without needing heap or sorting operations.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/third-maximum-number/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
