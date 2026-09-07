# 🧩 9. Palindrome Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Determine whether a given integer is a palindrome, meaning it reads the same forward and backward.

---

## 💡 Intuition

A number is a palindrome if reversing its digits yields the exact same number. Negative numbers can never be palindromes due to the leading minus sign. By extracting digits from right to left using modulo and building a new reversed number using multiplication and addition, we can directly compare the reversed value to the original number.

---

## 🧠 Algorithmic Pattern

> **Math / Digit Manipulation**

---

## 🚀 Approach

1. Check if the input integer `x` is negative; if so, immediately return `false`.
2. Store a copy of `x` in a variable `n` and initialize `revNum` to `0` to hold the reversed number.
3. Loop while `n > 0` to process each digit from right to left.
4. Extract the last digit of `n` using `d = n % 10`.
5. Shift `revNum` one decimal place to the left and add `d` (`revNum = revNum * 10 + d`).
6. Remove the last digit from `n` using integer division (`n = n / 10`).
7. Compare `revNum` with the original `x` and return `true` if they match, otherwise return `false`.

---

## ✅ Why This Works

Repeatedly applying `% 10` isolates the rightmost digit of `n`, and appending it to `revNum` via `revNum * 10 + d` constructs the reverse of `x` from left to right. Once all digits are processed, `revNum` represents the exact numerical reverse of `x`. If `revNum == x`, the number is symmetrical and therefore a palindrome.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `4` |
| Memory | `46080000` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using modulo (`% 10`) and division (`/ 10`) allows you to manipulate and reverse integer digits directly without relying on string conversion or extra memory allocations.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
