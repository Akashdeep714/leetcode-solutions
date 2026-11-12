# 🧩 160. Intersection of Two Linked Lists

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · Linked List · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/intersection-of-two-linked-lists/)

---

## 📝 Problem

Given the heads of two singly linked lists `headA` and `headB`, return the node reference where the two lists intersect, or `null` if no intersection exists.

---

## 💡 Intuition

This brute-force approach relies on the definition of list intersection: two linked lists intersect if and only if they share a common node reference in memory. To find this node, we can test every node in list A against every node in list B. If either list is empty, or if the lists share no common nodes, the nested traversal finishes and safely concludes there is no intersection. While simple and requiring no extra space, comparing all node pairs results in quadratic comparisons relative to list lengths.

---

## 🧠 Algorithmic Pattern

> **Brute Force / Nested Loop Comparison**

---

## 🚀 Approach

1. Initialize a pointer `currA` to `headA` to begin traversing the first linked list.
2. Enter an outer loop that continues as long as `currA` is not `null`.
3. At the start of each outer loop iteration, reset pointer `currB` to `headB` to scan the second linked list from its head.
4. Enter an inner loop that continues as long as `currB` is not `null`.
5. Check for reference equality with `currA == currB`. If true, return `currA` immediately as the intersection node.
6. Advance `currB` to `currB.next` to check the next node in list B.
7. Once the inner loop completes without finding a match, advance `currA` to `currA.next`.
8. If `currA` becomes `null` without finding any match, return `null`.

---

## ✅ Why This Works

If two linked lists intersect at a specific node, that single node instance belongs to both list structures. By evaluating reference equality (`currA == currB`) across all pairs of nodes from list A and list B, the algorithm exhaustively searches the entire Cartesian product of nodes and is guaranteed to identify the first shared memory address if one exists.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m * n) — The outer loop runs up to $m$ times and the inner loop runs up to $n$ times, resulting in a worst-case time complexity of $O(m \times n)$ pointer comparisons.** |
| Space | **O(1) — The implementation only uses two pointer variables (`currA` and `currB`), allocating no additional memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1486 ms` |
| Memory | `52.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Checking linked list intersection requires matching node memory addresses rather than values; while brute-force pair checking costs $O(m \times n)$ time, it serves as a baseline before optimizing to $O(m + n)$ using two pointers or hash sets.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-linked-lists/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
