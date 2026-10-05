# 🧩 136. Single Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Bit Manipulation  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/single-number/)

---

## 📝 Problem

Find the unique element in an array where all other elements appear exactly twice.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Hash Table

> **Language:** Java
> **Runtime:** `16 ms`  
> **Memory:** `47.5 MB`

#### 💡 Intuition

By storing the frequency of each element in a hash map during a first pass, we can easily identify the single number by inspecting the frequency counts in a second pass.

#### 🧠 Algorithmic Pattern

> **Hash Table**

#### 🚀 Approach

1. Initialize a hash map to store each integer alongside its occurrence count.
2. Iterate through the array and increment the frequency count for each element in the hash map.
3. Iterate through the array again (or map keys) to find the key whose associated frequency value is 1.
4. Return the integer that has a frequency count of 1.

#### ✅ Why This Works

A hash map provides average O(1) insertion and lookup operations. Counting frequencies guarantees that duplicate numbers reach a count of 2, while the single number remains at a count of 1.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We perform two linear passes over the array of size n, and each hash table insertion/lookup operates in average O(1) time, resulting in O(n) overall time complexity.** |
| Space | **O(n) — In the worst case, the hash map stores around (n/2) + 1 distinct elements, requiring O(n) extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Using a hash map is an intuitive way to keep track of frequencies, though it uses O(n) extra auxiliary space.

---

### 🧠 Solution 2 — Bit Manipulation

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `47 MB`

#### 💡 Intuition

Bitwise XOR has two key properties: a ^ a = 0 and a ^ 0 = a. Because XOR is commutative and associative, XORing all elements together causes all duplicate pairs to cancel each other out, leaving only the single unique number.

#### 🧠 Algorithmic Pattern

> **Bit Manipulation**

#### 🚀 Approach

1. Initialize an accumulator variable `res` to 0.
2. Iterate through each integer in the input array.
3. Update `res` by taking the bitwise XOR (`^`) with the current integer.
4. After processing all elements, return `res` as the single unique number.

#### ✅ Why This Works

If the array is [a, b, a, c, b], taking the cumulative XOR yields: a ^ b ^ a ^ c ^ b = (a ^ a) ^ (b ^ b) ^ c = 0 ^ 0 ^ c = c. The duplicates cancel out regardless of their order in the array.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm visits each of the n elements in the array exactly once, performing a constant-time bitwise operation at each step.** |
| Space | **O(1) — Only a single integer variable (`res`) is maintained, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Bitwise XOR allows canceling identical pairs in a single pass without needing any additional data structure, satisfying both linear time and constant space requirements.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/single-number/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
