# 🧩 119. Pascal's Triangle II

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Dynamic Programming  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/pascals-triangle-ii/)

---

## 📝 Problem

Return the rowIndex-th (0-indexed) row of Pascal's triangle.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Dynamic Programming

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `42.8 MB`

#### 💡 Intuition

Each entry in Pascal's triangle (except the boundaries) is the sum of the two adjacent entries in the row directly above it. We can start with the 0-th row containing just [1] and iteratively generate each subsequent row up to rowIndex using the previous row's values.

#### 🧠 Algorithmic Pattern

> **Dynamic Programming**

#### 🚀 Approach

1. Initialize the 0-th row as a list with a single element: [1].
2. Iterate through row indices from 1 up to rowIndex.
3. For each new row, set the boundary element to 1, then calculate intermediate elements by summing prev.get(i) and prev.get(i - 1).
4. Append a final 1 to the current row and update the previous row pointer to reference the current row.
5. Return the last constructed row after reaching rowIndex.

#### ✅ Why This Works

By definition, C(n, k) = C(n - 1, k - 1) + C(n - 1, k). Building rows sequentially guarantees that all values from row (n - 1) are computed before row n needs them.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(k^2) — Generating row i requires computing i + 1 elements. Summing across all rows from 0 to k takes 1 + 2 + ... + (k + 1) = O(k^2) total operations, where k is rowIndex.** |
| Space | **O(k) — At any given point, only two rows (the previous row and the current row being built) are kept in memory, each using at most O(k) extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Simulating the row-by-row additive construction directly mimics Pascal's definition and requires space for only the current and previous rows.

---

### 🧠 Solution 2 — Math / Combinatorics

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `42.4 MB`

#### 💡 Intuition

The elements of the n-th row in Pascal's triangle correspond to the binomial coefficients C(n, 0), C(n, 1), ..., C(n, n). Consecutive coefficients satisfy the mathematical recurrence C(n, i) = C(n, i - 1) * (n - i + 1) / i. This allows each element to be computed in O(1) time directly from the preceding element without computing intermediate rows.

#### 🧠 Algorithmic Pattern

> **Math / Combinatorics**

#### 🚀 Approach

1. Initialize the result row list starting with the first element C(n, 0) = 1.
2. Iterate i from 1 to rowIndex.
3. Compute C(n, i) from C(n, i - 1) using the formula: C(n, i) = C(n, i - 1) * (rowIndex - i + 1) / i.
4. Use 64-bit integer arithmetic (long) during multiplication to prevent integer overflow before dividing by i.
5. Cast the result to an integer and append it to the row.

#### ✅ Why This Works

The ratio C(n, i) / C(n, i - 1) simplifies algebraically to (n - i + 1) / i. Multiplying the previous element by this factor directly yields the current element.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(k) — The loop executes k times (where k is rowIndex), with each iteration performing basic arithmetic operations in O(1) time, resulting in O(k) total runtime.** |
| Space | **O(1) — Excluding the output list of size k + 1 required for the result, the algorithm uses O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Binomial coefficient recurrence relations allow direct linear-time generation of any single row of Pascal's triangle.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/pascals-triangle-ii/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
