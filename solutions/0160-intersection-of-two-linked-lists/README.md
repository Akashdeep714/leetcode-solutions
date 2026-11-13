# 🧩 160. Intersection of Two Linked Lists

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · Linked List · Two Pointers  
> **Solutions:** 4 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/intersection-of-two-linked-lists/)

---

## 📝 Problem

Given the heads of two singly linked lists `headA` and `headB`, return the node reference where the two lists intersect, or `null` if no intersection exists.

---

## 🛠️ Solutions

This folder contains **4 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Brute Force / Nested Loop Comparison

> **Language:** Java
> **Runtime:** `1486 ms`  
> **Memory:** `52.2 MB`

#### 💡 Intuition

This brute-force approach relies on the definition of list intersection: two linked lists intersect if and only if they share a common node reference in memory. To find this node, we can test every node in list A against every node in list B. If either list is empty, or if the lists share no common nodes, the nested traversal finishes and safely concludes there is no intersection. While simple and requiring no extra space, comparing all node pairs results in quadratic comparisons relative to list lengths.

#### 🧠 Algorithmic Pattern

> **Brute Force / Nested Loop Comparison**

#### 🚀 Approach

1. Initialize a pointer `currA` to `headA` to begin traversing the first linked list.
2. Enter an outer loop that continues as long as `currA` is not `null`.
3. At the start of each outer loop iteration, reset pointer `currB` to `headB` to scan the second linked list from its head.
4. Enter an inner loop that continues as long as `currB` is not `null`.
5. Check for reference equality with `currA == currB`. If true, return `currA` immediately as the intersection node.
6. Advance `currB` to `currB.next` to check the next node in list B.
7. Once the inner loop completes without finding a match, advance `currA` to `currA.next`.
8. If `currA` becomes `null` without finding any match, return `null`.

#### ✅ Why This Works

If two linked lists intersect at a specific node, that single node instance belongs to both list structures. By evaluating reference equality (`currA == currB`) across all pairs of nodes from list A and list B, the algorithm exhaustively searches the entire Cartesian product of nodes and is guaranteed to identify the first shared memory address if one exists.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m * n) — The outer loop runs up to $m$ times and the inner loop runs up to $n$ times, resulting in a worst-case time complexity of $O(m \times n)$ pointer comparisons.** |
| Space | **O(1) — The implementation only uses two pointer variables (`currA` and `currB`), allocating no additional memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Checking linked list intersection requires matching node memory addresses rather than values; while brute-force pair checking costs $O(m \times n)$ time, it serves as a baseline before optimizing to $O(m + n)$ using two pointers or hash sets.

---

### 🧠 Solution 2 — Hash Table / Set Lookup

> **Language:** Java
> **Runtime:** `9 ms`  
> **Memory:** `52.1 MB`

#### 💡 Intuition

By storing all node references of list A in a set, we can check whether any node in list B has already been visited in $O(1)$ time.

#### 🧠 Algorithmic Pattern

> **Hash Table / Set Lookup**

#### 🚀 Approach

1. Traverse list A completely and insert every node reference into a `HashSet`.
2. Traverse list B node by node.
3. For each node in list B, check if it exists in the `HashSet`.
4. Return the first node reference from list B that is present in the set; if none match, return `null`.

#### ✅ Why This Works

The `HashSet` relies on object identity/references. The first node in list B that is found in the set is the exact point of intersection.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m + n) — Traversing list A takes $O(m)$ time to populate the set, and traversing list B takes up to $O(n)$ time for hash lookups, totaling $O(m + n)$ overall.** |
| Space | **O(m) — The `HashSet` stores references for all $m$ nodes of list A, consuming $O(m)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Trading auxiliary space for linear time complexity provides a straightforward $O(m + n)$ solution.

---

### 🧠 Solution 3 — Two Pointers / Path Concatenation

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `51.8 MB`

#### 💡 Intuition

If pointer A traverses list A then list B ($m + n$), and pointer B traverses list B then list A ($n + m$), both pointers will travel the exact same total distance and meet at the intersection node (or both reach `null`).

#### 🧠 Algorithmic Pattern

> **Two Pointers / Path Concatenation**

#### 🚀 Approach

1. Initialize pointer `currA` at `headA` and pointer `currB` at `headB`.
2. Loop while `currA != currB`.
3. In each step, advance `currA` to `currA.next`; if `currA` becomes `null`, redirect it to `headB`.
4. Similarly, advance `currB` to `currB.next`; if `currB` becomes `null`, redirect it to `headA`.
5. When `currA == currB`, return `currA` (which is either the intersection node or `null`).

#### ✅ Why This Works

Let list A have $a$ unshared nodes, list B have $b$ unshared nodes, and shared suffix length be $c$. Pointer A travels $a + c + b$ nodes, while pointer B travels $b + c + a$ nodes. Both cover $a + b + c$ nodes and arrive at the intersection simultaneously.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m + n) — Each pointer traverses at most $m + n$ nodes before either meeting at the intersection or reaching `null` simultaneously.** |
| Space | **O(1) — Only two pointer references (`currA`, `currB`) are stored, requiring $O(1)$ extra memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution-3.java)

#### 🎯 Key Takeaway

Concatenating traversal paths equalizes total path length dynamically, achieving optimal time and space complexity cleanly.

---

### 🧠 Solution 4 — Two Pointers / Precomputed Offset Alignment

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `52.5 MB`

#### 💡 Intuition

The tail portions of both lists from the intersection onwards are shared and identical in length. By computing list lengths, we can advance the pointer of the longer list by the difference in lengths so both pointers start at equal distances from the end.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Precomputed Offset Alignment**

#### 🚀 Approach

1. Traverse list A to calculate its length `lenA`.
2. Traverse list B to calculate its length `lenB`.
3. Calculate `diff = |lenA - lenB|`.
4. Reset pointers to `headA` and `headB`, then advance the pointer of the longer list by `diff` steps.
5. Traverse both pointers together until `currA == currB` or `null` is reached.
6. Return the matching node.

#### ✅ Why This Works

Aligning the starting positions eliminates the head length disparity, ensuring both pointers reach the intersection node at the exact same iteration step.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m + n) — Traversing both lists to compute lengths takes $O(m + n)$ time. Skipping the offset difference takes at most $O(|m - n|)$ steps, and the final combined traversal takes $O(\min(m, n))$ steps. Total time complexity is $O(m + n)$.** |
| Space | **O(1) — Uses a few integer variables and pointers, requiring constant $O(1)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-4.java)

#### 🎯 Key Takeaway

Explicit length calculation aligns starting offsets, guaranteeing synchronization without modifying list structure.


---

## 🎯 Key Takeaway

This repository currently contains 4 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-linked-lists/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
