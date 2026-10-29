# 🧩 724. Find Pivot Index

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Prefix Sum  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/find-pivot-index/)

---

## 📝 Problem

Find the leftmost index in an array where the sum of elements strictly to the left equals the sum of elements strictly to the right.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Prefix Sum

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `47.7 MB`

#### 💡 Intuition

If we know the total sum of the array in advance, the sum of elements to the right of index `i` is simply `total_sum - left_sum - nums[i]`. Thus, we can evaluate whether `i` is a pivot in O(1) time while iterating through the array.

#### 🧠 Algorithmic Pattern

> **Prefix Sum**

#### 🚀 Approach

1. Compute the total sum of all elements in the array in a first pass.
2. Initialize `leftSum` to 0 and set `rightSum` to the computed total sum.
3. Iterate through each index `i` from left to right.
4. Check if `leftSum == rightSum - nums[i]`. If equal, return index `i` immediately.
5. Otherwise, update `leftSum += nums[i]` and `rightSum -= nums[i]` before continuing to the next element.
6. If no pivot index is found after checking all elements, return -1.

#### ✅ Why This Works

At any index `i`, the remaining sum to the right is equal to `totalSum - leftSum - nums[i]`. By incrementally tracking `leftSum`, we check the equality condition in constant time per element.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm computes the total sum in one O(n) pass, then inspects each element in a second O(n) pass. Overall time complexity is linear, O(n).** |
| Space | **O(1) — Only a constant number of scalar variable integer accumulators (`leftSum` and `rightSum`) are used, giving O(1) auxiliary space complexity.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Pre-calculating global properties (like array total sum) allows converting nested traversal problems into linear O(N) running sum inspections.

---

### 🧠 Solution 2 — Nested Iteration / Brute Force

> **Language:** Java
> **Runtime:** `318 ms`  
> **Memory:** `47.3 MB`

#### 💡 Intuition

For each index `i`, directly iterate over all elements to its left to compute `leftSum`, and all elements to its right to compute `rightSum`, then compare the two.

#### 🧠 Algorithmic Pattern

> **Nested Iteration / Brute Force**

#### 🚀 Approach

1. Loop through each index `i` from 0 to `nums.length - 1`.
2. For the current index `i`, iterate through all elements from index `0` to `i - 1` to calculate `leftSum`.
3. Iterate through all elements from index `i + 1` to `nums.length - 1` to calculate `rightSum`.
4. If `leftSum == rightSum`, return `i` as the leftmost pivot index.
5. If the loop finishes without finding a valid index, return -1.

#### ✅ Why This Works

The algorithm directly computes the exact sums specified in the definition for every candidate index, guaranteeing correctness by brute force.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2) — For each index `i`, the code iterates over all `n` elements across two inner loops. Summing `n` times for `n` candidates yields O(n^2) time overall.** |
| Space | **O(1) — The calculation uses only primitive variables for `leftSum` and `rightSum`, requiring constant O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

While correct, re-summing sub-arrays independently for each index leads to quadratic time complexity, which can be optimized using running prefix sums.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/find-pivot-index/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
