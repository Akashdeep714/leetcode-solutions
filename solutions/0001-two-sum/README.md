# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Find indices of two numbers in an array that add up to a target sum.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Brute Force / Array Iteration

> **Language:** Java
> **Runtime:** `98 ms`  
> **Memory:** `46.8 MB`

#### 💡 Intuition

Exhaustively check all pairs of distinct elements in the array until a pair summing to the target is found.

#### 🧠 Algorithmic Pattern

> **Brute Force / Array Iteration**

#### 🚀 Approach

1. Initialize an array of size 2 to store the resulting indices.
2. Iterate through each index i from 0 to nums.length - 1.
3. Iterate through each index j from 0 to nums.length - 1.
4. Check if i and j are distinct and if nums[i] + nums[j] equals target.
5. If a matching pair is found, record the indices and return the result.

#### ✅ Why This Works

Because the problem guarantees exactly one valid solution, checking every possible pair guarantees that the correct pair will eventually be evaluated.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2) — With two nested loops iterating over the array of size n, the total number of pair comparisons is proportional to n^2.** |
| Space | **O(1) — The algorithm only uses a fixed array of size 2 for the result, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Brute force requires no additional data structures, but evaluating every pair leads to quadratic time complexity.

---

### 🧠 Solution 2 — Hash Table / Complement Search

> **Language:** Java
> **Runtime:** `5 ms`  
> **Memory:** `46.7 MB`

#### 💡 Intuition

For each number x, the required matching value is target - x. Storing array elements in a hash map allows us to check for the existence of this complement in O(1) average time.

#### 🧠 Algorithmic Pattern

> **Hash Table / Complement Search**

#### 🚀 Approach

1. Initialize a hash map to map each element's value to its corresponding array index.
2. Populate the map by iterating through the array and inserting each element.
3. Iterate through the array again and compute the target complement (lookupNumber = target - nums[i]).
4. Check if the hash map contains the complement at an index different from i.
5. If found, return the complement's index along with the current index i.

#### ✅ Why This Works

The equation nums[i] + nums[j] = target is equivalent to nums[j] = target - nums[i]. Storing values in a hash map turns an O(n) search into an O(1) average lookup.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Populating and querying the hash map takes O(1) average time per element, leading to an overall O(n) runtime across n elements.** |
| Space | **O(n) — In the worst case, the hash map stores up to n elements, requiring O(n) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-4.java)

#### 🎯 Key Takeaway

Trading linear auxiliary space for a hash map drastically optimizes search time from quadratic O(n^2) to linear O(n).


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
