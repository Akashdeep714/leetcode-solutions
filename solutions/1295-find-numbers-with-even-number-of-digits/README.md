# 🧩 1295. Find Numbers with Even Number of Digits

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/)

---

## 📝 Problem

Given an array of positive integers, count and return how many numbers contain an even number of digits.

---

## 💡 Intuition

To check if an integer has an even number of digits, we can convert the integer into its string representation. Because each digit corresponds to exactly one character in the string, the length of the string directly gives the total count of digits. Checking if this length is divisible by 2 reveals whether the digit count is even.

---

## 🧠 Algorithmic Pattern

> **String Conversion / Array Iteration**

---

## 🚀 Approach

1. Initialize a counter variable `evenCount` to `0` to keep track of numbers with an even number of digits.
2. Iterate through each integer `num` in the `nums` array using a loop.
3. Convert `num` to its string representation using `String.valueOf(num)` and compute its length using `.length()`, storing the value in `len`.
4. Check if `len` is even using the condition `len % 2 == 0`.
5. If the condition is met, increment `evenCount` by `1`.
6. After iterating through all numbers in `nums`, return `evenCount`.

---

## ✅ Why This Works

For positive integers, string conversion maps each decimal place to exactly one character without extra symbols like minus signs. Therefore, `String.valueOf(num).length()` accurately counts the number of digits in `num`, and the modulo arithmetic `len % 2 == 0` correctly identifies even digit counts.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Iterating through the array of $n$ elements takes $O(n)$ time, and converting each integer up to $10^5$ to a string takes bounded $O(1)$ time since numbers have at most 6 digits.** |
| Space | **O(1) — The algorithm creates a temporary string of at most 6 characters per iteration, using $O(1)$ auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `45.7 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Converting an integer to a string is a simple and clean way to determine its digit length without manually writing a digit-counting division loop.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
