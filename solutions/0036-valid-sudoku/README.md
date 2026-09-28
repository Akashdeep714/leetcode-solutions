# 🧩 36. Valid Sudoku

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Hash Table · Matrix  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/valid-sudoku/)

---

## 📝 Problem

Validate a partially filled 9x9 Sudoku board to ensure digits 1-9 appear at most once per row, column, and 3x3 sub-box.

---

## 💡 Intuition

To validate the board in a single pass, we can track digits seen so far in each row, column, and sub-box using fixed-size 2D arrays. Calculating the sub-box index `3 * (r / 3) + (c / 3)` maps any cell `(r, c)` to one of nine distinct sub-boxes.

---

## 🧠 Algorithmic Pattern

> **Matrix Traversal / Hash Table (Array Lookup)**

---

## 🚀 Approach

1. Initialize three 9x9 2D integer arrays (`rows`, `cols`, `boxes`) to track presence of each digit (0 to 8) across rows, columns, and sub-boxes.
2. Iterate over every cell `(r, c)` in the 9x9 board.
3. Ignore empty cells marked with `.`.
4. Convert the character digit to a 0-indexed integer `val = board[r][c] - '1'` and compute the box index `boxIdx = 3 * (r / 3) + (c / 3)`.
5. Check if `val` has already been recorded in `rows[r][val]`, `cols[c][val]`, or `boxes[boxIdx][val]`. If so, return `false`.
6. Mark the digit as seen in all three tracking matrices and continue.
7. If the entire board is processed without finding duplicates, return `true`.

---

## ✅ Why This Works

Each cell belongs to exactly one row, one column, and one 3x3 sub-box. Updating and querying constant-size frequency arrays during traversal guarantees that duplicate digits are caught immediately upon first collision.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(1) — The board has a fixed size of 9x9 (81 cells). Checking and updating the lookup arrays per cell takes O(1) operations, yielding a total time of O(81) = O(1).** |
| Space | **O(1) — The auxiliary memory consists of three 9x9 integer arrays, which consume a fixed amount of memory independent of input values, yielding O(1) extra space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `46.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Fixed-size grids allow replacing dynamic hash sets with predictable 2D primitive arrays and coordinate arithmetic for constant-time constraint validation.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/valid-sudoku/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
