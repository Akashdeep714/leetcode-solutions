# 🧩 142. Linked List Cycle II

> **Difficulty:** 🟡 Medium  
> **Topics:** Hash Table · Linked List · Two Pointers · Floyd's Cycle Finding Algorithm  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/linked-list-cycle-ii/)

---

## 📝 Problem

Given the head of a singly-linked list, find and return the node where a cycle begins, or return null if the list contains no cycle.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Hash Table

> **Language:** Java
> **Runtime:** `6 ms`  
> **Memory:** `46.2 MB`

#### 💡 Intuition

In a acyclic linked list, every node is visited at most once during traversal before reaching null. However, if a cycle exists, traversing the list will loop infinitely, revisiting nodes in the cycle. The key observation is that the very first node encountered a second time during traversal is the exact node where the cycle begins. By recording visited node memory addresses in a hash set, we can immediately detect when a node is revisited.

#### 🧠 Algorithmic Pattern

> **Hash Table**

#### 🚀 Approach

1. Initialize an empty hash set named set to store references to visited ListNode objects.
2. Set a pointer curr to head to begin traversing the list.
3. Execute a while loop that continues as long as curr is not null.
4. At each step, check if curr is already in set using set.contains(curr).
5. If set.contains(curr) is true, return curr immediately, as it is the first node revisited and thus the start of the cycle.
6. If curr is not in set, add it to set using set.add(curr).
7. Advance curr to curr.next to inspect the next node.
8. If the loop terminates because curr becomes null, return null indicating no cycle exists.

#### ✅ Why This Works

Nodes before the cycle entry point are visited exactly once as the traversal moves linearly from the head. Once traversal enters the cycle, it traverses around the loop and returns to the entry point. Since all nodes traversed so far—including the cycle entry point itself—were added to the set on their first visit, the cycle entry node is guaranteed to be the first node already present in the set upon a second visit.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We visit each node at most twice (or once if there is no cycle), performing O(1) average-time hash set lookups and insertions per node.** |
| Space | **O(n) — The hash set stores at most n unique node references, where n is the total number of nodes in the linked list.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using a hash set to track visited node references provides a clean O(n) time solution for cycle entry detection, though Floyd's Cycle-Finding Algorithm can achieve O(1) auxiliary space.

---

### 🧠 Solution 2 — Two Pointers (Fast & Slow)

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `46.2 MB`

#### 💡 Intuition

When a fast pointer (moving 2 steps) and a slow pointer (moving 1 step) meet inside a cycle, mathematical relationship shows that the distance from the head to the cycle start equalizes with the distance from the meeting point to the cycle start.

#### 🧠 Algorithmic Pattern

> **Two Pointers (Fast & Slow)**

#### 🚀 Approach

1. Initialize two pointers, `slow` and `fast`, both pointing to the head of the list.
2. Move `slow` by 1 step and `fast` by 2 steps until `fast` reaches null or `fast == slow`.
3. If `fast` or `fast.next` is null, there is no cycle, so return null.
4. Once `fast == slow`, keep `slow` at the meeting point and initialize a new pointer `curr` at `head`.
5. Advance both `curr` and `slow` one step at a time until they meet; their intersection node is the start of the cycle.

#### ✅ Why This Works

Let distance from head to cycle entry be $a$, cycle entry to meeting point be $b$, and remaining cycle length be $c$. Fast travels $a + b + k(b+c)$ and slow travels $a + b$. Because fast is twice as fast: $2(a + b) = a + b + k(b+c) \implies a = (k-1)(b+c) + c$. Thus, walking $a$ steps from head and $a$ steps from the meeting point leads directly to the cycle entry.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — Phase 1 (cycle detection) takes at most N steps for the pointers to meet inside the cycle. Phase 2 (finding entry) takes $a$ steps (where $a < N$). Hence, total time is bounded by O(N).** |
| Space | **O(1) — Only two pointer variables (`slow` and `fast`, plus `curr`) are used, consuming constant O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Floyd's algorithm solves cycle detection and entry location in linear time using only pointer manipulation without extra memory allocation.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/linked-list-cycle-ii/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
