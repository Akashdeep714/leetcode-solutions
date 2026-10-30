# 🧩 1051. Height Checker

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Sorting · Counting Sort · Bubble Sort  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/height-checker/)

---

## 📝 Problem

Find the number of indices where the current height array differs from the expected sorted height array.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Array / Comparison Sorting

> **Language:** Java
> **Runtime:** `3 ms`  
> **Memory:** `42.9 MB`

#### 💡 Intuition

The expected line ordering is simply the input array sorted in non-decreasing order. By cloning the input array and sorting it, we create the exact target array `expected` and can compare elements index by index.

#### 🧠 Algorithmic Pattern

> **Array / Comparison Sorting**

#### 🚀 Approach

1. Create a copy array `res` with the same elements as `heights`.
2. Sort `res` in non-decreasing order using standard array sorting.
3. Iterate through both `heights` and `res` concurrently.
4. Count and return the number of indices where `heights[i] != res[i]`.

#### ✅ Why This Works

Sorting the copied array yields the exact target array `expected`. Comparing corresponding elements at each index directly counts the number of out-of-order students.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N log N) — Copying takes O(N) time, sorting an array of size N takes O(N log N) time, and linear comparison takes O(N) time, leading to an overall O(N log N) runtime.** |
| Space | **O(N) — An auxiliary array of size N is allocated to store the sorted heights, requiring O(N) additional memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

When target order is simply non-decreasing order, cloning and sorting gives a direct O(N log N) baseline solution.

---

### 🧠 Solution 2 — Counting Sort / Frequency Array

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `43.2 MB`

#### 💡 Intuition

Since height values are constrained to a small range (1 to 100), we can count the frequency of each height. By consuming heights from smallest to largest in sequence, we can determine what `expected[i]` should be at index `i` on the fly.

#### 🧠 Algorithmic Pattern

> **Counting Sort / Frequency Array**

#### 🚀 Approach

1. Initialize a frequency array `countArray` of size 101 to store the frequency of each height.
2. Populate `countArray` by iterating through `heights`.
3. Maintain a pointer `currHeight` initialized to 1 to represent the current minimum height available.
4. Iterate through index `i` from 0 to N - 1: advance `currHeight` until `countArray[currHeight] > 0`, compare `heights[i]` with `currHeight`, increment mismatch count if they differ, and decrement `countArray[currHeight]`.

#### ✅ Why This Works

The frequency array implicitly represents the sorted order. Consuming counts from lowest to highest height simulates inspecting `expected[i]` without allocating or sorting a full copy of the array.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N + K) — Populating the frequency array takes O(N) time. Iterating through `heights` while advancing `currHeight` up to the max height bound K (100) takes O(N + K) total time.** |
| Space | **O(K) — The frequency array size is fixed at K = 101, taking O(K) (or O(1) relative to input size N) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

When array values lie in a small bounded range, counting sort allows linear-time processing and avoids full comparison sorting.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/height-checker/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
