# 🧩 202. Happy Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · Math · Two Pointers · Floyd's Cycle Finding Algorithm  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/happy-number/)

---

## 📝 Problem

Determine if repeatedly replacing a positive integer with the sum of the squares of its digits eventually reaches 1 or falls into an infinite repeating loop.

---

## 💡 Intuition

When repeatedly calculating the sum of squares of digits, large numbers rapidly shrink (for example, the largest 32-bit integer produces a sum well under 250 in one step). Because the set of possible numbers in the sequence is small and bounded, the process will either reach 1 or cycle endlessly through previously visited numbers. Using a hash set to store each intermediate number allows us to detect when we have entered a loop.

---

## 🧠 Algorithmic Pattern

> **Hash Table / Cycle Detection**

---

## 🚀 Approach

1. Define a helper function sumOfSquaresOfDigits(n) that extracts each digit using n % 10, squares it, adds it to a total sum, and reduces n using integer division n / 10 until n is 0.
2. Initialize a HashSet of integers named set to track numbers encountered in the chain.
3. Execute a while loop that runs as long as n is not equal to 1.
4. Inside the loop, check if set already contains n; if it does, a cycle is detected, so return false.
5. Add the current value of n to set to mark it as visited.
6. Update n to sumOfSquaresOfDigits(n).
7. If the loop terminates because n becomes 1, return true.

---

## ✅ Why This Works

The process is a deterministic state transition where each number maps to exactly one next number. Since the values quickly drop below 243 for any 32-bit integer, there are only finitely many distinct values the sequence can take. By Dirichlet's box principle (pigeonhole principle), the chain must either hit 1 (and stay there) or repeat a value. The hash set acts as a memory of visited states; returning false as soon as a duplicate number appears correctly identifies non-terminating infinite loops.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n) — Computing the sum of squared digits takes O(log n) time based on the number of digits, and for values under 243, the chain length is bounded by a small constant.** |
| Space | **O(log n) — The hash set stores at most O(log n) distinct numbers generated during the sequence before reaching 1 or entering a loop.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `41.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When repeatedly applying a deterministic function generates a sequence of bounded values, a Hash Set can effectively detect infinite loops by identifying duplicate states.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/happy-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
