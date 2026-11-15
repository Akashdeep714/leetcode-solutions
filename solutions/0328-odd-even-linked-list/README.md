# 🧩 328. Odd Even Linked List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/odd-even-linked-list/)

---

## 📝 Problem

Reorder a singly linked list in-place so that all nodes at odd 1-based positions precede all nodes at even positions, preserving their original relative order.

---

## 💡 Intuition

Instead of allocating new nodes or copying values, we can separate the list into two sub-lists during a single traversal: one for odd-positioned nodes and one for even-positioned nodes. By initializing `odd` at the first node and `even` at the second node (keeping a reference to `evenHead`), we can step through the list and reassign pointer references. The node immediately after an even node is always the next odd node, and after appending it to the odd chain, the node following it is the next even node. Once the traversal completes, we link the tail of the odd list directly to `evenHead`.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Check if `head` is `null`; if so, return `null` immediately.
2. Initialize `odd` to `head`, and both `even` and `evenHead` to `head.next`.
3. Traverse the list using a `while` loop that continues as long as `even` and `even.next` are both non-null.
4. Inside the loop, assign `odd.next = even.next` to link the current odd node to the next odd node in the list.
5. Advance `odd` forward to `odd.next`.
6. Assign `even.next = odd.next` to link the current even node to the next even node in the list.
7. Advance `even` forward to `even.next`.
8. After the loop finishes, set `odd.next = evenHead` to attach the start of the even sub-list to the end of the odd sub-list, and return `head`.

---

## ✅ Why This Works

The algorithm maintains two loop invariants: `odd` always points to the tail of the processed odd-indexed list, and `even` points to the tail of the processed even-indexed list. Because `even.next` points to the next odd node in sequence, updating `odd.next = even.next` correctly isolates and appends that node to the odd list while maintaining order. Immediately after advancing `odd`, its `next` reference points to the next even node, so `even.next = odd.next` accurately appends the next even node to the even list. When the end of the list is reached, attaching `evenHead` to `odd.next` cleanly joins the two ordered partitions in $O(1)$ auxiliary space.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The while loop advances two nodes per iteration, traversing each node of the $n$-node list exactly once.** |
| Space | **O(1) — The algorithm reorders the nodes in-place using only a constant number of pointer variables (`odd`, `even`, `evenHead`).** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `45.8 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Linked list partition and reordering problems can be solved in-place by maintaining separate tail pointers for each sub-list during traversal and stitching the sub-lists together at the end.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/odd-even-linked-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
