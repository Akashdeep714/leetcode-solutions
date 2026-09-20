# 🧩 48. Rotate Image

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Math · Matrix  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/rotate-image/)

---

## 📝 Problem

Rotate an n x n 2D matrix 90 degrees clockwise in-place without allocating another 2D matrix.

---

## 💡 Intuition

Rotating a matrix 90 degrees clockwise can be visualised as rotating concentric square layers from the outermost border toward the center. Within each layer, every element belongs to a 4-element cyclic group formed by one cell from each of the four sides. By computing the offset `del = j - i` for the current cell on the top side, we can shift values along this four-cell cycle sequentially using temporary variables, directly updating all four locations without clobbering unread values or using extra matrix memory.

---

## 🧠 Algorithmic Pattern

> **Layer-by-Layer 4-Way Cyclic Swap**

---

## 🚀 Approach

1. Determine the dimension n from matrix.length.
2. Loop layer index i from 0 up to n - 1, representing the current concentric outer layer.
3. For each layer i, iterate j from i to n - i - 2 (stopping before the layer's corner element to avoid duplicate processing).
4. Calculate the current position's offset del = j - i within the layer.
5. Perform a 4-way cyclic shift of values using auxiliary variables curr and next across four positions: top (i, j), right (i + del, n - 1 - i), bottom (n - 1 - i, n - 1 - i - del), and left (n - 1 - i - del, i).
6. Assign the last held value back to the top position matrix[i][j] to complete the cyclic rotation.

---

## ✅ Why This Works

A 90-degree clockwise rotation maps any cell at coordinate (r, c) to position (c, n - 1 - r). Applying this coordinate mapping four times sequentially traces a closed loop of four distinct positions on the matrix grid. Because the inner loops partition the entire grid into disjoint 4-element cycles across all concentric rings, executing a 4-way cyclic swap for each group guarantees every entry reaches its correct rotated destination in-place without overwriting unvisited values.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n^2)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `43.7 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

In-place matrix rotations can be achieved by partitioning the matrix into concentric rings and performing 4-way cyclic shifts on corresponding cell groups along each layer.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/rotate-image/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
