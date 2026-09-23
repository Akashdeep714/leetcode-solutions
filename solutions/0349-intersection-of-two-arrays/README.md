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

---
### 🔀 Solution 2 — Hash Table

> **Language:** Java  
> **Runtime:** `3 ms`  
> **Memory:** `45.2 MB`

#### 💡 Intuition

To find common elements between two arrays while ensuring the output contains no duplicates, we need both rapid element lookup and duplicate filtering. Converting each array into a hash set automatically eliminates duplicate values within the same array. By iterating through the unique elements of one set and checking for their presence in the second set using average O(1) lookups, we can efficiently extract only the shared unique values.

#### 🧠 Algorithmic Pattern

> **Hash Table**

#### 🚀 Approach

1. Initialize two hash sets, `s1` and `s2`, to store unique integers.
2. Iterate through `nums1` and add every element into `s1`.
3. Iterate through `nums2` and add every element into `s2`.
4. Allocate a result array `res` with size equal to `s1.size()` and set a pointer `k = 0`.
5. Iterate through each unique element `num` in `s1` and check if `s2.contains(num)` is true.
6. If `num` is present in `s2`, write `num` to `res[k]` and increment `k`.
7. Return the sliced array containing only the populated elements from index `0` up to `k` using `Arrays.copyOfRange(res, 0, k)`.

#### ✅ Why This Works

Inserting array values into hash sets enforces uniqueness by discarding duplicates. Iterating over `s1` guarantees that each candidate value is evaluated only once, and checking `s2.contains(num)` confirms that the value exists in both original arrays. This directly satisfies the set intersection property without producing duplicate elements in the final output.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n + m) — Inserting elements into hash sets and performing set membership checks takes average O(1) time per element, leading to O(n + m) total time where n and m are the lengths of nums1 and nums2.** |
| Space | **O(n + m) — Storing the unique elements of nums1 and nums2 in two hash sets plus allocating the temporary result array requires O(n + m) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/intersection-of-two-arrays/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
