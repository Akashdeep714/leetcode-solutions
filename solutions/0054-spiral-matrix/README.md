# 🧩 54. Spiral Matrix

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Matrix · Simulation  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/spiral-matrix/)

---

## 📝 Problem

Traverse an m x n 2D matrix in clockwise spiral order and return all of its elements in a single 1D list.

---

## 💡 Intuition

A clockwise spiral traversal decomposes into alternating horizontal and vertical movements whose segment lengths decrease over time. Starting from row 0 and column -1, moving right covers all $n$ columns, after which the top row is consumed and the remaining usable row count $m$ drops by 1. Moving down then covers the remaining $m$ rows, consuming the rightmost column and reducing the available column count $n$ by 1. Reversing the movement step with a direction multiplier `dir = -1` switches the motion to leftward and upward. By continually toggling `dir` between 1 and -1 while shrinking $m$ and $n$, the traversal perfectly spirals inward without needing a separate visited matrix or four explicit boundary pointers.

---

## 🧠 Algorithmic Pattern

> **Matrix Simulation**

---

## 🚀 Approach

1. Initialize row index `i = 0`, column index `j = -1`, available row count `m = matrix.length`, available column count `n = matrix[0].length`, and direction step `dir = 1`.
2. Execute a loop that continues as long as there are remaining rows (`m > 0`) and remaining columns (`n > 0`).
3. Traverse horizontally `n` times: update column index `j += dir`, append `matrix[i][j]` to `res`, and decrement remaining rows `m` by 1.
4. Traverse vertically `m` times: update row index `i += dir`, append `matrix[i][j]` to `res`, and decrement remaining columns `n` by 1.
5. Invert the movement direction by updating `dir = dir * -1` so the next pass moves in the opposite directions (left and up).
6. Return the accumulated result list `res` once either `m` or `n` reaches 0.

---

## ✅ Why This Works

Horizontal traversals process $n$ unvisited cells in the current row before decreasing $m$, guaranteeing that the row is not revisited. Vertical traversals process $m$ unvisited cells in the current column before decreasing $n$, guaranteeing that the column is retired. Multiplying `dir` by -1 toggles step direction between forward (+1 for right/down) and backward (-1 for left/up). Because each step consumes a complete row or column boundary and exact coordinate offsets match the shrinking inner matrix dimensions, every cell is visited exactly once in clockwise order.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m * n) — Each of the m * n cells in the matrix is processed and appended to the output list exactly once.** |
| Space | **O(1) — Ignoring the space required for the output list, the algorithm uses only a few scalar variables for tracking indices and bounds.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `43.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Alternating horizontal and vertical segments while toggling a direction sign (+1 / -1) and decrementing active row/column counts provides an elegant way to simulate spiral matrix traversals.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/spiral-matrix/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
