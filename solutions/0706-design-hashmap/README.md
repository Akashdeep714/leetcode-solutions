# 🧩 706. Design HashMap

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Linked List · Design · Hash Function  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/design-hashmap/)

---

## 📝 Problem

Design a custom HashMap supporting put, get, and remove operations for integer keys and values without using built-in hash table libraries.

---

## 💡 Intuition

To build a HashMap from scratch, we need a way to map a large key space to a smaller array of buckets using a hash function. Because different keys can hash to the exact same index (a collision), we use separate chaining: each array index contains a bucket backed by a linked list of key-value pairs. Using a prime number size like 769 for the hash table array helps distribute keys uniformly and minimize collisions.

---

## 🧠 Algorithmic Pattern

> **Separate Chaining Hash Table**

---

## 🚀 Approach

1. Define a custom generic class Pair<U, V> to store key-value pairs.
2. Define a Bucket class containing a LinkedList of Pair<Integer, Integer> elements, providing bucket-level operations for searching, updating, inserting, and deleting pairs.
3. In Bucket.put(key, value), iterate through the list: if the key already exists, update its value; otherwise, prepend a new Pair(key, value) to the front of the list.
4. In Bucket.get(key) and Bucket.remove(key), iterate through the list to find the matching key to either return its value (returning -1 if not found) or remove the pair from the list.
5. Initialize MyHashMap with a fixed array of 769 Bucket instances.
6. Compute the bucket index for any key using the modulo hash function: key % 769.
7. Delegate put, get, and remove calls from MyHashMap to the corresponding Bucket at index key % 769.

---

## ✅ Why This Works

The modulo operation key % 769 maps any integer key into a valid array index within [0, 768]. Separate chaining handles collisions by storing all key-value pairs that hash to the same bucket in a linked list, while linear scanning within a bucket ensures unique keys are updated rather than duplicated.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(1) — Assuming a uniform distribution of keys across 769 buckets, each bucket contains a small constant number of elements on average, yielding O(1) average time complexity for put, get, and remove operations.** |
| Space | **O(N) — The memory overhead consists of a fixed array of 769 buckets plus O(N) space for storing the N unique key-value pairs currently present in the hash map.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `20 ms` |
| Memory | `51.9 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

A fundamental hash map can be constructed using an array of buckets combined with separate chaining (linked lists) and modulo hashing to handle collisions efficiently.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/design-hashmap/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
