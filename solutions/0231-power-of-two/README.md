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

The key to this problem is recognizing the right data structure or algorithmic pattern: **Math, Bit Manipulation, Recursion**. Instead of repeatedly checking unnecessary possibilities, the solution keeps track of the information required to make each decision efficiently.

---

## 🚀 Approach

1. Identify the main algorithmic pattern.
2. Traverse the input while maintaining the required state.
3. Use the relevant technique (Math, Bit Manipulation, Recursion) to avoid unnecessary work.
4. Return the result after processing the required input.

---

## ⏱️ Complexity

The exact complexity follows from the algorithm used in the accepted
solution.

**Runtime reported by LeetCode:** `1`  
**Memory reported by LeetCode:** `42724000`

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The most important lesson is to recognize the underlying algorithmic
pattern and choose a data structure that avoids unnecessary repeated work.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/power-of-two/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
