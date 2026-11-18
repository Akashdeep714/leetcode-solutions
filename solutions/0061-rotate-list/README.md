# 🧩 61. Rotate List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/rotate-list/)

---

## 📝 Problem

Given the head of a singly-linked list and an integer k, rotate the list to the right by k positions and return the new head.

---

## 💡 Intuition

Rotating a linked list of length N to the right by k places is equivalent to shifting the entire list modulo N, because rotating by N full places results in the exact same list. Thus, we only need to shift right by k % size places. The last (k % size) nodes of the list will become the new head section, while the preceding node becomes the new tail. By first measuring the total length and identifying the original tail node, we can locate the exact split index at size - (k % size), break the list connection there, and attach the original tail to the original head.

---

## 🧠 Algorithmic Pattern

> **Linked List Traversal & Modulo Arithmetic**

---

## 🚀 Approach

1. Handle base cases: if k == 0, head is null, or the list has only one node (head.next == null), return head immediately.
2. Traverse the linked list with a pointer curr to calculate its total length (size) and keep track of the last node (tail).
3. Compute the effective number of rotations using newK = k % size. If newK == 0, return head as no rotation changes the list.
4. Calculate diff = size - newK to find the 1-based index of the node that will become the new tail.
5. Traverse from head up to index diff - 1 using a loop to locate the new tail node (curr).
6. Set newHead = curr.next, disconnect the list by setting curr.next = null, and reconnect the list by setting tail.next = head.
7. Return newHead as the head of the rotated linked list.

---

## ✅ Why This Works

Rotating a list to the right by k positions moves the last k % size nodes to the front of the list while maintaining internal node order. The node at position size - (k % size) becomes the last element of the new list. By severing its next pointer to end the list and pointing the original tail node to the original head node, the algorithm seamlessly reorders the two list segments into the correctly rotated sequence in place.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The code makes at most two linear passes through the linked list—one to compute the size and tail, and another to reach the split node.** |
| Space | **O(1) — Only a few pointer references (curr, tail, newHead) and integer variables are used, requiring standard O(1) auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `43.9 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When performing cyclical shifts on linear structures, using modulo arithmetic k % N eliminates unnecessary full rotations and reveals the exact split point for pointer manipulation.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/rotate-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
