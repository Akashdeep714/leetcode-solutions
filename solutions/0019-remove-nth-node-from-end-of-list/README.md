# 🧩 19. Remove Nth Node From End of List

> **Difficulty:** 🟡 Medium  
> **Topics:** Linked List · Two Pointers  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

---

## 📝 Problem

Remove the n-th node from the end of a singly linked list and return the head of the modified list.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Two-pass Linked List Traversal

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `43 MB`

#### 💡 Intuition

The n-th node from the end is at a distance of len - n steps from the start of the list. Since a singly linked list can only be traversed forward, we can first make a full pass to count the total length of the list. In a second pass, we navigate to the node immediately before the target node to bypass it. Creating a dummy node pointing to the head simplifies edge cases—specifically when the node to be removed is the head itself (when len == n)—because the dummy node acts as a permanent predecessor.

#### 🧠 Algorithmic Pattern

> **Two-pass Linked List Traversal**

#### 🚀 Approach

1. Initialize a counter len = 0 and a pointer cur = head.
2. Traverse the linked list using cur, incrementing len until cur becomes null to compute the total node count.
3. Instantiate a dummy node with value 0 and set dummy.next = head to handle head deletions cleanly.
4. Compute jumps = len - n, which represents the number of forward steps required from dummy to reach the node preceding the target.
5. Initialize prev = dummy and advance prev forward jumps times using a loop.
6. Unlink the target node by reassigning prev.next = prev.next.next.
7. Return dummy.next, which holds the head of the updated list.

#### ✅ Why This Works

In a list of total length `len`, the n-th node from the end is located at 0-based index `len - n` relative to the head. Starting from a dummy node positioned before the head, advancing `len - n` steps stops exactly at the predecessor node (index `len - n - 1` relative to head). Modifying `prev.next` to point to `prev.next.next` effectively unlinks the target node without altering any other links in the list.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — The list is traversed twice—once to measure its total length N and once to reach the removal point—taking O(N) linear time overall.** |
| Space | **O(1) — The implementation only allocates a single dummy node and a few pointer variables, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using a dummy node placed before the head simplifies linked list node deletions by ensuring every node, including the original head, has a valid predecessor to update.

---

### 🧠 Solution 2 — Two Pointers / Fast & Slow Pointers

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `43.2 MB`

#### 💡 Intuition

Maintaining a fixed gap of n nodes between a fast pointer and a slow pointer allows us to find the node preceding the target when the fast pointer reaches the end.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Fast & Slow Pointers**

#### 🚀 Approach

1. Advance a fast pointer cur forward by n steps from the head.
2. Create a dummy head node pointing to head and place a slow pointer prev at dummy.
3. Advance both cur and prev simultaneously one step at a time until cur reaches null.
4. Update prev.next = prev.next.next to remove the target node and return dummy.next.

#### ✅ Why This Works

Because the distance between cur and prev is exactly n + 1 nodes (due to prev starting at dummy), when cur reaches null (end of list at position L + 1 relative to dummy), prev rests exactly at position L - n, which is the node right before the target.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — The fast pointer traverses the list of length N exactly once, performing the entire operation in O(N) time.** |
| Space | **O(1) — Only pointer references and a single dummy node are maintained, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Maintaining a fixed offset window with two pointers eliminates the need to pre-compute the list length and achieves single-pass execution.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
