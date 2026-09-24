# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Given an array of integers nums and an integer target, return the indices of two numbers that add up to target.

---

## 💡 Intuition

Instead of checking every pair of numbers using nested loops, we can search for the required complement value in constant time using a hash map. For each element nums[i], the number needed to reach the target is lookupNumber = target - nums[i]. By keeping track of previously seen numbers and their indices in a hash map as we iterate, we can immediately identify if the complementary value was already encountered, allowing us to solve the problem in a single pass.

---

## 🧠 Algorithmic Pattern

> **Hash Table**

---

## 🚀 Approach

1. Initialize an empty hash map named map to store array values as keys and their corresponding indices as values.
2. Iterate through the array nums using a loop counter i from 0 to nums.length - 1.
3. Calculate the required complement for the current number: lookupNumber = target - nums[i].
4. Check if map already contains lookupNumber using map.containsKey(lookupNumber).
5. If lookupNumber is in map, return a new integer array containing the current index i and map.get(lookupNumber).
6. If lookupNumber is not in map, store the current element and its index by calling map.put(nums[i], i).
7. If the loop finishes without finding a matching pair, return [-1, -1] as a fallback.

---

## ✅ Why This Works

The equation nums[i] + nums[j] = target can be rewritten as nums[j] = target - nums[i]. By inserting each element into the hash map as we iterate, every element at index j < i is available for constant-time lookup. When the loop reaches the second number of the solution pair, its complement (the first number) is already stored in the hash map, ensuring the exact indices are found without duplicate checks or using the same element twice.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(n)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `47.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a hash map to look up complementary values (target - current_value) converts a slow O(n^2) pair search into an efficient O(n) single-pass algorithm.

---

---
### 🔀 Solution 2 — Brute Force

> **Language:** Java  
> **Runtime:** `98 ms`  
> **Memory:** `46.8 MB`

#### 💡 Intuition

The direct brute-force approach to finding two numbers that sum to a target is to examine every possible pair of elements in the array. Since the problem guarantees that exactly one valid solution exists and requires indices of distinct elements, iterating through all index combinations `(i, j)` where `i != j` and calculating `nums[i] + nums[j]` ensures we eventually test the pair that adds up to `target`.

#### 🧠 Algorithmic Pattern

> **Brute Force**

#### 🚀 Approach

1. Initialize a 2-element integer array `arr` to store the pair of matching indices.
2. Run an outer `for` loop with index `i` from `0` to `nums.length - 1` to pick the first number's index.
3. Run an inner `for` loop with index `j` from `0` to `nums.length - 1` to pick the second number's index.
4. Check if the indices are distinct (`i != j`) and if `nums[i] + nums[j] == target`.
5. When a matching pair is found, assign `i` to `arr[0]` and `j` to `arr[1]`.
6. Return the array `arr` containing the two answer indices.

#### ✅ Why This Works

By exhaustively evaluating all pairs of distinct indices `(i, j)` in `nums`, the algorithm is guaranteed to test the unique pair whose elements sum to `target`. When the condition `nums[i] + nums[j] == target` evaluates to true, storing `i` and `j` in the output array ensures the correct answer is captured and returned.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2) — The code uses two nested loops that each iterate over the array of length `n`, performing $n \times n = n^2$ comparisons in the worst case.** |
| Space | **O(1) — The code only allocates a fixed 2-element array to hold the result, consuming $O(1)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

---
### 🔀 Solution 3 — Brute Force

> **Language:** Java  
> **Runtime:** `52 ms`  
> **Memory:** `47 MB`

#### 💡 Intuition

This implementation uses a straightforward brute force search to test all distinct pairs of numbers in the array. By fixing a first number at index `i` and scanning all subsequent numbers at index `j` (where `j > i`), the code systematically evaluates every potential sum against the `target`. While simple, this exhaustive pair checking guarantees that the unique solution pair will eventually be evaluated.

#### 🧠 Algorithmic Pattern

> **Brute Force**

#### 🚀 Approach

1. Create a fixed-size array `arr` of size 2 to hold the resulting pair of indices.
2. Iterate through the array with an outer loop variable `i` from index `0` up to `nums.length - 1`.
3. For each index `i`, start an inner loop with variable `j` from index `i + 1` up to `nums.length - 1` to avoid using the same element twice.
4. Check if the sum `nums[i] + nums[j]` equals `target`.
5. When a matching pair is found, assign `i` to `arr[0]` and `j` to `arr[1]`.
6. After checking all pairs, return the array `arr` containing the matching indices.

#### ✅ Why This Works

The code exhaustively tests all $n(n - 1) / 2$ unique pairs of indices $(i, j)$ where $i < j$. Because the problem statement guarantees that exactly one valid solution exists, the nested loops will encounter this specific pair of indices and set `arr[0]` and `arr[1]` to `i` and `j` respectively before returning.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2) — The outer loop runs $n$ times and the inner loop runs on average $n/2$ times, leading to a total of $n(n - 1) / 2$ checks, which evaluates to $O(n^2)$ time.** |
| Space | **O(1) — Only a fixed 2-element array is allocated to store the output, requiring constant extra memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution-3.java)

---
### 🔀 Solution 4 — Two-Pass Hash Table

> **Language:** Java  
> **Runtime:** `5 ms`  
> **Memory:** `46.7 MB`

#### 💡 Intuition

Instead of checking every pair of numbers with nested loops in O(n²) time, we can reframe the problem from finding two numbers that sum to target into finding whether a single required complement exists. For any element nums[i], its complement is lookupNumber = target - nums[i]. By storing every element and its index in a hash map during an initial pass, we can instantly look up whether lookupNumber exists during a second pass, making sure not to use the same element index twice.

#### 🧠 Algorithmic Pattern

> **Two-Pass Hash Table**

#### 🚀 Approach

1. Initialize an empty hash map named map to store array values as keys and their corresponding indices as values.
2. Loop through the nums array from index 0 to nums.length - 1 to populate map with each element nums[i] and its index i.
3. Loop through the nums array a second time with index i.
4. In each iteration, calculate lookupNumber = target - nums[i].
5. Check if map contains lookupNumber as a key and ensure map.get(lookupNumber) != i so an element is not paired with itself.
6. If both conditions are met, return a new integer array containing map.get(lookupNumber) and i.
7. If no pair is found after completing the loop, return [-1, -1] as a fallback.

#### ✅ Why This Works

Any valid pair of numbers at distinct indices i and j satisfying nums[i] + nums[j] == target also satisfies nums[j] == target - nums[i]. Because the first pass inserts every array element into the hash map, the map is guaranteed to contain the complement lookupNumber if it exists in the array. Checking map.get(lookupNumber) != i prevents the algorithm from using the same array index twice when target is equal to 2 * nums[i].

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Iterating through the array twice takes O(n) time, and each hash map insertion and lookup operation takes O(1) average time.** |
| Space | **O(n) — The hash map stores up to n key-value pairs corresponding to the n elements in nums, requiring O(n) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-4.java)

---
### 🔀 Solution 5 — Hash Map / One-pass Hash Table

> **Language:** Java  
> **Runtime:** `2 ms`  
> **Memory:** `47.2 MB`

#### 💡 Intuition

Instead of checking every pair of numbers with nested loops in $O(n^2)$ time, we can rewrite the equation $a + b = \text{target}$ as $b = \text{target} - a$. As we iterate through the array, each number $a$ requires a specific complement $b$ to reach the target. By keeping track of previously seen numbers and their indices in a hash map, we can check if the complement $b$ has already been processed in $O(1)$ average time, completing the search in a single pass.

#### 🧠 Algorithmic Pattern

> **Hash Map / One-pass Hash Table**

#### 🚀 Approach

1. Initialize an empty hash map `map` to store each number as a key and its index as the value.
2. Iterate through the array `nums` from index `i = 0` to `nums.length - 1`.
3. For the current element `nums[i]`, compute its complement `lookupNumber = target - nums[i]`.
4. Check if `map.containsKey(lookupNumber)` evaluates to true.
5. If the complement exists in `map`, return an array containing `i` and `map.get(lookupNumber)`.
6. If the complement is not present, store the current number and index by calling `map.put(nums[i], i)`.
7. Return `{-1, -1}` as a fallback if the loop completes without finding a valid pair.

#### ✅ Why This Works

By adding elements to the hash map as we iterate rather than pre-populating it, any lookup for `target - nums[i]` will only match elements at indices strictly less than `i`. This naturally prevents an element from being paired with itself. Because exactly one valid pair exists, the second element of the target pair will always find the first element already stored in the hash map.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We iterate through the array of length $n$ once, performing average $O(1)$ hash map lookup and insertion operations for each element.** |
| Space | **O(n) — In the worst case, the hash map stores up to $n - 1$ elements before finding the target pair.** |

#### 💻 Solution

[View the complete Java solution →](./solution-5.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
