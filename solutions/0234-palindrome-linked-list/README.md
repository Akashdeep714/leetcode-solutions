# 🧩 234. Palindrome Linked List

> **Difficulty:** 🟢 Easy  
> **Topics:** Linked List · Two Pointers · Stack · Recursion  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/palindrome-linked-list/)

---

## 📝 Problem

Determine whether the values in a given singly linked list read the same forward and backward.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Two Pointers

> **Language:** Java
> **Runtime:** `8 ms`  
> **Memory:** `99.2 MB`

#### 💡 Intuition

Because a singly linked list only allows forward traversal, checking for symmetry directly on the nodes is tricky. By copying all node values into an `ArrayList`, we gain $O(1)$ random index access. This transforms the problem into a standard array palindrome check, where two pointers starting at opposite ends move inward and compare corresponding elements.

#### 🧠 Algorithmic Pattern

> **Two Pointers**

#### 🚀 Approach

1. Initialize an empty `ArrayList` of integers named `list` to hold node values.
2. Traverse the singly linked list starting from `head`, appending each node's value `curr.val` to `list` until `curr` becomes `null`.
3. Initialize two index pointers: `i = 0` at the beginning of `list` and `j = list.size() - 1` at the end.
4. Loop while `i < j`, comparing `list.get(i)` with `list.get(j)` at each step.
5. If `list.get(i)` is not equal to `list.get(j)`, return `false` immediately.
6. Increment `i` and decrement `j` to move toward the center of the list.
7. If the loop finishes without finding any mismatch, return `true`.

#### ✅ Why This Works

A sequence of length $N$ is a palindrome if and only if the element at index $i$ equals the element at index $N - 1 - i$ for all $0 \le i < N / 2$. Transferring the linked list elements into an array preserves their order, and the two-pointer loop systematically checks this precise equality condition from the boundaries inward.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm visits each of the $n$ nodes once to copy values into the array list, followed by at most $n/2$ iterations in the two-pointer loop, running in $O(n)$ overall time.** |
| Space | **O(n) — An auxiliary `ArrayList` stores all $n$ node values, resulting in $O(n)$ extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

When singly linked list traversal limits bidirectional access, copying elements into an array enables $O(1)$ random access for standard two-pointer techniques at the cost of $O(n)$ space.

---

### 🧠 Solution 2 — Fast and Slow Pointers / Linked List Reversal

> **Language:** Java
> **Runtime:** `4 ms`  
> **Memory:** `93.8 MB`

#### 💡 Intuition

To check for palindrome symmetry without additional memory, we can find the middle of the list, reverse the second half in place, and iterate simultaneously from the start of the list and the head of the reversed second half.

#### 🧠 Algorithmic Pattern

> **Fast and Slow Pointers / Linked List Reversal**

#### 🚀 Approach

1. Use fast and slow pointers to locate the middle node (slow advances by 1, fast advances by 2).
2. Reverse the second half of the linked list starting from the slow pointer in place.
3. Set one pointer at the original head and another at the start of the reversed second half.
4. Iterate both pointers forward, comparing node values. Return false on any mismatch.
5. If the second half pointer reaches the end with all values matching, return true.

#### ✅ Why This Works

Reversing the second half allows forward iteration from both ends toward the middle, eliminating the need for backward traversal or external data structures.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Finding the middle takes n/2 steps, reversing the second half takes n/2 steps, and comparing the two halves takes n/2 steps. The total operation count is linear, O(n).** |
| Space | **O(1) — All operations are performed in place by modifying link references, requiring only O(1) auxiliary variables.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Combining the fast and slow pointer midpoint search with in-place list reversal solves the palindrome check in optimal O(1) auxiliary space.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/palindrome-linked-list/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
