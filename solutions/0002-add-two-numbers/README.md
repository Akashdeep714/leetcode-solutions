# 🧩 2. Add Two Numbers

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List · Math · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/add-two-numbers/)

---

## 📝 Problem

Add two non-negative integers represented as linked lists with digits stored in reverse order, and return the sum as a new reversed linked list.

---

## 💡 Intuition

Because the digits are stored in reverse order, the head of each list represents the least significant digit (the ones place). This setup aligns directly with standard right-to-left schoolbook addition. By traversing both lists simultaneously, we can sum corresponding digits alongside a carry variable that tracks overflow from the previous column. A dummy head node simplifies constructing the result list, eliminating edge cases for head node creation.

---

## 🧠 Algorithmic Pattern

> **Linked List Traversal / Elementary Math**

---

## 🚀 Approach

1. Initialize a dummy head node `dHead` with value 0, set pointer `curr = dHead`, and set `carry = 0`.
2. Loop as long as `l1 != null`, `l2 != null`, or `carry != 0`.
3. Extract digit `a` from `l1` (or 0 if `l1` is null) and digit `b` from `l2` (or 0 if `l2` is null).
4. Calculate `sum = carry + a + b`, update `carry` to `sum / 10`, and create a new `ListNode` with digit `sum % 10` linked to `curr.next`.
5. Move `curr` to `curr.next`, and advance `l1` and `l2` to their next nodes if they are not null.
6. Return `dHead.next`, which points to the first actual digit node of the calculated sum list.

---

## ✅ Why This Works

Positional addition processes digits from right to left, adding corresponding place values and carrying over any amount $\ge 10$. Since the linked lists store digits in reverse order, iterating through the lists left to right naturally processes least significant to most significant digits. Including `carry != 0` in the loop condition ensures that an extra digit node is appended when the final addition produces an extra place value (e.g., $99 + 1 = 100$).

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(max(m, n)) — The loop executes at most $\max(m, n) + 1$ times, where $m$ and $n$ are the lengths of the two linked lists, performing $O(1)$ operations per node.** |
| Space | **O(max(m, n)) — The algorithm constructs a new linked list containing at most $\max(m, n) + 1$ nodes to store the sum result.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `46.4 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a dummy sentinel head node simplifies linked list construction by avoiding conditional logic for the initial head node, while a carry variable manages place-value overflow across lists of equal or unequal lengths.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/add-two-numbers/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
