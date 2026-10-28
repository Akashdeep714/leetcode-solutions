# 🧩 19. Remove Nth Node From End of List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

---

## 📝 Problem

Remove the n-th node from the end of a singly linked list and return the head of the modified list.

---

## 💡 Intuition

The n-th node from the end is at a distance of len - n steps from the start of the list. Since a singly linked list can only be traversed forward, we can first make a full pass to count the total length of the list. In a second pass, we navigate to the node immediately before the target node to bypass it. Creating a dummy node pointing to the head simplifies edge cases—specifically when the node to be removed is the head itself (when len == n)—because the dummy node acts as a permanent predecessor.

---

## 🧠 Algorithmic Pattern

> **Two-pass Linked List Traversal**

---

## 🚀 Approach

1. Initialize a counter len = 0 and a pointer cur = head.
2. Traverse the linked list using cur, incrementing len until cur becomes null to compute the total node count.
3. Instantiate a dummy node with value 0 and set dummy.next = head to handle head deletions cleanly.
4. Compute jumps = len - n, which represents the number of forward steps required from dummy to reach the node preceding the target.
5. Initialize prev = dummy and advance prev forward jumps times using a loop.
6. Unlink the target node by reassigning prev.next = prev.next.next.
7. Return dummy.next, which holds the head of the updated list.

---

## ✅ Why This Works

In a list of total length `len`, the n-th node from the end is located at 0-based index `len - n` relative to the head. Starting from a dummy node positioned before the head, advancing `len - n` steps stops exactly at the predecessor node (index `len - n - 1` relative to head). Modifying `prev.next` to point to `prev.next.next` effectively unlinks the target node without altering any other links in the list.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — The list is traversed twice—once to measure its total length N and once to reach the removal point—taking O(N) linear time overall.** |
| Space | **O(1) — The implementation only allocates a single dummy node and a few pointer variables, requiring O(1) auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `43 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a dummy node placed before the head simplifies linked list node deletions by ensuring every node, including the original head, has a valid predecessor to update.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
