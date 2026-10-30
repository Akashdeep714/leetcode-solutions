# 🧩 206. Reverse Linked List

> **Difficulty:** 🟢 Easy  
> **Topics:** Linked List · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/reverse-linked-list/)

---

## 📝 Problem

Given the head of a singly linked list, reverse the direction of all pointers and return the new head of the reversed list.

---

## 💡 Intuition

To reverse a singly linked list, each node's next reference must be redirected to point to the node before it rather than the node after it. However, overwriting a node's next pointer immediately severs the link to the rest of the list. To overcome this, we temporarily back up the next node before modifying the link. By keeping a pointer to the previous node (initialized to null) and a pointer to the current node (initialized to head), we can step through the list node by node, reversing one reference at a time until reaching the end.

---

## 🧠 Algorithmic Pattern

> **Two Pointers / In-Place Linked List Traversal**

---

## 🚀 Approach

1. Initialize `curr` to point to `head` and `prev` to `null`.
2. Begin a loop that continues as long as `curr` is not `null`.
3. Store `curr.next` in a temporary variable `next` so the remaining chain is not lost.
4. Reassign `curr.next = prev` to reverse the current node's pointer direction.
5. Advance `prev` to `curr`, making `curr` the tail of the newly updated reversed portion.
6. Advance `curr` to `next` to move on to the next node in the original list.
7. Return `prev` after the loop terminates, which points to the head of the fully reversed list.

---

## ✅ Why This Works

The algorithm maintains a loop invariant where all nodes processed before `curr` form a correctly reversed linked list rooted at `prev`, while nodes starting from `curr` retain their original structure. In each iteration, reassigning `curr.next = prev` attaches `curr` to the front of the reversed portion without losing the unvisited sublist because `next` preserves the remaining path. When `curr` becomes `null`, every link in the original list has been reversed, and `prev` holds the reference to the original tail node, which is now the head of the reversed list.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm visits each of the n nodes in the linked list exactly once, performing constant-time pointer operations at each step.** |
| Space | **O(1) — The list is reversed in place using only three pointer variables (`curr`, `prev`, and `next`), requiring constant extra space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `43.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When modifying pointers in a singly linked list, always store the reference to the next node before overwriting `curr.next` to avoid losing access to the rest of the list.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/reverse-linked-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
