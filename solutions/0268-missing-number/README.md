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

The key to this problem is recognizing the right data structure or algorithmic pattern: **Array, Hash Table, Math**. Instead of repeatedly checking unnecessary possibilities, the solution keeps track of the information required to make each decision efficiently.

---

## 🚀 Approach

1. Identify the main algorithmic pattern.
2. Traverse the input while maintaining the required state.
3. Use the relevant technique (Array, Hash Table, Math, Binary Search) to avoid unnecessary work.
4. Return the result after processing the required input.

---

## ⏱️ Complexity

The exact complexity follows from the algorithm used in the accepted
solution.

**Runtime reported by LeetCode:** `0`  
**Memory reported by LeetCode:** `47100000`

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The most important lesson is to recognize the underlying algorithmic
pattern and choose a data structure that avoids unnecessary repeated work.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
