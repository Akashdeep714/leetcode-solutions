# 🧩 234. Palindrome Linked List

> **Difficulty:** 🟢 Easy  
> **Topics:** Linked List · Two Pointers · Stack · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-linked-list/)

---

## 📝 Problem

Determine whether the values in a given singly linked list read the same forward and backward.

---

## 💡 Intuition

Because a singly linked list only allows forward traversal, checking for symmetry directly on the nodes is tricky. By copying all node values into an `ArrayList`, we gain $O(1)$ random index access. This transforms the problem into a standard array palindrome check, where two pointers starting at opposite ends move inward and compare corresponding elements.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize an empty `ArrayList` of integers named `list` to hold node values.
2. Traverse the singly linked list starting from `head`, appending each node's value `curr.val` to `list` until `curr` becomes `null`.
3. Initialize two index pointers: `i = 0` at the beginning of `list` and `j = list.size() - 1` at the end.
4. Loop while `i < j`, comparing `list.get(i)` with `list.get(j)` at each step.
5. If `list.get(i)` is not equal to `list.get(j)`, return `false` immediately.
6. Increment `i` and decrement `j` to move toward the center of the list.
7. If the loop finishes without finding any mismatch, return `true`.

---

## ✅ Why This Works

A sequence of length $N$ is a palindrome if and only if the element at index $i$ equals the element at index $N - 1 - i$ for all $0 \le i < N / 2$. Transferring the linked list elements into an array preserves their order, and the two-pointer loop systematically checks this precise equality condition from the boundaries inward.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm visits each of the $n$ nodes once to copy values into the array list, followed by at most $n/2$ iterations in the two-pointer loop, running in $O(n)$ overall time.** |
| Space | **O(n) — An auxiliary `ArrayList` stores all $n$ node values, resulting in $O(n)$ extra space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `8 ms` |
| Memory | `99.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When singly linked list traversal limits bidirectional access, copying elements into an array enables $O(1)$ random access for standard two-pointer techniques at the cost of $O(n)$ space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-linked-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
