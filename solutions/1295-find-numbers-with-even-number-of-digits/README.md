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

---
### 🔀 Solution 2 — Math / Logarithmic Digit Counting

> **Language:** Java  
> **Runtime:** `1 ms`  
> **Memory:** `44.8 MB`

#### 💡 Intuition

To determine if an integer has an even number of digits, we need its digit count. Instead of converting each number to a string or repeatedly dividing by 10 in a loop, we can leverage the mathematical property of base-10 logarithms. For any positive integer $n$, $\log_{10}(n)$ tells us the power of 10 needed to equal $n$. Floor-evaluating this value and adding 1 gives the exact number of digits in constant time. Once we have the digit count, checking if it is even reduces to a simple modulo arithmetic check.

#### 🧠 Algorithmic Pattern

> **Math / Logarithmic Digit Counting**

#### 🚀 Approach

1. Initialize `evenCount` to 0 to keep track of integers that have an even number of digits.
2. Iterate through each integer `num` in the array `nums`.
3. Calculate the digit count using `digitCount = (int) Math.floor(Math.log10(num)) + 1`.
4. Evaluate if `digitCount` is even by checking if `digitCount % 2 == 0`.
5. If the condition is met, increment `evenCount` by 1.
6. Return `evenCount` after processing all elements in `nums`.

#### ✅ Why This Works

For any positive integer $x$, the range $10^{d-1} \le x < 10^d$ corresponds to numbers with exactly $d$ digits. Taking the base-10 logarithm yields $d-1 \le \log_{10}(x) < d$. Floor-truncating $\log_{10}(x)$ rounds down to $d-1$, so adding $1$ precisely recovers the digit count $d$. Checking `digitCount % 2 == 0` correctly identifies whether $d$ is an even number.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The code iterates through the array of length $n$ once, performing an $O(1)$ logarithmic calculation for each element.** |
| Space | **O(1) — Only a few primitive integer variables are used to maintain state, requiring $O(1)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

---
### 🔀 Solution 3 — Digit Extraction / Array Iteration

> **Language:** Java  
> **Runtime:** `1 ms`  
> **Memory:** `44.7 MB`

#### 💡 Intuition

To determine whether an integer has an even digit count, we can continuously strip off its least significant digit by dividing by 10 until the number becomes zero. Counting the total number of divisions gives us the exact digit count. If this count is divisible by 2, the number has an even number of digits. By iterating over the array and applying this digit-counting helper, we can accumulate the total count of valid numbers.

#### 🧠 Algorithmic Pattern

> **Digit Extraction / Array Iteration**

#### 🚀 Approach

1. Initialize `evenCount` to `0` to keep track of how many numbers meet the even digit count condition.
2. Loop through the `nums` array from index `0` to `nums.length - 1`.
3. For each number, call the helper function `numberHasEvenDigits(nums[i])`.
4. Inside `numberHasEvenDigits`, initialize a counter `digitsCount` to `0`.
5. Execute a `while` loop while `num != 0`: perform integer division `num = num / 10` to remove the last digit and increment `digitsCount` by `1`.
6. Return `true` if `digitsCount % 2 == 0` (even), or `false` otherwise.
7. If `numberHasEvenDigits` returns `true`, increment `evenCount` by `1`.
8. After checking all numbers in the array, return `evenCount`.

#### ✅ Why This Works

In base-10 arithmetic, integer division by 10 truncates the rightmost digit of a positive integer. Repeatedly performing this division until the value reaches 0 guarantees that every digit is processed exactly once, yielding the total digit count. Applying the modulo operator `% 2` on `digitsCount` correctly evaluates parity, returning `true` for even digit counts and `false` for odd ones.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Iterating through the array of size $n$ takes $O(n)$ time, and since each number is bounded by $10^5$, counting its digits takes at most 6 operations, which is $O(1)$ work per number.** |
| Space | **O(1) — The implementation only uses a few local integer variables (`evenCount`, `digitsCount`, loop index) without allocating any additional memory structures.** |

#### 💻 Solution

[View the complete Java solution →](./solution-3.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
