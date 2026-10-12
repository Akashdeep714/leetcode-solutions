# 🧩 1295. Find Numbers with Even Number of Digits

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Math  
> **Solutions:** 4 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/)

---

## 📝 Problem

Count how many numbers in an integer array contain an even number of digits.

---

## 🛠️ Solutions

This folder contains **4 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🔀 Solution 1 — Digit Extraction / Array Iteration

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
---

### 🧠 Solution 2 — Type Conversion / String Inspection

> **Language:** Java
> **Runtime:** `2 ms`  
> **Memory:** `45.7 MB`

#### 💡 Intuition

An integer's number of digits directly corresponds to the length of its string representation. Converting each number to a string allows us to query `.length()` directly.

#### 🧠 Algorithmic Pattern

> **Type Conversion / String Inspection**

#### 🚀 Approach

1. Iterate through each number in `nums`.
2. Convert the number to a string using `String.valueOf(num)`.
3. Check if `string.length()` is even.
4. Increment the answer count if it is even, and return the total count at the end.

#### ✅ Why This Works

The string representation contains one character for each digit in the base-10 number, so string length directly equals the digit count.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N * K) — Converting a number with K digits to a string takes O(K) time. Across N numbers, total time is O(N * K).** |
| Space | **O(K) — Each integer creates a temporary string of length K (at most 6 characters), requiring O(K) temporary space per iteration.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Converting numbers to strings provides concise code, but incurs small memory allocations for temporary string objects.

---

### 🔀 Solution 3 — Math / Logarithmic Digit Counting

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
---

### 🧠 Solution 4 — Direct Range Checking / Boundary Comparison

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `44.6 MB`

#### 💡 Intuition

Given the problem constraint $1 \le nums[i] \le 10^5$, the only possible ranges with even numbers of digits are 2-digit numbers [10, 99], 4-digit numbers [1000, 9999], and the 6-digit number 100000. Checking range boundaries directly avoids string operations, loops, or floating-point calculations.

#### 🧠 Algorithmic Pattern

> **Direct Range Checking / Boundary Comparison**

#### 🚀 Approach

1. Iterate through each element in `nums`.
2. Check if the element lies within `[10, 99]`, `[1000, 9999]`, or equals `100000`.
3. If any condition is satisfied, increment the count.
4. Return the total count after processing all elements.

#### ✅ Why This Works

Every integer within the bounded ranges specified explicitly contains an even count of decimal digits (2, 4, or 6 digits), covering all possible even-digit numbers under the given constraints.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — For each of the N numbers, a few simple integer comparisons are performed in O(1) time.** |
| Space | **O(1) — No extra storage is used beyond a few integer loop counters.** |

#### 💻 Solution

[View the complete Java solution →](./solution-4.java)

#### 🎯 Key Takeaway

Leveraging problem constraints allows converting digit-counting logic into direct, low-overhead range comparisons.


---

## 🎯 Key Takeaway

This repository currently contains 4 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
