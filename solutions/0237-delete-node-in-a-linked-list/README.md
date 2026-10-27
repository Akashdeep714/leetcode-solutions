# 🧩 237. Delete Node in a Linked List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/delete-node-in-a-linked-list/)

---

## 📝 Problem

Delete a given non-tail node from a singly-linked list without access to the head of the list.

---

## 💡 Intuition

Standard node deletion in a singly-linked list requires updating the `next` pointer of the preceding node to bypass the target node. Because we are given access only to the node to be deleted and not the head, accessing the previous node is impossible. Instead of attempting to delete the given node structure itself, we can copy the value from the next node (`node.next.val`) into the current node (`node.val`) and then skip the next node by updating `node.next` to `node.next.next`. Since the problem guarantees that the given node is not the tail, a valid next node always exists, making this copy-and-skip strategy completely safe.

---

## 🧠 Algorithmic Pattern

> **In-Place Value Replacement**

---

## 🚀 Approach

1. Identify the immediate successor node using `node.next`.
2. Retrieve the integer value stored in the successor node (`node.next.val`).
3. Overwrite the target node's value (`node.val`) with `node.next.val`.
4. Update `node.next` to point to `node.next.next`, removing the successor node from the linked list.

---

## ✅ Why This Works

Copying the successor node's value transforms the given node into a clone of its next node. Bypassing the successor node via `node.next = node.next.next` eliminates the duplicate, reducing the list size by one while maintaining the relative order of all other elements.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(1) — The algorithm executes a constant number of pointer and value assignments without any iteration or recursion.** |
| Space | **O(1) — The operation modifies the existing linked list in-place and uses no extra memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `44.7 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When you cannot modify references pointing to a target node in a singly-linked list, copy the next node's value into the target node and delete the next node instead.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/delete-node-in-a-linked-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
