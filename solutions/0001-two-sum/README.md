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

The key idea is to remember useful information from elements that have already been processed. A hash map provides O(1) average lookup, allowing the solution to avoid repeatedly scanning the input.

### 🧠 Algorithmic Pattern

| Role | Pattern |
|---|---|
| Primary | **Hash Map** |
| Supporting | None |

---

## 🚀 Approach

1. Create a hash map to store information about previously processed values.
2. Traverse the input once.
3. For each element, compute the value or state needed to satisfy the problem.
4. Use the hash map for a fast average-time lookup.
5. Return or update the answer when the required condition is met.

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
| Time | **O(n)** |
| Space | **O(n)** |

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

- [LeetCode Problem](https://leetcode.com/problems/two-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
