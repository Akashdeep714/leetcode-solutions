# 🧩 498. Diagonal Traverse

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Matrix · Simulation  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/diagonal-traverse/)

---

## 📝 Problem

Return all elements of an m x n matrix in a diagonal zigzag order.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Matrix Diagonal Traversal / Outer Loop by Diagonal Index

> **Language:** Java
> **Runtime:** `6 ms`  
> **Memory:** `47.6 MB`

#### 💡 Intuition

Every cell (r, c) on the same diagonal shares a constant sum i = r + c. There are m + n - 1 total diagonals. By iterating over diagonal indices from 0 to m + n - 2, we can determine the starting boundaries for each diagonal, collect all cells along that diagonal from top-right to bottom-left, and reverse the collected list for alternating diagonals to achieve the required upward movement.

#### 🧠 Algorithmic Pattern

> **Matrix Diagonal Traversal / Outer Loop by Diagonal Index**

#### 🚀 Approach

1. Loop i from 0 to m + n - 2 representing each diagonal index sum.
2. Determine the starting row and column indices for the i-th diagonal.
3. Traverse down-left along the diagonal (rowIdx++, colIdx--) while remaining within matrix bounds.
4. If the diagonal index i is even, store elements in a temporary list and reverse it before adding to the result array to simulate upward traversal.
5. If the diagonal index i is odd, append elements directly to the result array.

#### ✅ Why This Works

Cells in any diagonal satisfy r + c = constant. Grouping elements by this property ensures complete and orderly traversal of every diagonal, while selective list reversal correctly matches the required alternating directions.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m * n) — Every element of the m x n matrix is visited once during diagonal collection and once during array copy, taking O(m * n) total operations.** |
| Space | **O(min(m, n)) — An auxiliary temporary list is used to store elements of a single diagonal before reversal. The maximum size of a diagonal in an m x n matrix is min(m, n), consuming O(min(m, n)) extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using the mathematical property (r + c = constant) simplifies boundary determination for matrix diagonals and simplifies direction handling via temporary reversal.

---

### 🧠 Solution 2 — State Machine / Directional Matrix Simulation

> **Language:** Java
> **Runtime:** `4 ms`  
> **Memory:** `48 MB`

#### 💡 Intuition

Instead of processing whole diagonals at once, we can simulate the trajectory of a moving point. Maintain a single direction indicator (1 for moving up-right, -1 for moving down-left). Move cell by cell until a boundary is hit, then flip the direction and adjust the row/column to enter the next diagonal.

#### 🧠 Algorithmic Pattern

> **State Machine / Directional Matrix Simulation**

#### 🚀 Approach

1. Initialize pointers rowIdx = 0, colIdx = 0, and dir = 1 (upward-right direction).
2. For each step up to m * n, copy mat[rowIdx][colIdx] into the result array.
3. Compute the tentative next position: (rowIdx - dir, colIdx + dir).
4. Check if the tentative position is out of matrix bounds. If within bounds, update (rowIdx, colIdx) directly.
5. If out of bounds, flip direction (dir = -dir) and shift coordinates according to corner/edge conditions (prefer moving right if moving up-right hits a boundary, otherwise move down; prefer moving down if moving down-left hits a boundary, otherwise move right).

#### ✅ Why This Works

The boundaries of the matrix naturally force a direction flip and a coordinate reset. Explicitly handling boundary conditions keeps coordinate updates correct without requiring auxiliary collections or intermediate lists.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m * n) — The algorithm visits each cell in the m x n matrix exactly once in sequence, performing O(1) coordinate updates per cell, yielding O(m * n) overall time.** |
| Space | **O(1) — Only constant O(1) additional variables (pointers and direction flag) are used, excluding the output array.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Simulating pointer movement with direct boundary reflections allows O(1) extra space matrix traversal without intermediate data structures.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/diagonal-traverse/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
