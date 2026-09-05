# 🧩 231. Power of Two

> **Difficulty:** 🟢 Easy  
> **Topics:** Math · Bit Manipulation · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/power-of-two/)

---

## 📝 Problem

Given an integer
n
, return
true
 if it is a power of two. Otherwise, return
false
.

An integer
n
 is a power of two, if there exists an integer
x
 such that
n == 2
x
.

 

Example 1:

```text

Input:
 n = 1

Output:
 true

Explanation:
2
0
 = 1

```

Example 2:

```text

Input:
 n = 16

Output:
 true

Explanation:
2
4
 = 16

```

Example 3:

```text

Input:
 n = 3

Output:
 false

```

 

Constraints:

-2
31
 <= n <= 2
31
 - 1

 

Follow up:
 Could you solve it without loops/recursion?

---

## 💡 Intuition

The solution uses properties of binary representation and bitwise operations to express the required condition efficiently.

### 🧠 Algorithmic Pattern

| Role | Pattern |
|---|---|
| Primary | **Bit Manipulation** |
| Supporting | None |

---

## 🚀 Approach

1. Identify the relevant property of the binary representation.
2. Apply the required bitwise operation.
3. Repeat while relevant bits remain to be processed.
4. Return the resulting value or condition.

---

## 🔍 Why This Works

The approach avoids unnecessary repeated work by maintaining the
right state or data structure while processing the input.

The key advantage comes from choosing an algorithmic pattern that
reduces the amount of work required at each step.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(1) to O(log n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `Previously recorded` |
| Memory | `Previously recorded` |

> The Big-O complexity is inferred from the detected algorithmic
> pattern and is intended as a high-level guide.

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The most valuable part of this problem is recognizing the underlying
pattern and understanding why it reduces unnecessary computation.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
