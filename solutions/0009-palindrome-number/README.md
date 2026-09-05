# 🧩 9. Palindrome Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Math  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-number/)

---

## 📝 Problem

Given an integer
x
, return
true
 if
x
 is a
palindrome
, and
false
 otherwise.

 

Example 1:

```text

Input:
 x = 121

Output:
 true

Explanation:
 121 reads as 121 from left to right and from right to left.

```

Example 2:

```text

Input:
 x = -121

Output:
 false

Explanation:
 From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

```

Example 3:

```text

Input:
 x = 10

Output:
 false

Explanation:
 Reads 01 from right to left. Therefore it is not a palindrome.

```

 

Constraints:

-2
31
 <= x <= 2
31
 - 1

 

Follow up:
 Could you solve it without converting the integer to a string?

---

## 💡 Intuition

The solution processes the input systematically while keeping only the state necessary to make the next decision efficiently.

### 🧠 Algorithmic Pattern

| Role | Pattern |
|---|---|
| Primary | **Direct Iterative Approach** |
| Supporting | None |

---

## 🚀 Approach

1. Initialize the required state.
2. Traverse the input.
3. Apply the problem-specific condition at each step.
4. Update the result and return the final answer.

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
| Time | **Depends on the implementation** |
| Space | **Depends on the implementation** |

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

- [LeetCode Problem](https://leetcode.com/problems/palindrome-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
