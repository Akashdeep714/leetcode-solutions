# 🧩 7. Reverse Integer

> **Difficulty:** 🟡 Medium  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/reverse-integer/)

---

## 📝 Problem

Reverse the decimal digits of a 32-bit signed integer and return 0 if the reversed result overflows the 32-bit signed integer range.

---

## 💡 Intuition

Digits can be popped from the end of a number using modulo 10 and pushed onto a new number by multiplying by 10 and adding the digit. To avoid integer overflow in a 32-bit environment, we must check whether multiplying the accumulated result by 10 will exceed the 32-bit integer bounds before actually performing the multiplication.

---

## 🧠 Algorithmic Pattern

> **Mathematical Digit Extraction & Bound Checking**

---

## 🚀 Approach

1. Initialize `rev = 0` to store the reversed integer.
2. Iterate while input `x` is not equal to zero.
3. Extract the last digit using `x % 10`.
4. Check for potential overflow: if `rev` is greater than `Integer.MAX_VALUE / 10` (or equal and digit > 7), or less than `Integer.MIN_VALUE / 10` (or equal and digit < -8), return 0 immediately.
5. Append the extracted digit to `rev` via `rev = rev * 10 + digit` and reduce `x` by integer division `x / 10`.
6. Return `rev` after the loop completes.

---

## ✅ Why This Works

The maximum 32-bit signed integer is 2,147,483,647 and the minimum is -2,147,483,648. Checking `rev` against `MAX_VALUE / 10` (214,748,364) before multiplying ensures that `rev * 10 + digit` never exceeds the valid range or triggers undefined/overflow behavior.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log10(|x|)) — The number of digits in an integer $x$ is $\lfloor \log_{10}(|x|) \rfloor + 1$. Since $x$ is bounded by 32 bits, the loop executes at most 10 times, making it $O(1)$ in practice.** |
| Space | **O(1) — Only a few primitive integer variables are maintained for the state, using $O(1)$ auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `42.4 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When strict hardware or runtime constraints prohibit 64-bit arithmetic, integer bounds must be validated mathematically prior to performing potentially overflowing arithmetic operations.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/reverse-integer/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
