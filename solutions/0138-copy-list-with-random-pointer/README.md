# 🧩 138. Copy List with Random Pointer

> **Difficulty:** 🟡 Medium  
> **Topics:** Hash Table · Linked List  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/)

---

## 📝 Problem

Create a deep copy of a linked list where each node has a standard 'next' pointer and an arbitrary 'random' pointer.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Hash Table / Graph Cloning

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `46.1 MB`

#### 💡 Intuition

The main challenge of deep copying a graph/list with random pointers is that a random pointer might point to a node that hasn't been created yet, or to a previously created node. Using a hash map to map `originalNode -> copiedNode` serves as a lookup table to ensure every original node is cloned exactly once and pointer relationships can be dynamically linked.

#### 🧠 Algorithmic Pattern

> **Hash Table / Graph Cloning**

#### 🚀 Approach

1. Check if the input head is null; if so, return null immediately.
2. Initialize a Map<Node, Node> to maintain mappings from original nodes to their newly allocated copies.
3. Create the clone of the head node and put the pair (head, newHead) into the map.
4. Traverse the list using pointers for the original list (`curr`) and copied list (`newCurr`).
5. For both `curr.random` and `curr.next`, check if the target node exists in the map. If it exists, retrieve its clone. If not, instantiate a new cloned node and insert it into the map.
6. Assign the retrieved/created cloned nodes to `newCurr.random` and `newCurr.next`, then advance to the next node.

#### ✅ Why This Works

The hash map acts as a cache/dictionary of visited nodes. When traversing a node's arbitrary edge (next or random), looking up the target node in the map guarantees we either link to an existing clone or create a new clone immediately, ensuring no duplicate nodes are created for the same original node.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We visit each node in the original linked list once and perform constant-time hash map lookups and insertions for every node's next and random pointers, resulting in O(n) total time complexity.** |
| Space | **O(n) — The hash map stores one key-value pair per node in the list, requiring O(n) auxiliary memory space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using a hash table maps graph/list nodes efficiently, handling forward and backward arbitrary pointers dynamically in O(n) time and O(n) auxiliary space.

---

### 🧠 Solution 2 — Two Pointers / In-place List Modification

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `45.7 MB`

#### 💡 Intuition

Instead of using an external hash map to store `originalNode -> clonedNode`, we can store each cloned node directly after its corresponding original node (`A -> A' -> B -> B'`). This structure provides immediate access to any cloned node: the copy of `curr.random` is simply `curr.random.next`.

#### 🧠 Algorithmic Pattern

> **Two Pointers / In-place List Modification**

#### 🚀 Approach

1. Pass 1 (Stitching): Traverse the original list and insert a clone of each node immediately following its original node (`curr.next = node; node.next = currNext`).
2. Pass 2 (Assign Random Pointers): Iterate through the interleaved list. For each original node `curr`, set its cloned node's random pointer: `curr.next.random = (curr.random != null) ? curr.random.next : null`.
3. Pass 3 (Untangle): Separate the interleaved list back into the original list and the newly constructed copied list by restoring original `next` links and chaining cloned `next` links together.
4. Return the head of the restored copied list.

#### ✅ Why This Works

Interleaving places each cloned node right next to its original counterpart. Because `original.next` points to `clone`, `original.random.next` is guaranteed to point to `clone.random`, resolving arbitrary random pointers in O(1) auxiliary space without hash table lookups.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm makes three linear passes over the linked list of length n, performing constant-time pointer updates in each pass, yielding O(n) overall runtime.** |
| Space | **O(1) — Only a constant number of pointer variables (`curr`, `newCurr`, `oldHead`, etc.) are used. The cloned nodes themselves form the returned result and do not count toward auxiliary space complexity.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

By temporarily mutating the input linked list structure to interleave original and copied nodes, we can map random pointers in-place and achieve optimal O(1) auxiliary space.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/copy-list-with-random-pointer/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
