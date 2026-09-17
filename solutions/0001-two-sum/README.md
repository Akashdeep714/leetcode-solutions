# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

Given an array of integers nums and an integer target, return the indices of two numbers that add up to target.

---

## 💡 Intuition

Instead of checking every pair of numbers using nested loops, we can search for the required complement value in constant time using a hash map. For each element nums[i], the number needed to reach the target is lookupNumber = target - nums[i]. By keeping track of previously seen numbers and their indices in a hash map as we iterate, we can immediately identify if the complementary value was already encountered, allowing us to solve the problem in a single pass.

---

## 🧠 Algorithmic Pattern

> **Hash Table**

---

## 🚀 Approach

1. Initialize an empty hash map named map to store array values as keys and their corresponding indices as values.
2. Iterate through the array nums using a loop counter i from 0 to nums.length - 1.
3. Calculate the required complement for the current number: lookupNumber = target - nums[i].
4. Check if map already contains lookupNumber using map.containsKey(lookupNumber).
5. If lookupNumber is in map, return a new integer array containing the current index i and map.get(lookupNumber).
6. If lookupNumber is not in map, store the current element and its index by calling map.put(nums[i], i).
7. If the loop finishes without finding a matching pair, return [-1, -1] as a fallback.

---

## ✅ Why This Works

The equation nums[i] + nums[j] = target can be rewritten as nums[j] = target - nums[i]. By inserting each element into the hash map as we iterate, every element at index j < i is available for constant-time lookup. When the loop reaches the second number of the solution pair, its complement (the first number) is already stored in the hash map, ensuring the exact indices are found without duplicate checks or using the same element twice.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(n)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `47.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a hash map to look up complementary values (target - current_value) converts a slow O(n^2) pair search into an efficient O(n) single-pass algorithm.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
