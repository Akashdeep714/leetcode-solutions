# 🧩 141. Linked List Cycle

> **Difficulty:** 🟢 Easy  
> **Topics:** Hash Table · Linked List · Two Pointers · Floyd's Cycle Finding Algorithm  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/linked-list-cycle/)

---

## 📝 Problem

Determine whether a singly-linked list contains a cycle, returning true if any node can be reached repeatedly by following next pointers, and false otherwise.

---

## 💡 Intuition

If two runners race on a circular track at different speeds, the faster runner will eventually lap the slower runner and meet them again. We can apply this principle to a linked list using two pointers: a `slow` pointer moving one node per step and a `fast` pointer moving two nodes per step. If the list has no cycle, `fast` will safely hit the end (`null`). If a cycle exists, both pointers will eventually enter the loop, where `fast` closes the gap by one node in every iteration until both pointers meet at the exact same node.

---

## 🧠 Algorithmic Pattern

> **Floyd's Cycle Finding Algorithm (Two Pointers)**

---

## 🚀 Approach

1. Initialize two pointers, `slow` and `fast`, both starting at `head`.
2. Enter a `while` loop that continues as long as `fast` and `fast.next` are not `null`.
3. Advance `slow` by one step (`slow = slow.next`).
4. Advance `fast` by two steps (`fast = fast.next.next`).
5. Check if `slow == fast`. If they point to the exact same node reference, a cycle exists, so return `true`.
6. If the loop exits because `fast` or `fast.next` reached `null`, return `false` as the list is acyclic.

---

## ✅ Why This Works

When there is a cycle of length $K$, both pointers will eventually enter it. Once inside, the distance between `fast` and `slow` along the cycle decreases by 1 in every iteration because `fast` gains 1 step on `slow` per step ($2 - 1 = 1$). Because the relative distance shrinks by 1 each step modulo $K$, the pointers are guaranteed to meet within at most $K$ iterations, accurately detecting the cycle without an infinite loop.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — If the list has no cycle, `fast` reaches the end in $N/2$ steps; if it has a cycle, `fast` catches up to `slow` in at most $N$ iterations, running in linear time total.** |
| Space | **O(1) — The algorithm only uses two pointer variables (`slow` and `fast`), requiring constant auxiliary space regardless of list size.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `46.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using fast and slow pointers moving at different speeds allows detecting cycles in linked structures in $O(n)$ time while maintaining $O(1)$ constant auxiliary memory.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/linked-list-cycle/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
