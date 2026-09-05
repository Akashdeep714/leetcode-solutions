# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Given an array
nums
 containing
n
 distinct numbers in the range
[0, n]
, return
the only number in the range that is missing from the array.

 

Example 1:

Input:

nums = [3,0,1]

Output:

2

Explanation:

n = 3
 since there are 3 numbers, so all numbers are in the range
[0,3]
. 2 is the missing number in the range since it does not appear in
nums
.

Example 2:

Input:

nums = [0,1]

Output:

2

Explanation:

n = 2
 since there are 2 numbers, so all numbers are in the range
[0,2]
. 2 is the missing number in the range since it does not appear in
nums
.

Example 3:

Input:

nums = [9,6,4,2,3,5,7,0,1]

Output:

8

Explanation:

n = 9
 since there are 9 numbers, so all numbers are in the range
[0,9]
. 8 is the missing number in the range since it does not appear in
nums
.

 

 

 

 

 

Constraints:

n == nums.length

1 <= n <= 10
4

0 <= nums[i] <= n

All the numbers of
nums
 are
unique
.

 

Follow up:
 Could you implement a solution using only
O(1)
 extra space complexity and
O(n)
 runtime complexity?

---

## 💡 Intuition

Because the search space has an exploitable order, each comparison can eliminate roughly half of the remaining possibilities. This reduces a linear search to logarithmic time.

### 🧠 Algorithmic Pattern

| Role | Pattern |
|---|---|
| Primary | **Binary Search** |
| Supporting | Hash Map · Sorting |

---

## 🚀 Approach

1. Initialize the search boundaries.
2. Calculate the middle position.
3. Use the ordering property to determine which half can still contain the answer.
4. Discard the other half and repeat until the answer is found.

---

## 🔍 Why This Works

The approach avoids unnecessary repeated work by maintaining the
right state or data structure while processing the input.

The key advantage comes from choosing an algorithmic pattern that
reduces the amount of work required at each step.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(log n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `Previously recorded` |
| Memory | `Previously recorded` |

> The Big-O complexity is inferred from the detected algorithmic
> pattern and is intended as a high-level guide.

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The most valuable part of this problem is recognizing the underlying
pattern and understanding why it reduces unnecessary computation.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
