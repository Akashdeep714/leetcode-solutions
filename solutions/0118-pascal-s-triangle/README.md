# 🧩 118. Pascal's Triangle

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Dynamic Programming  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/pascals-triangle/)

---

## 📝 Problem

Generate the first numRows of Pascal's Triangle.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Dynamic Programming / Tabulation

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `43.3 MB`

#### 💡 Intuition

Every element in Pascal's Triangle (except the boundary 1s) is the sum of the two elements directly above it in the previous row.

#### 🧠 Algorithmic Pattern

> **Dynamic Programming / Tabulation**

#### 🚀 Approach

1. Initialize the result list and add the base case row `[1]`.
2. Iterate `row` from 1 to `numRows - 1`.
3. For each row, initialize a new list with 1 as the first element.
4. Fill interior elements at index `i` by adding `prevRow[i - 1]` and `prevRow[i]`.
5. Append 1 at the end of the row and add the completed row to the output list.

#### ✅ Why This Works

Pascal's identity guarantees that element $C(n, k) = C(n-1, k-1) + C(n-1, k)$. Fetching values directly from the stored previous row computes each element in $O(1)$ time without duplicate calculations.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(numRows^2) — Row $r$ contains $r + 1$ elements. Summing $1 + 2 + \dots + \text{numRows}$ yields $\frac{\text{numRows}(\text{numRows} + 1)}{2}$ total operations, which is $O(\text{numRows}^2)$.** |
| Space | **O(1) — Ignoring memory required for the output list, only $O(1)$ auxiliary memory is used for iteration indices and pointers.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Constructing each row directly from the preceding row is simple, avoids integer overflow risks, and generates the entire triangle efficiently.

---

### 🧠 Solution 2 — Combinatorics / Math

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `43.4 MB`

#### 💡 Intuition

Row $n$ (0-indexed) consists of combination values $\binom{n}{0}, \binom{n}{1}, \dots, \binom{n}{n}$. Each term can be derived directly from the preceding term using $\binom{n}{k} = \binom{n}{k-1} \times \frac{n - k + 1}{k}$.

#### 🧠 Algorithmic Pattern

> **Combinatorics / Math**

#### 🚀 Approach

1. Iterate through row index `n` from `0` to `numRows - 1`.
2. Initialize the first element of row `n` as `res = 1`.
3. Iterate `i` from `1` to `n`, updating `res = res * (n - i + 1) / i` to derive each element.
4. Append each computed `res` value to the row and return all generated rows.

#### ✅ Why This Works

The relation $\binom{n}{k} = \binom{n}{k-1} \frac{n - k + 1}{k}$ allows computing element $k$ directly from element $k-1$ within the same row without constructing preceding rows of the triangle.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(numRows^2) — Generating row $n$ requires $n$ iterations. Across all `numRows`, total steps equal $1 + 2 + \dots + \text{numRows} = O(\text{numRows}^2)$.** |
| Space | **O(1) — Only $O(1)$ extra space is used for temporary arithmetic computations beyond the space allocated for the output structure.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Using the combination multiplication formula allows any single row of Pascal's Triangle to be generated independently in $O(n)$ time.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/pascals-triangle/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
