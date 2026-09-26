# 🧩 189. Rotate Array

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Math · Two Pointers  
> **Solutions:** 2 unique approach(es)  
> **Languages:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/rotate-array/)

---

## 📝 Problem

Rotate an array of n integers to the right by k steps in-place.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Two Pointers / Array Reversal

> **Language:** Java  
> **Runtime:** `5 ms`  
> **Memory:** `268.6 MB`

#### 💡 Intuition

Rotating right by k moves the last k elements to the front and shifts the first n - k elements to the back. Reversing the entire array swaps the relative positions of these two blocks, but leaves each block internally inverted. Reversing the first k elements and the remaining n - k elements restores internal order, completing the rotation.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Array Reversal**

#### 🚀 Approach

1. Normalize k using modular arithmetic (k = k % n) to handle k greater than or equal to array length n.
2. If k % n == 0, return early as the array remains unchanged.
3. Reverse the entire array from index 0 to n - 1.
4. Reverse the first k elements from index 0 to k - 1.
5. Reverse the remaining n - k elements from index k to n - 1.

#### ✅ Why This Works

Reversing the entire array moves the tail section (length k) to the head and the head section (length n - k) to the tail. Since reversing flips element order within each section, applying two subsequent localized reversals corrects the order of elements within both sections.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Reversing the array requires n / 2 swaps total across all three reversal steps (n/2 + k/2 + (n-k)/2 = n swaps), yielding linear O(n) time complexity.** |
| Space | **O(1) — The reversals are done in-place using two pointers and a scalar temporary swap variable, using O(1) extra memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Block-based cyclic shifts on contiguous memory can often be performed in-place by combining global and sub-array reversal operations.

---

### 🧠 Solution 2 — Cycle Decomposition / Modular Arithmetic

> **Language:** Java  
> **Runtime:** `8 ms`  
> **Memory:** `268.7 MB`

#### 💡 Intuition

Every element at index idx belongs to a cyclic chain defined by target position next = (idx + k) % n. Following this chain lets us place each element directly into its target index while carrying the displaced value to the next target. Repeating this for all disjoint cycles places every element into place without extra array allocation.

#### 🧠 Algorithmic Pattern

> **Cycle Decomposition / Modular Arithmetic**

#### 🚀 Approach

1. Maintain a count variable tracking the total number of elements successfully placed.
2. Iterate starting cycle heads from index i = 0 up until count equals n.
3. Store the starting element value in a variable curr and traverse the cycle using idx = (idx + k) % n.
4. Swap curr with the value at the new target index, update idx, and increment count.
5. Continue until returning to the cycle start index i, then increment i to begin the next disjoint cycle.

#### ✅ Why This Works

The permutation formed by rotating right by k decomposes into exactly gcd(n, k) disjoint cycles. Traversing every cycle until all n elements are moved guarantees each element reaches its correct rotated destination.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Every element is visited and placed in its correct destination exactly once across all cycle loops, performing n total placement operations for O(n) time.** |
| Space | **O(1) — Cycle traversal only requires scalar temporary variables (curr, next, count, idx), running in O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

In-place array permutations can be executed in optimal time and space by tracing disjoint cycle paths.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/rotate-array/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
