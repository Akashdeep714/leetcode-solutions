# 🧩 705. Design HashSet

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Linked List · Design · Hash Function  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/design-hashset/)

---

## 📝 Problem

Design a custom HashSet data structure supporting `add`, `remove`, and `contains` operations for non-negative integer keys without using built-in hash table libraries.

---

## 💡 Intuition

To implement a hash set from scratch, we need a hash function to map integer keys to array indices and a mechanism to handle collisions when two keys map to the same index. This implementation uses separate chaining with a fixed array of 769 buckets (a prime number chosen to distribute keys evenly). Each bucket contains a Java `LinkedList`. When a key is inserted, removed, or checked, we map the key to a bucket index using `key % 769` and perform the corresponding linear search or modification on that specific bucket's linked list.

---

## 🧠 Algorithmic Pattern

> **Hash Table with Separate Chaining**

---

## 🚀 Approach

1. Define a `Bucket` class that encapsulates a Java `LinkedList<Integer>` to manage elements sharing the same hash index.
2. Instantiate `MyHashSet` with a fixed array `buckets` of size 769 (stored in `numBuckets`), populating each index with a new `Bucket` object.
3. Compute target bucket indices using the helper method `getIndex(key)`, which returns `key % 769`.
4. For `add(key)`: Locate the target bucket, search for `key` using `indexOf`, and prepend it to the linked list using `addFirst` if it is not already present.
5. For `remove(key)`: Locate the target bucket and invoke `remove(key)` on the linked list to delete the key if it exists.
6. For `contains(key)`: Locate the target bucket and check if `indexOf(key)` returns a index other than `-1`.

---

## ✅ Why This Works

The modulo operator `key % 769` deterministically maps any non-negative integer into the range `[0, 768]`. Storing elements in linked lists within each bucket guarantees that multiple keys mapping to the same bucket index coexist without collision conflicts. Checking for duplicate existence before adding ensures the set uniqueness property.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(1) — Assuming keys are distributed uniformly across the 769 buckets, each bucket contains N/769 elements on average, making bucket lookup and linked list search O(1) on average.** |
| Space | **O(N + K) — The memory overhead consists of a fixed array of K = 769 buckets plus additional nodes proportional to the number of unique inserted keys N.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `17 ms` |
| Memory | `53.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Separate chaining handles hash collisions by storing elements in a linked list per bucket, combining array indexing with linear traversal to achieve average O(1) set operations.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/design-hashset/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
