# 🧩 448. Find All Numbers Disappeared in an Array

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)

---

## 📝 Problem

Find all numbers from 1 to n that do not appear in the input array of size n.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Hash Table / Set Lookup

> **Language:** Java
> **Runtime:** `21 ms`  
> **Memory:** `78.8 MB`

#### 💡 Intuition

By storing all seen numbers in a Hash Set, we can check whether any number from 1 to n is present in O(1) average time.

#### 🧠 Algorithmic Pattern

> **Hash Table / Set Lookup**

#### 🚀 Approach

1. Iterate through the array `nums` and insert every element into a `HashSet`.
2. Iterate through all candidate numbers from `1` to `n` (inclusive).
3. Check if the `HashSet` contains the current number.
4. If the number is missing from the set, append it to the result list.

#### ✅ Why This Works

A hash set allows constant time average lookups, enabling us to easily identify which integers in the sequence 1 through n were omitted.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Populating the hash set takes O(n) time, and checking numbers 1 through n takes O(n) time, giving an overall linear runtime.** |
| Space | **O(n) — The HashSet stores up to n distinct elements from the array, taking O(n) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using a HashSet provides a direct and easy-to-understand solution for tracking element presence, though it requires O(n) extra space.

---

### 🧠 Solution 2 — In-Place Array Modification / Index Mapping

> **Language:** Java
> **Runtime:** `7 ms`  
> **Memory:** `73.8 MB`

#### 💡 Intuition

Since all numbers are within range [1, n], each number `x` corresponds to a valid array index `x - 1`. We can mark the presence of `x` by making the element at index `x - 1` negative.

#### 🧠 Algorithmic Pattern

> **In-Place Array Modification / Index Mapping**

#### 🚀 Approach

1. Iterate through each element `num` in `nums`.
2. Determine the corresponding target index as `idx = Math.abs(num) - 1`.
3. If the element at `nums[idx]` is positive, negate it to signify that `idx + 1` exists in the array.
4. Perform a second pass over `nums`: for any index `i` where `nums[i]` remains positive, `i + 1` was never encountered, so append `i + 1` to the output list.

#### ✅ Why This Works

The absolute value allows us to read original values even after they have been negated, effectively utilizing the array's sign bit as a boolean visited flag without losing information.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm makes two linear scans over the array of size n, resulting in O(n) runtime.** |
| Space | **O(1) — All operations modify the array in-place. The output list does not count as extra space as per the problem description, so auxiliary space complexity is O(1).** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

When input values map directly to valid array indices ([1, n] to [0, n-1]), the sign of elements can be repurposed as in-place visited flags to achieve O(1) auxiliary space.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
