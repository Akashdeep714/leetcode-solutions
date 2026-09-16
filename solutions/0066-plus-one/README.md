# 🧩 66. Plus One

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/plus-one/)

---

## 📝 Problem

Given an array of digits representing a non-negative integer with the most significant digit at index 0, add 1 to the integer and return the resulting digit array.

---

## 💡 Intuition

When adding 1 to a number digit by digit from right to left, a carry is only generated if the current digit is 9. If a digit is less than 9, incrementing it increases the overall number by 1 without producing a carry, allowing us to return the modified array immediately. If a digit is 9, adding 1 turns it into 0 and passes a carry of 1 to the next digit to the left. The only edge case where the carry propagates past the most significant digit is when every digit is 9 (e.g., 999 becomes 1000), which requires allocating a new array of length n + 1 with a leading 1.

---

## 🧠 Algorithmic Pattern

> **Right-to-Left Array Traversal**

---

## 🚀 Approach

1. Iterate backward through the `digits` array starting from the last element at index `digits.length - 1` down to index `0`.
2. For the current index `i`, check if `digits[i]` is equal to `9`.
3. If `digits[i] == 9`, set `digits[i] = 0` to handle the carry and continue the loop to process the next digit to the left.
4. If `digits[i]` is not `9`, increment `digits[i]` by `1` (`digits[i] = digits[i] + 1`) and immediately return the modified `digits` array.
5. If the loop finishes completely without returning, it means every digit in the original array was `9` and has been changed to `0`.
6. Create a new integer array `res` of size `digits.length + 1`.
7. Set `res[0] = 1` (the remaining elements default to `0`) and return `res`.

---

## ✅ Why This Works

The algorithm mimics elementary right-to-left addition. Incrementing a digit less than 9 resolves the addition locally because $d + 1 < 10$, generating zero carry and rendering all digits to the left unchanged. Conversely, $9 + 1 = 10$, which leaves a remainder digit of $0$ and carries $1$ to the next position. If all $n$ digits are $9$, every digit becomes $0$ and a final carry of $1$ remains, which requires an additional digit position; placing $1$ at index $0$ of an array of length $n + 1$ correctly forms $10^n$.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(n)** |

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

Right-to-left array processing allows early termination as soon as carry propagation stops, while overflow beyond the most significant digit can be handled cleanly by allocating a new array extended by one index.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/plus-one/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
