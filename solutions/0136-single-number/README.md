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

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/single-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
