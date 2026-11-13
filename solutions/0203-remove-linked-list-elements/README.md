# 🧩 203. Remove Linked List Elements

> **Difficulty:** 🟢 Easy  
> **Topics:** Linked List · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/remove-linked-list-elements/)

---

## 📝 Problem

Remove all nodes from a singly-linked list whose values match a given integer target `val`, and return the head of the updated list.

---

## 💡 Intuition

Deleting a node in a singly-linked list requires re-linking its predecessor node's `next` pointer to skip the target node. However, if the head of the list itself needs to be removed, it has no predecessor, creating special edge cases. Introducing a dummy head node (`pHead`) before the actual head standardizes the deletion logic: every node, including the original head, now has a non-null preceding node (`prev`), allowing us to cleanly bypass target nodes without extra conditional checks for the start of the list.

---

## 🧠 Algorithmic Pattern

> **Dummy Head Pointer**

---

## 🚀 Approach

1. Instantiate a dummy node `pHead` with value `0` and set `pHead.next = head`.
2. Initialize pointer `prev` to point to `pHead` and pointer `curr` to point to `head`.
3. Traverse the linked list using a `while` loop until `curr` becomes `null`.
4. If `curr.val == val`, remove `curr` by setting `prev.next = curr.next` without advancing `prev` (since the new `prev.next` might also contain `val`).
5. If `curr.val != val`, move `prev` forward to `curr`.
6. Advance `curr` to `curr.next` in every iteration to evaluate the next node.
7. Return `pHead.next`, which points to the updated head of the list.

---

## ✅ Why This Works

The dummy head guarantees that `prev` always references a valid node whose value is confirmed not to equal `val`. When a target node is identified (`curr.val == val`), setting `prev.next = curr.next` effectively unlinks `curr` from the list structure. Keeping `prev` stationary during a deletion ensures that if consecutive nodes contain `val`, they are all continuously bypassed until a non-matching node is reached.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The solution visits each of the n nodes in the linked list exactly once in a single pass.** |
| Space | **O(1) — The algorithm operates in-place, using only a single dummy node and two pointer references regardless of input size.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `46.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a dummy (sentinel) head node simplifies linked list modifications by ensuring every node has a valid predecessor, eliminating special edge cases for head updates.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/remove-linked-list-elements/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
