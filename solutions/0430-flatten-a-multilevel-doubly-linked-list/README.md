# 🧩 430. Flatten a Multilevel Doubly Linked List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List · Depth-First Search · Doubly-Linked List  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/)

---

## 📝 Problem

Flatten a multilevel doubly linked list into a single-level doubly linked list where any child sublist is inserted directly after its parent node and before the parent's next sibling, clearing all child pointers.

---

## 💡 Intuition

Flattening a multilevel doubly linked list requires visiting nodes in pre-order traversal order: whenever a node has a child sublist, we must traverse the entire child list before resuming with the node's original next neighbor. An explicit stack simplifies this pre-order traversal iteratively. By pushing `curr.next` onto the stack first and `curr.child` second, the stack's Last-In, First-Out (LIFO) property ensures the child list is popped and processed immediately. As each node is popped, we stitch it to the previously processed node via `prev` and `next` pointers while clearing its `child` reference.

---

## 🧠 Algorithmic Pattern

> **Iterative Depth-First Search (DFS) with Stack**

---

## 🚀 Approach

1. Handle the edge case where `head` is `null` by returning `null` immediately.
2. Initialize a dummy node `pHead` and a pointer `prev` set to `pHead` to easily construct the flattened list without special head-linking conditions.
3. Instantiate a stack of `Node` references and push the input `head` onto it.
4. Iterate while the stack is not empty: pop the top node from the stack and store it in `curr`.
5. Link `curr` to the output list by setting `curr.prev = prev` and `prev.next = curr`.
6. If `curr.next` is not null, push it onto the stack first so that main-level siblings are stored for later processing.
7. If `curr.child` is not null, push it onto the stack second (so it is popped next) and set `curr.child = null` to clear the child pointer.
8. Advance `prev` to `curr` and repeat until the stack is empty, then break the dummy node's reverse link (`pHead.next.prev = null`) and return `pHead.next`.

---

## ✅ Why This Works

Pushing `curr.next` before `curr.child` onto a LIFO stack enforces a depth-first traversal order, ensuring the entire child sublist is inserted immediately after `curr` and before `curr.next`. Updating `prev.next` and `curr.prev` at each popped node incrementally constructs a valid, single-level doubly linked list.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Every node in the multilevel list is pushed onto and popped from the stack exactly once, spending O(1) time per node.** |
| Space | **O(n) — The stack stores unvisited nodes, which requires O(n) space in the worst case when the list has deep child nesting or sequential nodes.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `43.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Multilevel tree-like linked structures can be flattened sequentially using pre-order DFS with an explicit stack, pushing next siblings before child branches to maintain proper traversal order.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
