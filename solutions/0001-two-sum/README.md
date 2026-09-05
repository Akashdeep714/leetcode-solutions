# 🧩 1. Two Sum

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum/)

---

## 📝 Problem

You are given an array of integers
nums
 and an integer
target
, return
indices of the two numbers such that they add up to
target
.

You may assume that each input would have
exactly
 one solution
, and you may not use the
same
 element twice.

You can return the answer in any order.

 

Example 1:

```text

Input:
 nums = [2,7,11,15], target = 9

Output:
 [0,1]

Explanation:
 Because nums[0] + nums[1] == 9, we return [0, 1].

```

Example 2:

```text

Input:
 nums = [3,2,4], target = 6

Output:
 [1,2]

```

Example 3:

```text

Input:
 nums = [3,3], target = 6

Output:
 [0,1]

```

 

Constraints:

2 <= nums.length <= 10
4

-10
9
 <= nums[i] <= 10
9

-10
9
 <= target <= 10
9

Only one valid answer exists.

 

Follow-up: 
Can you come up with an algorithm that is less than
O(n
2
)
 
time complexity?

---

## 💡 Intuition

The key to this problem is recognizing the right data structure or algorithmic pattern: **Array, Hash Table**. Instead of repeatedly checking unnecessary possibilities, the solution keeps track of the information required to make each decision efficiently.

---

## 🚀 Approach

1. Identify the main algorithmic pattern.
2. Traverse the input while maintaining the required state.
3. Use the relevant technique (Array, Hash Table) to avoid unnecessary work.
4. Return the result after processing the required input.

---

## ⏱️ Complexity

The exact complexity follows from the algorithm used in the accepted
solution.

**Runtime reported by LeetCode:** `52`  
**Memory reported by LeetCode:** `47024000`

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

The most important lesson is to recognize the underlying algorithmic
pattern and choose a data structure that avoids unnecessary repeated work.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
