# 🧩 142. Linked List Cycle II

> **Difficulty:** 🟡 Medium  
> **Topics:** Hash Table · Linked List · Two Pointers · Floyd's Cycle Finding Algorithm  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/linked-list-cycle-ii/)

---

## 📝 Problem

Given the head of a singly-linked list, find and return the node where a cycle begins, or return null if the list contains no cycle.

---

## 💡 Intuition

In a acyclic linked list, every node is visited at most once during traversal before reaching null. However, if a cycle exists, traversing the list will loop infinitely, revisiting nodes in the cycle. The key observation is that the very first node encountered a second time during traversal is the exact node where the cycle begins. By recording visited node memory addresses in a hash set, we can immediately detect when a node is revisited.

---

## 🧠 Algorithmic Pattern

> **Hash Table**

---

## 🚀 Approach

1. Initialize an empty hash set named set to store references to visited ListNode objects.
2. Set a pointer curr to head to begin traversing the list.
3. Execute a while loop that continues as long as curr is not null.
4. At each step, check if curr is already in set using set.contains(curr).
5. If set.contains(curr) is true, return curr immediately, as it is the first node revisited and thus the start of the cycle.
6. If curr is not in set, add it to set using set.add(curr).
7. Advance curr to curr.next to inspect the next node.
8. If the loop terminates because curr becomes null, return null indicating no cycle exists.

---

## ✅ Why This Works

Nodes before the cycle entry point are visited exactly once as the traversal moves linearly from the head. Once traversal enters the cycle, it traverses around the loop and returns to the entry point. Since all nodes traversed so far—including the cycle entry point itself—were added to the set on their first visit, the cycle entry node is guaranteed to be the first node already present in the set upon a second visit.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We visit each node at most twice (or once if there is no cycle), performing O(1) average-time hash set lookups and insertions per node.** |
| Space | **O(n) — The hash set stores at most n unique node references, where n is the total number of nodes in the linked list.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `6 ms` |
| Memory | `46.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a hash set to track visited node references provides a clean O(n) time solution for cycle entry detection, though Floyd's Cycle-Finding Algorithm can achieve O(1) auxiliary space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/linked-list-cycle-ii/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
