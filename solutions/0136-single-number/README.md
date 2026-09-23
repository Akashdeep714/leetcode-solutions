# 🧩 136. Single Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Bit Manipulation  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/single-number/)

---

## 📝 Problem

Find the unique element in an integer array where every other element appears exactly twice, using linear runtime and constant extra space.

---

## 💡 Intuition

The bitwise XOR operation has two key algebraic properties that make it ideal for pair cancellation: any number XORed with itself equals zero ($a \oplus a = 0$), and any number XORed with zero equals itself ($a \oplus 0 = a$). Because XOR is both commutative and associative, elements can be reordered without changing the final result. If we accumulate the XOR sum across every number in the array, all duplicate pairs will cancel each other out to zero, leaving only the single unique integer.

---

## 🧠 Algorithmic Pattern

> **Bit Manipulation**

---

## 🚀 Approach

1. Initialize an integer variable `res` to `0` to serve as the cumulative XOR accumulator.
2. Iterate through each element `num` in the input array `nums` using a for-each loop.
3. Perform a bitwise XOR operation between `res` and `num` (`res = res ^ num`) and store the result back in `res`.
4. After visiting every element in the array, return `res` as the unique single number.

---

## ✅ Why This Works

Bitwise XOR is commutative and associative, meaning $a \oplus b \oplus c = a \oplus c \oplus b$. This allows us to conceptually regroup the entire array's XOR sum so that identical pairs are adjacent: $(x_1 \oplus x_1) \oplus (x_2 \oplus x_2) \oplus \dots \oplus \text{single}$. Since $x \oplus x = 0$ for any integer $x$, all duplicate pairs evaluate to $0$. The overall expression reduces to $0 \oplus 0 \oplus \dots \oplus 0 \oplus \text{single} = \text{single}$, which guarantees that `res` holds the exact value of the single element at the end of the loop.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `47 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Accumulating elements with bitwise XOR isolates a single un-paired element in $O(n)$ time and $O(1)$ space because identical values cancel each other out ($a \oplus a = 0$).

---

---
### 🔀 Solution 2 — Hash Table / Frequency Counting

> **Language:** Java  
> **Runtime:** `16 ms`  
> **Memory:** `47.5 MB`

#### 💡 Intuition

To identify the element that appears only once, we can count how many times each number occurs throughout the array. By using a hash map, we can record each number alongside its frequency during an initial pass. A second pass over the array allows us to query the hash map and immediately locate the single integer whose frequency is 1.

#### 🧠 Algorithmic Pattern

> **Hash Table / Frequency Counting**

#### 🚀 Approach

1. Initialize a hash map named `map` to map each integer to its frequency count.
2. Iterate through each element `num` in the input array `nums`.
3. Check if `num` is present in `map`; if absent, initialize its count to 0 in `map`.
4. Update the frequency of `num` in `map` by setting it to `map.get(num) + 1`.
5. Iterate through the `nums` array a second time to inspect each element's frequency.
6. Check `map.get(num)` for each element and return `num` as soon as an element with a frequency of 1 is encountered.
7. Return `-1` at the end as a default fallback if no single number is found.

#### ✅ Why This Works

The algorithm works because populating the hash map records the exact frequency of every integer in the array. Since every number except one appears twice, elements with duplicate occurrences will have a hash map value of 2, while the unique element will have a value of 1. Checking `map.get(num) == 1` during the second iteration reliably isolates and returns the unique integer.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm completes two linear passes over an array of size n, performing average O(1) hash map operations per element, resulting in an average time complexity of O(n).** |
| Space | **O(n) — The hash map stores entries for all unique numbers in the array, using O(n) auxiliary space to hold (n + 1) / 2 distinct keys.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/single-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
