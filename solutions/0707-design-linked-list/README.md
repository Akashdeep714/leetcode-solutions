# 🧩 707. Design Linked List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List · Design  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/design-linked-list/)

---

## 📝 Problem

Design a 0-indexed singly linked list supporting value retrieval by index, insertion at the head, tail, or specific index, and deletion at a specific index.

---

## 💡 Intuition

Inserting and deleting nodes in a singly linked list usually requires handling head updates as special edge cases. By introducing a dummy head node (a sentinel node positioned before index 0) and maintaining an explicit list size counter, every real element—including the very first node—always has a predecessor. This unifies pointer manipulation logic across all operations and makes boundary validation straightforward.

---

## 🧠 Algorithmic Pattern

> **Singly Linked List with Dummy Head**

---

## 🚀 Approach

1. Initialize the data structure with a dummy head node (`ListNode(0)`) and set `size` to 0.
2. For `get(index)`, check if `index` is within `[0, size - 1]`. Starting from `head`, traverse `index + 1` steps forward to arrive at the target node and return its `val`.
3. For `addAtIndex(index, val)`, validate that `index` is within `[0, size]`. Advance a `curr` pointer from `head` for `index` steps to land on the node immediately preceding the target insertion position.
4. Increment `size`, create a `newNode` with value `val`, and splice it in by setting `newNode.next = curr.next` and `curr.next = newNode`.
5. Delegate `addAtHead(val)` and `addAtTail(val)` directly to `addAtIndex(0, val)` and `addAtIndex(size, val)`, respectively.
6. For `deleteAtIndex(index)`, validate that `index` is within `[0, size - 1]`. Advance `curr` from `head` for `index` steps to locate the predecessor node, decrement `size`, and bypass the target node using `curr.next = curr.next.next`.

---

## ✅ Why This Works

The dummy head acts as a fixed anchor at index -1. Because every valid list node (from index 0 to `size - 1`) has a guaranteed predecessor node reachable by making `index` steps from `head`, insertions and deletions never encounter `null` predecessor pointers. Explicitly tracking `size` allows immediate detection of out-of-bounds indices before starting pointer traversals.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Each lookup, insertion, or deletion operation takes up to O(n) time to traverse to the target index in the worst case, where n is the current number of elements in the list.** |
| Space | **O(n) — The list stores n element nodes in memory across all insert operations, using O(1) auxiliary space per method call.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `10 ms` |
| Memory | `46.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a dummy head node simplifies singly linked list operations by guaranteeing that every element, including the head, has a non-null preceding node.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/design-linked-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
