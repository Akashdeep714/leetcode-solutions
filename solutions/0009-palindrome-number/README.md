# 9. Palindrome Number

> **Difficulty:** 🟢 Easy
>
> **Topics:** Math
>
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Determine whether an integer is a palindrome (reads the same forward and backward) without converting it to a string.

---

## 💡 Intuition

A number is a palindrome if reversing its digits yields the exact original value. Negative numbers are never palindromes because of the minus sign. By repeatedly stripping off the last digit of the number using modulo operations and appending it to a new number, we can reverse the integer mathematically and compare it to the original.

---

## 🧠 Algorithmic Pattern

> **Math / Digit Manipulation**

---

## 🚀 Approach

1. Check if `x` is negative; if so, immediately return `false` because negative signs prevent palindrome symmetry.
2. Initialize a temporary variable `n` equal to `x` to keep the original value of `x` intact, and set `revNum` to `0`.
3. Loop while `n` is greater than `0`.
4. Extract the last digit of `n` using `d = n % 10`.
5. Append `d` to `revNum` by multiplying `revNum` by `10` and adding `d`.
6. Remove the last digit from `n` using integer division `n = n / 10`.
7. After the loop, compare `revNum` to `x` and return `true` if they are equal, or `false` otherwise.

---

## ✅ Why This Works

The operation `n % 10` isolates the rightmost digit of `n`, and `revNum * 10 + d` appends this digit to `revNum`, effectively processing the digits of `x` from right to left. Integer division `n / 10` shifts `n` right by one decimal place. Once all digits are processed, `revNum` contains the exact reverse of `x`, making `revNum == x` a direct and accurate symmetry test.

---

## ⏱️ Complexity

| Metric | Complexity |
| ---- | --------------------------------------------------------------------------------------------------------------------- |
| Time | **O(log10(x)) — The number of iterations equals the total number of digits in x, which is proportional to log10(x).** |
| Space | **O(1) — The solution uses a constant amount of memory with only a few primitive integer variables (n, revNum, d).** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `4 ms` |
| Memory | `46.08 MB` |

---

## 💻 Solution

[View the complete Java solution →](https://github.com/Akashdeep714/leetcode-solutions/blob/main/solutions/0009-palindrome-number/solution.java)

---

## 🎯 Key Takeaway

Digits of a base-10 integer can be processed from right to left using modulo (`% 10`) to extract the last digit and integer division (`/ 10`) to drop it, avoiding string conversion.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](https://github.com/Akashdeep714/leetcode-solutions/blob/main/solutions/0009-palindrome-number/solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission
