# 🧩 66. Plus One

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/plus-one/)

---

## 📝 Problem

Increment an integer represented as an array of digits by one and return the updated digit array.

---

## 💡 Intuition

Standard addition starts from the least significant digit (the end of the array). If a digit is less than 9, incrementing it finishes the addition immediately with no carry. If a digit is 9, incrementing turns it into 0 and propagates a carry of 1 to the left. If all digits were 9, an overflow occurs requiring a new array with an extra leading digit.

---

## 🧠 Algorithmic Pattern

> **Array Traversal / Arithmetic Carry Propagation**

---

## 🚀 Approach

1. Iterate backwards through the `digits` array starting from the last index (`digits.length - 1`) down to `0`.
2. If the current digit `digits[i]` is 9, change it to 0 and continue to the next left digit to carry over the 1.
3. If `digits[i]` is less than 9, increment `digits[i]` by 1 and immediately return `digits` as no carry remains.
4. If the loop finishes entirely, all original digits were 9 (e.g., `[9, 9]`). Allocate a new array of size `digits.length + 1`, set the first element to 1, and return it.

---

## ✅ Why This Works

In base-10 addition, incrementing a digit only generates a carry when the digit transitions from 9 to 10. By replacing 9s with 0s and incrementing the first digit smaller than 9, we correctly perform addition in place. The edge case where all digits are 9 results in $99\dots9 + 1 = 100\dots0$, which cleanly maps to a newly allocated array of size $N+1$ with `res[0] = 1` and default 0s.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — In the worst case (all digits are 9), we traverse all $N$ digits once, taking $O(N)$ time. In the best case, the last digit is less than 9, allowing the method to terminate in $O(1)$ time.** |
| Space | **O(1) — The computation modifies the input array in-place, using $O(1)$ extra space for typical cases. Only when all $N$ digits are 9 is a new array of size $N + 1$ allocated, taking $O(N)$ space.** |

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

By handling the carry sequentially from right to left and returning early upon the first non-9 digit, we avoid unnecessary work and avoid extra array allocations in most cases.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/plus-one/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
