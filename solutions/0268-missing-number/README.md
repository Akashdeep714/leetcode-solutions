# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Find the one missing value from an array containing distinct numbers chosen from the range 0 through n.

---

## 💡 Intuition

XOR cancels equal values. Combine the expected range with the values in the array so every present number cancels itself, leaving only the missing number.

---

## 🧠 Algorithmic Pattern

> **🔀 XOR**

---

## 🚀 Approach

1. Initialize the XOR accumulator with the required range state.
2. Traverse the array and XOR each present value into the accumulator.
3. Also XOR the corresponding range values.
4. Let equal values cancel each other through XOR.
5. Return the value left in the accumulator.

---

## ✅ Why This Works

Because x ^ x = 0 and x ^ 0 = x, every value that exists in both the range and the array cancels. The only value without a matching partner is the missing number.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `47.1 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

XOR is a useful way to find one missing value without extra storage.

---

---
### 🔀 Solution 2 — Math

> **Language:** Java  
> **Runtime:** `0 ms`  
> **Memory:** `47.3 MB`

#### 💡 Intuition

The sum of all integers from 0 to n can be calculated in O(1) time using Gauss's summation formula, n * (n + 1) / 2. Since the input array contains every number in this range except one, the sum of the array's elements will be smaller than the expected total by exactly the missing number. Subtracting the actual sum of elements in the array from the expected sum directly isolates the missing value.

#### 🧠 Algorithmic Pattern

> **Math**

#### 🚀 Approach

1. Determine the size of the input array nums as n.
2. Calculate the total expected sum of integers from 0 to n using the formula n * (n + 1) / 2.
3. Initialize an integer variable actual to 0 to store the sum of all elements present in nums.
4. Iterate through each number num in nums and add it to actual.
5. Subtract actual from expected and return the difference as the missing number.

#### ✅ Why This Works

The set of numbers from 0 to n has a fixed mathematical sum of n * (n + 1) / 2. By linear equation, Sum(0..n) = Sum(nums) + missing_number. Subtracting the sum of the array elements from the total theoretical sum leaves only the missing number, regardless of the order in which elements appear in the array.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm iterates through the array of length n once to compute the sum of its elements, resulting in O(n) runtime.** |
| Space | **O(1) — The algorithm only uses a few scalar variables (n, expected, actual) to hold intermediate arithmetic results, using O(1) extra space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
