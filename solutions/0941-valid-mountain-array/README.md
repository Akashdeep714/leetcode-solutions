# 🧩 941. Valid Mountain Array

> **Difficulty:** 🟢 Easy  
> **Topics:** Array  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/valid-mountain-array/)

---

## 📝 Problem

Check if an integer array forms a valid mountain structure, strictly increasing to a peak and then strictly decreasing to the end.

---

## 💡 Intuition

Thinking of the array as a elevation map, a valid mountain must go strictly uphill to a single peak and then strictly downhill to the very end. We can simulate climbing this mountain with a single pointer: first advance as long as elements are strictly increasing. Once the climb stops, we check if we actually climbed (the peak isn't at the very start) and if there is a slope left to descend (the peak isn't at the very end). If these conditions hold, we continue walking downhill while elements are strictly decreasing. If the pointer successfully reaches the final element, the array is a valid mountain.

---

## 🧠 Algorithmic Pattern

> **Two-Phase Linear Scan**

---

## 🚀 Approach

1. Initialize a index pointer `i = 0` and store the array length in `n`.
2. Advance `i` in a loop as long as `i + 1 < n` and `arr[i] < arr[i + 1]` to traverse the strictly increasing climb.
3. Check if `i == 0` (no initial climb) or `i == n - 1` (no subsequent descent); if either is true, return `false` immediately.
4. Advance `i` in a second loop as long as `i + 1 < n` and `arr[i] > arr[i + 1]` to traverse the strictly decreasing descent.
5. Return `true` if `i == n - 1`, confirming that the descent reached the last element of the array.

---

## ✅ Why This Works

A valid mountain must consist of a non-empty strictly increasing prefix followed by a non-empty strictly decreasing suffix that spans the entire array. The first `while` loop locates the end of the initial strictly increasing sequence. Rejecting peaks at index `0` or `n - 1` guarantees both the climb and descent phases are non-empty. The second `while` loop then validates that every remaining element strictly decreases; reaching index `n - 1` proves that the entire array fits the exact peak specification without any flat regions or secondary climbs.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The pointer `i` starts at index 0 and only moves forward, visiting each element of the array at most once.** |
| Space | **O(1) — The implementation only uses two integer variables (`i` and `n`) to track the traversal, requiring constant memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `47.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

A single pointer advancing through monotonic phases in sequence can validate structural sequence requirements (like an increasing-then-decreasing mountain) in linear time and constant space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/valid-mountain-array/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
