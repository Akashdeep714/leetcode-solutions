# 🧩 167. Two Sum II - Input Array Is Sorted

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Two Pointers · Binary Search  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

---

## 📝 Problem

Given a 1-indexed sorted array of integers and a target value, find the 1-based indices of two numbers that add up to target.

---

## 💡 Intuition

Because the array is sorted in non-decreasing order, the smallest values are on the left and the largest are on the right. By placing one pointer at the beginning and another at the end, we can evaluate the sum of the extreme values. If the sum exceeds the target, decreasing the right pointer reduces the sum; if the sum is below the target, increasing the left pointer raises the sum. This monotonic property allows us to narrow down the answer in linear time without extra space.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize pointer `left` to index `0` and pointer `right` to index `numbers.length - 1`.
2. Loop while `left` is strictly less than `right`.
3. Calculate the current sum `sum = numbers[left] + numbers[right]`.
4. If `sum == target`, return a new array containing the 1-based indices `[left + 1, right + 1]`.
5. If `sum > target`, decrement `right` by 1 to test a smaller sum.
6. If `sum < target`, increment `left` by 1 to test a larger sum.
7. Return `[-1, -1]` as a fallback if no pair is found (guaranteed not to occur per problem constraints).

---

## ✅ Why This Works

At any step, if `numbers[left] + numbers[right] > target`, then `numbers[right]` cannot be paired with any element at index `k >= left` because all such elements are greater than or equal to `numbers[left]`, making their sums even larger. Thus, `numbers[right]` can be safely eliminated by decrementing `right`. Symmetric logic applies when the sum is less than `target`, allowing us to increment `left`. This invariant guarantees that we never skip the unique target pair.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Each iteration of the while loop either increments `left` or decrements `right`, processing at most $n$ elements in total.** |
| Space | **O(1) — The algorithm only allocates a constant number of scalar variables (`left`, `right`, `sum`) regardless of the array size.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `48.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Sorting enables a two-pointer approach that shrinks the search space from opposite ends in linear time while using $O(1)$ auxiliary space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
