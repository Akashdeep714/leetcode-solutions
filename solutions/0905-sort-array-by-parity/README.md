# 🧩 905. Sort Array By Parity

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers · Sorting  
> **Solutions:** 4 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/sort-array-by-parity/)

---

## 📝 Problem

Reorder an array of integers so all even elements appear before all odd elements.

---

## 🛠️ Solutions

This folder contains **4 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Sorting with Custom Comparator

> **Language:** Java
> **Runtime:** `5 ms`  
> **Memory:** `47 MB`

#### 💡 Intuition

By defining a sort order where an integer's weight is determined by its parity (`x % 2`), even numbers (remainder 0) naturally sort before odd numbers (remainder 1).

#### 🧠 Algorithmic Pattern

> **Sorting with Custom Comparator**

#### 🚀 Approach

1. Box the primitive `int[]` into an `Integer[]` array to support object custom sorting.
2. Sort the array using `Arrays.sort` with a custom lambda comparator comparing `val1 % 2` and `val2 % 2`.
3. Unbox the sorted `Integer[]` elements back into the primitive `int[]` array.
4. Return the modified array.

#### ✅ Why This Works

Because `0 % 2 == 0` and `1 % 2 == 1` or `3 % 2 == 1`, sorting by `x % 2` orders all even numbers (0) before odd numbers (1).

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n log n) — Sorting an array of length $n$ using Timsort (`Arrays.sort` on objects) takes $O(n \log n)$ time in average and worst cases.** |
| Space | **O(n) — Requires $O(n)$ extra space to store the boxed `Integer[]` array.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Custom sorting directly solves custom ordering problems, but introduces extra comparison and space overhead compared to dedicated partition algorithms.

---

### 🧠 Solution 2 — Auxiliary Array / Two Pass

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `46.9 MB`

#### 💡 Intuition

Instead of swapping elements in-place, create a new result array and sequentially copy all even values first, followed by all odd values in a second pass.

#### 🧠 Algorithmic Pattern

> **Auxiliary Array / Two Pass**

#### 🚀 Approach

1. Allocate a new array `res` of the same length as `nums`.
2. Iterate through `nums` in a first pass and copy every even number (`nums[i] % 2 == 0`) into `res`.
3. Iterate through `nums` in a second pass and copy every odd number (`nums[i] % 2 == 1`) into `res`.
4. Return `res`.

#### ✅ Why This Works

Processing all evens first guarantees that the prefix of `res` consists entirely of even elements, while the second pass appends all odd elements into the remaining suffix.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm makes two full linear scans over the input array of size $n$, resulting in $O(n)$ overall time.** |
| Space | **O(n) — Requires $O(n)$ auxiliary space for the output array `res`.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Using extra memory simplifies logic into linear passes when in-place modification is not strictly required.

---

### 🧠 Solution 3 — Two Pointers (Inward Convergence)

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `46.7 MB`

#### 💡 Intuition

Maintain two pointers: one at the start looking for an odd number, and one at the end looking for an even number. Swap them when both are found, and shrink the pointers toward each other.

#### 🧠 Algorithmic Pattern

> **Two Pointers (Inward Convergence)**

#### 🚀 Approach

1. Initialize pointer `i = 0` at the start and pointer `j = nums.length - 1` at the end.
2. While `i < j`, inspect the parity of `nums[i]` and `nums[j]`.
3. If `nums[i]` is odd and `nums[j]` is even, swap `nums[i]` and `nums[j]`.
4. If `nums[i]` is even, increment `i` since it is already correctly positioned.
5. If `nums[j]` is odd, decrement `j` since it is already correctly positioned.
6. Return `nums` once `i >= j`.

#### ✅ Why This Works

The left pointer only advances when an even number is confirmed at its position, and the right pointer only retreats when an odd number is confirmed at its position. Swapping misaligned pairs maintains this invariant.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — In each step, at least one of the two pointers (`i` or `j`) moves toward the middle, ensuring at most $n$ total pointer increments/decrements.** |
| Space | **O(1) — The operation is performed entirely in-place using a constant number of variables, requiring $O(1)$ extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-3.java)

#### 🎯 Key Takeaway

Opposite-direction two pointers provide an optimal $O(n)$ time, $O(1)$ space in-place partitioning strategy.

---

### 🧠 Solution 4 — Read/Write Two Pointers (Lomuto Partition)

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `46.7 MB`

#### 💡 Intuition

Maintain a write pointer `j` that marks the boundary for the next even number. Scan through the array with a read pointer `i`. Every time an even number is encountered, swap it to position `j` and advance `j`.

#### 🧠 Algorithmic Pattern

> **Read/Write Two Pointers (Lomuto Partition)**

#### 🚀 Approach

1. Initialize write boundary pointer `j = 0`.
2. Iterate reader pointer `i` from `0` to `nums.length - 1`.
3. When `nums[i]` is even, swap `nums[i]` with `nums[j]`.
4. Increment `j` after the swap.
5. Return the modified `nums` array after the loop completes.

#### ✅ Why This Works

Pointer `j` always tracks the index where the next even number should be written. All elements before `j` are guaranteed to be even, effectively partitioning the array in one pass.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The single loop visits each element exactly once, performing $O(1)$ operations per element, yielding $O(n)$ total time.** |
| Space | **O(1) — All swaps are done in-place using scalar variables, taking $O(1)$ extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-4.java)

#### 🎯 Key Takeaway

Lomuto-style partitioning uses a single loop and a write pointer to achieve clean, single-pass in-place partitioning.


---

## 🎯 Key Takeaway

This repository currently contains 4 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/sort-array-by-parity/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
