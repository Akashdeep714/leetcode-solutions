# 🧩 67. Add Binary

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · String · Bit Manipulation · Simulation  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/add-binary/)

---

## 📝 Problem

Add two binary strings and return their sum as a binary string.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Simulation / Two Pointers

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `43.3 MB`

#### 💡 Intuition

Binary addition can be performed column by column from right to left (least significant bit to most significant bit), carrying over overflow bits just like standard elementary school decimal addition.

#### 🧠 Algorithmic Pattern

> **Simulation / Two Pointers**

#### 🚀 Approach

1. Swap strings if necessary so that string 'a' is guaranteed to be at least as long as string 'b'.
2. Iterate backwards from the rightmost index of 'a' and 'b', maintaining a carry variable initialized to 0.
3. At each index, sum the carry and the current binary digits from 'a' and 'b' (if within bounds of 'b').
4. Append the sum modulo 2 (sum % 2) to a StringBuilder, and update carry to sum divided by 2 (sum / 2).
5. If a carry remains after traversing all characters, append 1 to the StringBuilder.
6. Reverse the StringBuilder and return the result as a string.

#### ✅ Why This Works

Adding two single bits along with a carry yields a sum between 0 and 3. The least significant bit of this total (sum % 2) represents the bit at the current position, while the most significant bit (sum / 2) becomes the carry for the next position.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(max(N, M)) — Traversing the input strings from right to left takes O(max(N, M)) time, where N and M are the lengths of strings 'a' and 'b'. Reversing the result StringBuilder also takes O(max(N, M)) time.** |
| Space | **O(max(N, M)) — The extra memory is used by the StringBuilder to construct the result string, requiring space proportional to the maximum input string length plus at most one extra bit for a final carry.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Digit-by-digit string traversal avoids integer overflow limits, allowing arbitrary length binary string addition in linear time.

---

### 🧠 Solution 2 — Bit Manipulation / Arbitrary Precision Arithmetic

> **Language:** Java
> **Runtime:** `7 ms`  
> **Memory:** `44.8 MB`

#### 💡 Intuition

Addition without arithmetic operators can be achieved using bitwise XOR to compute sums without carry, and bitwise AND shifted left by one to compute carries, repeating until no carry remains.

#### 🧠 Algorithmic Pattern

> **Bit Manipulation / Arbitrary Precision Arithmetic**

#### 🚀 Approach

1. Parse input binary strings into Java BigInteger objects using radix 2.
2. Iterate in a loop while the second BigInteger (representing current carries) is non-zero.
3. In each step, compute bitwise XOR between the two BigIntegers to get the sum without carry.
4. Compute bitwise AND between the two BigIntegers and shift left by 1 to compute the propagated carry.
5. Update the first BigInteger to the XOR sum and the second BigInteger to the shifted carry.
6. Once the carry becomes zero, format the final BigInteger back to a base-2 binary string.

#### ✅ Why This Works

Bitwise XOR produces 1 when exactly one input bit is 1 (half-adder sum), while bitwise AND produces 1 only when both input bits are 1 (half-adder carry). Shifting the carry left by 1 moves carry bits into their correct target column for the next addition iteration.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(max(N, M)^2) — Parsing strings to BigInteger takes O(max(N, M)) time. The bitwise addition loop executes at most O(max(N, M)) times (bounded by the longest continuous carry sequence), and each BigInteger bitwise operation on max(N, M) bits takes linear time, leading to O(max(N, M)^2) worst-case time complexity.** |
| Space | **O(max(N, M)) — BigInteger instances allocate dynamic arrays proportional to the number of bits required to store numbers up to max(N, M) bits in length.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Full adder logic can be generalized to multi-bit numbers using bitwise XOR and left-shifted bitwise AND.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/add-binary/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
