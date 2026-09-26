# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Solutions:** 2 unique approach(es)  
> **Languages:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Find the single missing number from an array of n distinct numbers in the range [0, n].

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Math / Summation Formula

> **Language:** Java  
> **Runtime:** `0 ms`  
> **Memory:** `47.3 MB`

#### 💡 Intuition

The sum of all consecutive integers from 0 to n is known via Gauss's formula, n * (n + 1) / 2. Subtracting the actual sum of array elements from this expected total directly yields the missing number.

#### 🧠 Algorithmic Pattern

> **Math / Summation Formula**

#### 🚀 Approach

1. Calculate the expected sum of numbers from 0 to n using the formula n * (n + 1) / 2.
2. Iterate through the array nums to calculate the actual sum of all elements.
3. Subtract the actual sum from the expected sum.
4. Return the difference as the missing number.

#### ✅ Why This Works

Since the range [0, n] contains n + 1 elements and nums contains n elements with all values unique except for one missing value, the difference between the complete set's sum and the array's sum is exactly the missing element.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — A single linear pass over the array of length n is performed to compute the sum of elements.** |
| Space | **O(1) — Only a few primitive integer variables are used to keep track of the sums, using constant O(1) space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Mathematical summation formulas allow computing missing elements in O(n) time and O(1) auxiliary space without extra data structures.

---

### 🧠 Solution 2 — Bit Manipulation

> **Language:** Java  
> **Runtime:** `0 ms`  
> **Memory:** `47.1 MB`

#### 💡 Intuition

XORing a number with itself yields zero (x ^ x = 0) and XORing with zero leaves the number unchanged (x ^ 0 = x). If we XOR all indices from 0 to n together with all values present in nums, every present number appears twice (once as an index or n, and once as an array element) and cancels out to 0, leaving only the missing number.

#### 🧠 Algorithmic Pattern

> **Bit Manipulation**

#### 🚀 Approach

1. Initialize an accumulator variable xor with value n (the length of the array).
2. Iterate through each index i from 0 to n - 1.
3. In each iteration, update xor by XORing it with both index i and array element nums[i].
4. Return xor, which holds the missing number after all present pairs cancel out.

#### ✅ Why This Works

Because XOR is commutative and associative, pairing each index i with array element nums[i] creates pairs for every present number. The missing number appears only once (as an index/length value) and remains after all pairs evaluate to 0.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm makes a single pass through the array of length n, performing constant-time XOR operations per iteration.** |
| Space | **O(1) — Only a single primitive integer variable is maintained, resulting in O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Bitwise XOR is an optimal technique for missing or unique element problems because it operates in O(1) space and avoids potential integer overflow issues inherent to addition-based approaches.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
