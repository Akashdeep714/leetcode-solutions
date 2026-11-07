# 🧩 141. Linked List Cycle

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · Linked List · Two Pointers · Floyd's Cycle Finding Algorithm  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/linked-list-cycle/)

---

## 📝 Problem

Determine whether a singly-linked list contains a cycle, returning true if any node can be reached repeatedly by following next pointers, and false otherwise.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Floyd's Cycle Finding Algorithm (Two Pointers)

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `46.3 MB`

#### 💡 Intuition

If two runners race on a circular track at different speeds, the faster runner will eventually lap the slower runner and meet them again. We can apply this principle to a linked list using two pointers: a `slow` pointer moving one node per step and a `fast` pointer moving two nodes per step. If the list has no cycle, `fast` will safely hit the end (`null`). If a cycle exists, both pointers will eventually enter the loop, where `fast` closes the gap by one node in every iteration until both pointers meet at the exact same node.

#### 🧠 Algorithmic Pattern

> **Floyd's Cycle Finding Algorithm (Two Pointers)**

#### 🚀 Approach

1. Initialize two pointers, `slow` and `fast`, both starting at `head`.
2. Enter a `while` loop that continues as long as `fast` and `fast.next` are not `null`.
3. Advance `slow` by one step (`slow = slow.next`).
4. Advance `fast` by two steps (`fast = fast.next.next`).
5. Check if `slow == fast`. If they point to the exact same node reference, a cycle exists, so return `true`.
6. If the loop exits because `fast` or `fast.next` reached `null`, return `false` as the list is acyclic.

#### ✅ Why This Works

When there is a cycle of length $K$, both pointers will eventually enter it. Once inside, the distance between `fast` and `slow` along the cycle decreases by 1 in every iteration because `fast` gains 1 step on `slow` per step ($2 - 1 = 1$). Because the relative distance shrinks by 1 each step modulo $K$, the pointers are guaranteed to meet within at most $K$ iterations, accurately detecting the cycle without an infinite loop.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — If the list has no cycle, `fast` reaches the end in $N/2$ steps; if it has a cycle, `fast` catches up to `slow` in at most $N$ iterations, running in linear time total.** |
| Space | **O(1) — The algorithm only uses two pointer variables (`slow` and `fast`), requiring constant auxiliary space regardless of list size.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using fast and slow pointers moving at different speeds allows detecting cycles in linked structures in $O(n)$ time while maintaining $O(1)$ constant auxiliary memory.

---

### 🧠 Solution 2 — Hash Table / Hash Set

> **Language:** Java
> **Runtime:** `7 ms`  
> **Memory:** `46.1 MB`

#### 💡 Intuition

If we keep track of every node object we encounter during traversal, reaching a node that has already been stored indicates a cycle.

#### 🧠 Algorithmic Pattern

> **Hash Table / Hash Set**

#### 🚀 Approach

1. Create an empty `HashSet` to store node memory references (`ListNode`).
2. Traverse the linked list starting from `head` using a pointer `curr`.
3. At each node, check if `curr` is already present in the `HashSet`.
4. If present, return `true` as a cycle is detected.
5. Otherwise, add `curr` to the set and move `curr` to `curr.next`.
6. If `curr` becomes `null`, return `false`.

#### ✅ Why This Works

Node references in Java are unique memory addresses. If a cycle exists, traversing the list will eventually hit a node that was previously added to the set.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We visit each node at most once. Hash set membership check and insertion operate in average O(1) time, yielding O(n) total time complexity.** |
| Space | **O(n) — In the worst case (or when a cycle exists), the hash set stores references for up to N unique nodes, requiring O(n) extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Using a hash set to record node identity provides an intuitive way to detect cycles at the cost of linear memory space.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/linked-list-cycle/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
