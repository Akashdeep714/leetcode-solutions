# 🧩 1299. Replace Elements with Greatest Element on Right Side

> **Difficulty:** 🟢 Easy  
> **Topics:** Array  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/)

---

## 📝 Problem

Replace each element in an array with the largest element located to its right, replacing the last element with -1.

---

## 💡 Intuition

Finding the greatest element to the right of each position by scanning forward from left to right would require checking all remaining elements for every index, leading to quadratic time complexity. By reversing the direction and traversing from right to left, we can maintain a running maximum of all elements encountered so far. For any position, this running maximum represents the exact value needed to replace the current element, allowing us to update the array in a single pass.

---

## 🧠 Algorithmic Pattern

> **Right-to-Left Traversal**

---

## 🚀 Approach

1. Initialize a variable `max` to `-1`, representing the running maximum of elements to the right of the current index.
2. Loop backwards through the array starting from the last index (`arr.length - 1`) down to `0`.
3. At each index `i`, store the original value of `arr[i]` in a variable `temp` before modifying the array.
4. Replace `arr[i]` with `max`.
5. Update `max` to `Math.max(max, temp)` so that it includes the original element at index `i` for subsequent steps to the left.
6. Return the modified array `arr` after the loop completes.

---

## ✅ Why This Works

At each index `i` during a right-to-left traversal, `max` stores the maximum value among all original elements strictly to the right of `i`. Because we save `arr[i]` in `temp` before overwriting `arr[i]` with `max`, we can correctly update `max` using `Math.max(max, temp)` to include `arr[i]` in the suffix maximum for index `i - 1` without losing the original element's value.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The code uses a single loop that traverses the array of length n once from right to left, performing constant-time operations at each index.** |
| Space | **O(1) — The algorithm modifies the input array in-place using only two integer variables (`max` and `temp`), requiring O(1) extra space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `3 ms` |
| Memory | `49.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When a problem requires computing suffix properties (like the maximum element to the right), traversing the array backwards enables update-and-query operations in O(1) space and O(n) time.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
