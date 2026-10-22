# 🧩 561. Array Partition

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Greedy · Sorting · Counting Sort  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/array-partition/)

---

## 📝 Problem

Pair 2n integers into n pairs such that the sum of the minimum of each pair is maximized.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Greedy / Sorting

> **Language:** Java
> **Runtime:** `18 ms`  
> **Memory:** `49.7 MB`

#### 💡 Intuition

To maximize the sum of minimums in pairs, we want to minimize the loss caused by taking the smaller element of each pair. By sorting the numbers in ascending order and pairing adjacent elements (e.g., (nums[0], nums[1]), (nums[2], nums[3])), each smaller element is paired with the smallest possible element that is larger than or equal to it. Therefore, the sum of all elements at even indices yields the optimal total sum.

#### 🧠 Algorithmic Pattern

> **Greedy / Sorting**

#### 🚀 Approach

1. Sort the input array 'nums' in non-decreasing order using standard comparison sort.
2. Initialize a variable 'maxSum' to 0.
3. Iterate through the sorted array stepping by 2 (i.e., i = 0, 2, 4, ...).
4. Add nums[i] to 'maxSum' at each step and return the result.

#### ✅ Why This Works

In any pair (a, b) with a <= b, the element 'b' is discarded and 'a' contributes to the sum. To waste as little value as possible, 'b' should be as close to 'a' as possible. Sorting guarantees adjacent elements are closest in value.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N log N) — Sorting the array of size N takes O(N log N) time using Java's dual-pivot Quicksort. The subsequent linear traversal stepping by 2 takes O(N) time, yielding O(N log N) overall.** |
| Space | **O(log N) — Java's Arrays.sort() for primitive integer arrays uses dual-pivot Quicksort, requiring O(log N) auxiliary recursion stack space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

When pairing elements to maximize pair minimums, sorting ensures adjacent elements minimize the 'waste' of larger numbers.

---

### 🧠 Solution 2 — Counting Sort / Bucket Array

> **Language:** Java
> **Runtime:** `6 ms`  
> **Memory:** `48.5 MB`

#### 💡 Intuition

Since the constraint bounds the input values (-10,000 to 10,000), we can avoid the O(N log N) sorting overhead by counting value occurrences in a frequency array. Traversing this frequency array sequentially naturally yields elements in sorted order, allowing us to accumulate every second element using a parity tracker.

#### 🧠 Algorithmic Pattern

> **Counting Sort / Bucket Array**

#### 🚀 Approach

1. Create a frequency array of size 20,001 (offsetting numbers by +10,000 to handle negative values).
2. Iterate through 'nums' to count the frequency of each element.
3. Initialize a boolean flag 'isEvenIndex' to true to track whether the current element instance falls on an even index in the conceptual sorted order.
4. Iterate through the frequency array. While count > 0, add the element value to 'maxSum' if 'isEvenIndex' is true, decrement the count, and flip 'isEvenIndex'.

#### ✅ Why This Works

Counting sort implicitly sorts elements in O(N + K) linear time. Toggling a boolean flag for each instance of a value correctly identifies elements that would occupy even indices in a fully sorted array.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N + K) — Populating the frequency array takes O(N) time for N elements. Iterating over the fixed frequency array of range K = 20,001 takes O(K) time, giving a total runtime of O(N + K).** |
| Space | **O(K) — Requires a frequency array of size 2 * 10,000 + 1 = 20,001, which uses O(K) constant additional space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

When input values are bounded within a small known range, counting sort replaces comparison sorting for linear-time performance.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/array-partition/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
