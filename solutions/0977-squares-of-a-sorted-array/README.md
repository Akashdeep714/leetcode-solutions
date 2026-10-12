# 🧩 977. Squares of a Sorted Array

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers · Sorting  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/squares-of-a-sorted-array/)

---

## 📝 Problem

Given a sorted array of integers, return a new array containing the squares of each number sorted in non-decreasing order.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Brute-Force Transformation + Sorting

> **Language:** Java
> **Runtime:** `10 ms`  
> **Memory:** `48.9 MB`

#### 💡 Intuition

The simplest way to solve the problem is to transform each number into its square without worrying about order, and then apply a standard sorting algorithm to arrange the squared values in non-decreasing order.

#### 🧠 Algorithmic Pattern

> **Brute-Force Transformation + Sorting**

#### 🚀 Approach

1. Create a new array `result` of size `n` to store the squared elements.
2. Iterate through the input array `nums` from index 0 to `n - 1`, setting `result[i] = nums[i] * nums[i]`.
3. Sort the `result` array using `Arrays.sort(result)`.
4. Return the sorted `result` array.

#### ✅ Why This Works

Squaring preserves non-negativity, but distorts order for negative numbers. Sorting the resulting array explicitly re-establishes non-decreasing order regardless of initial signs.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n log n) — Squaring `n` elements takes O(n) time. Sorting an array of `n` primitive integers in Java using `Arrays.sort()` takes O(n log n) time. Thus, the overall time complexity is dominated by O(n log n).** |
| Space | **O(log n) — Excluding the output array, Java's Dual-Pivot Quicksort requires O(log n) auxiliary space for recursion stack depth.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Directly squaring and sorting is straightforward to implement, but it does not take advantage of the fact that the original array was already sorted.

---

### 🧠 Solution 2 — Two Pointers

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `47 MB`

#### 💡 Intuition

Because the input array is already sorted, the largest squared values must come from either the far-left (most negative) or far-right (most positive) elements. By comparing the magnitudes at both ends, we can select the larger square and fill the output array from right to left.

#### 🧠 Algorithmic Pattern

> **Two Pointers**

#### 🚀 Approach

1. Initialize two pointers: `l = 0` (left end) and `r = n - 1` (right end).
2. Create a `result` array of size `n`.
3. Iterate backwards from index `n - 1` down to `0` for the position to fill in `result`.
4. Compare the absolute values `|nums[l]|` and `|nums[r]|`.
5. If `|nums[l]| > |nums[r]|`, store `nums[l] * nums[l]` in `result[i]` and increment `l`.
6. Otherwise, store `nums[r] * nums[r]` in `result[i]` and decrement `r`.
7. Return the populated `result` array.

#### ✅ Why This Works

The absolute values of a sorted array decrease towards the middle and reach maximums at the boundaries. Choosing the maximum absolute value at each step guarantees that the result array is populated with the largest remaining square at the current highest available index.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Each element in `nums` is evaluated exactly once as either `l` increments or `r` decrements, resulting in a single O(n) pass.** |
| Space | **O(1) — Only a constant number of pointer variables (`l`, `r`, `val`) are used. The `result` array is required for the output and is not considered extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Leveraging the pre-sorted property of the input array with two pointers allows the problem to be solved in linear time without extra sorting overhead.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/squares-of-a-sorted-array/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
