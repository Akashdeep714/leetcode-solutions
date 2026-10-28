# 🧩 747. Largest Number At Least Twice of Others

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/largest-number-at-least-twice-of-others/)

---

## 📝 Problem

Find whether the unique maximum element in an array is at least twice as large as every other element, returning its index if true or -1 if false.

---

## 💡 Intuition

To check if the largest number in an array is at least twice as big as every other element, we do not need to compare it against every single number individually. It is mathematically sufficient to compare the largest element (`max1`) with the second-largest element (`max2`). If `max1 >= 2 * max2`, then `max1` is guaranteed to be at least twice as large as all other, even smaller, elements. We can track both the top two maximum values and the index of the largest value in a single traversal through the array.

---

## 🧠 Algorithmic Pattern

> **Single Pass Tracking Top Two Elements**

---

## 🚀 Approach

1. Initialize `idx`, `max1`, and `max2` to `-1` to store the index of the largest element, the largest value, and the second-largest value seen so far.
2. Iterate through the array `nums` from index `0` to `nums.length - 1`.
3. For each element `nums[i]`, if it is strictly greater than `max1`, demote the current `max1` to `max2`, update `max1` to `nums[i]`, and set `idx = i`.
4. Else, if `nums[i]` is strictly greater than `max2`, update `max2` to `nums[i]`.
5. After completing the loop, check if `max1 >= 2 * max2`. If true, return `idx`; otherwise, return `-1`.

---

## ✅ Why This Works

Because all elements in the array are non-negative, any element $x$ other than `max1` satisfies $x \le \text{max2}$. Multiplying both sides by 2 yields $2x \le 2 \cdot \text{max2}$. Therefore, if $\text{max1} \ge 2 \cdot \text{max2}$, it follows by transitivity that $\text{max1} \ge 2x$ for every element $x \neq \text{max1}$. Maintaining the top two largest elements in a single pass accurately captures both `max1` and `max2` required for this condition.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The code iterates through the array of length $n$ exactly once, performing constant-time comparisons and variable updates at each step.** |
| Space | **O(1) — Only three primitive integer variables (`idx`, `max1`, `max2`) are used, requiring $O(1)$ constant auxiliary space.** |

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

When a condition must hold relative to all other elements in an array, identifying the top one or two extreme values (like max and second-max) can reduce the problem to a single-pass scan with a single final check.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/largest-number-at-least-twice-of-others/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
