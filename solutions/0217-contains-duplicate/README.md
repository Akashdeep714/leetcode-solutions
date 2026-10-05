# 🧩 217. Contains Duplicate

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Sorting  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/contains-duplicate/)

---

## 📝 Problem

Determine if any element appears at least twice in an integer array.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Hash Set / Frequency Tracking

> **Language:** Java
> **Runtime:** `18 ms`  
> **Memory:** `108.2 MB`

#### 💡 Intuition

By keeping track of elements encountered so far in a hash set, we can check whether the current element was seen before in linear time.

#### 🧠 Algorithmic Pattern

> **Hash Set / Frequency Tracking**

#### 🚀 Approach

1. Initialize an empty HashSet of integers.
2. Iterate through each number in the array.
3. Check if the HashSet already contains the current number; if it does, return true immediately.
4. Otherwise, add the number to the set and continue.
5. If the loop finishes without finding any duplicate, return false.

#### ✅ Why This Works

A HashSet stores unique elements and provides O(1) average lookup time. Finding an element already present in the set guarantees the existence of a duplicate.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We iterate through the array of n elements once. Adding and searching in a HashSet takes O(1) average time per operation, giving an overall O(n) time complexity.** |
| Space | **O(n) — In the worst-case scenario where all elements are unique, the HashSet stores all n elements, consuming O(n) space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Using a hash set trades extra O(n) memory to achieve optimal linear O(n) execution time.

---

### 🧠 Solution 2 — Sorting / Adjacent Pair Check

> **Language:** Java
> **Runtime:** `26 ms`  
> **Memory:** `81.6 MB`

#### 💡 Intuition

If the array is sorted, any duplicate values must land adjacent to one another. Sorting simplifies the duplicate check to scanning neighboring elements.

#### 🧠 Algorithmic Pattern

> **Sorting / Adjacent Pair Check**

#### 🚀 Approach

1. Sort the array in ascending order using Arrays.sort().
2. Iterate through the array from index 0 up to n - 2.
3. Compare each element with its immediate neighbor (nums[i] == nums[i + 1]).
4. If any pair of adjacent elements are equal, return true.
5. If no matching adjacent pair is found after scanning the entire array, return false.

#### ✅ Why This Works

Sorting reorders the elements monotonically, bringing all instances of equal values adjacent to each other. Comparing neighboring elements is therefore sufficient to detect duplicates.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n log n) — Sorting the array dominates the runtime at O(n log n) time. The subsequent linear scan takes O(n) time, resulting in total time complexity of O(n log n).** |
| Space | **O(log n) — Java's Arrays.sort() for primitive arrays uses Dual-Pivot Quicksort, requiring O(log n) auxiliary stack space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Sorting avoids using extra heap space for hash structures at the expense of increasing time complexity to O(n log n).


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/contains-duplicate/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
