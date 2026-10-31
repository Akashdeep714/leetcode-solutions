# 🧩 21. Merge Two Sorted Lists

> **Difficulty:** 🟢 Easy  
> **Topics:** Linked List · Recursion  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/merge-two-sorted-lists/)

---

## 📝 Problem

Merge two sorted singly-linked lists into a single sorted list by splicing together existing nodes, returning the head of the merged list.

---

## 💡 Intuition

Because both lists are already sorted, the smallest remaining element overall must always be at the front of either `list1` or `list2`. By comparing the head values of both lists step by step, we can repeatedly pick the smaller node and append it to our merged list. Using a dummy head node eliminates edge-case logic for initializing the result list's head node. Once one list runs out of nodes, we can directly link the rest of the other list since its remaining elements are already sorted and larger than all merged elements.

---

## 🧠 Algorithmic Pattern

> **Two Pointers / Dummy Head**

---

## 🚀 Approach

1. Instantiate a `dummy` sentinel `ListNode` with a value of `0` and initialize a tail pointer `curr` referencing `dummy`.
2. Enter a `while` loop that continues as long as both `list1` and `list2` are not `null`.
3. If `list1.val < list2.val`, set `curr.next` to `list1`, move `curr` to `list1`, and advance `list1` to `list1.next`.
4. Otherwise, set `curr.next` to `list2`, move `curr` to `list2`, and advance `list2` to `list2.next`.
5. After the loop exits, check if `list1` is `null`; if so, attach the remainder of `list2` to `curr.next`, otherwise attach `list1`.
6. Return `dummy.next`, which points to the true head of the merged sorted list.

---

## ✅ Why This Works

The algorithm maintains the invariant that the merged list built starting at `dummy.next` is always in sorted order. At each iteration, comparing `list1.val` and `list2.val` guarantees that the smallest available node among all unmerged nodes is selected. Because both input lists are sorted, when one list becomes empty, all nodes remaining in the other list are guaranteed to be greater than or equal to all previously merged nodes, allowing them to be attached directly without further comparisons.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n + m) — Each iteration of the loop advances either `list1` or `list2` by one node, processing every node in both lists at most once.** |
| Space | **O(1) — The merge is performed in-place by updating pointer references, using only a fixed number of extra pointers regardless of list size.** |

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

Using a dummy head node avoids conditional checks for initializing a list, allowing an in-place merge of two sorted linked lists by adjusting pointers in linear time.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/merge-two-sorted-lists/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
