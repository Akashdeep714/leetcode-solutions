# 🧩 349. Intersection of Two Arrays

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Two Pointers · Binary Search · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/intersection-of-two-arrays/)

---

## 📝 Problem

Find the unique common elements present in two integer arrays, nums1 and nums2, returning the result in any order.

---

## 💡 Intuition

To quickly determine whether an element from nums2 exists in nums1, we can collect all unique elements of nums1 into a HashSet. As we iterate through nums2, we check if each value is present in our set. Using set.remove(num) allows us to perform this membership check and simultaneously consume the element: if the value was present, remove returns true and deletes it from the set. This ensures each intersecting value is processed and recorded exactly once, eliminating duplicate results. We can then reuse the space in nums1 to write output values in-place before trimming the array.

---

## 🧠 Algorithmic Pattern

> **Hash Set**

---

## 🚀 Approach

1. Initialize an empty HashSet named set to store the elements of nums1.
2. Iterate through nums1 and insert every integer into set.
3. Initialize a write index k = 0 to track the number of unique intersecting elements found.
4. Iterate through each integer num in nums2.
5. Call set.remove(num): if it returns true, num was present in set and has not been processed yet.
6. Upon a successful removal, write num to nums1[k] and increment k.
7. Return the prefix of nums1 of length k using Arrays.copyOf(nums1, k).

---

## ✅ Why This Works

Inserting elements of nums1 into a HashSet allows average O(1) time membership checks. The set.remove(num) operation returns true only on its first call for any given num that existed in nums1. Subsequent duplicate occurrences of num in nums2 will attempt set.remove(num), which will return false because the value was already deleted. This guarantees both that every written element exists in both arrays and that no element is written more than once.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(m + n)** |
| Space | **O(m)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `44.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Calling Set.remove() inside a conditional check serves as both a membership test and a deduplication mechanism in a single O(1) step.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-arrays/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
