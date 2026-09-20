# 🧩 485. Max Consecutive Ones

> **Difficulty:** 🟢 Easy  
> **Topics:** Array  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/max-consecutive-ones/)

---

## 📝 Problem

Given a binary array nums, find and return the maximum number of consecutive 1s in the array.

---

## 💡 Intuition

To find the maximum number of consecutive 1s in a single pass, we can maintain a running counter of the current streak of 1s. As we iterate through the array, encountering a 1 extends the current streak, so we increment our counter. Encountering a 0 signals the end of the streak, requiring us to update our maximum recorded streak and reset the counter back to 0. Since an array might end with a sequence of 1s without encountering a trailing 0 to trigger the update inside the loop, a final comparison after the loop ensures the last streak is also considered.

---

## 🧠 Algorithmic Pattern

> **Single Pass / Counter Variable**

---

## 🚀 Approach

1. Initialize two integer variables: `count` set to 0 to track the current streak of 1s, and `max` set to 0 to keep track of the maximum streak seen so far.
2. Loop through the array `nums` from index `0` up to `nums.length - 1`.
3. Inside the loop, check if `nums[i] == 1`. If it is, increment `count` by 1.
4. If `nums[i]` is `0`, update `max` using `Math.max(max, count)` to save the longest streak found so far, and then reset `count` to 0.
5. After the loop finishes, evaluate `Math.max(max, count)` one last time to account for any trailing streak of 1s that reached the end of the array, and return this value.

---

## ✅ Why This Works

The algorithm maintains the invariant that `count` accurately represents the length of the contiguous sequence of 1s up to the current index, while `max` holds the maximum length of any fully processed sequence. Resetting `count` on encountering 0 correctly partitions contiguous blocks of 1s. Comparing `count` against `max` both during transitions (at 0s) and at the end of traversal guarantees that every block of consecutive 1s is evaluated.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm iterates through the array of length n exactly once, performing constant-time O(1) operations at each element.** |
| Space | **O(1) — The algorithm uses only two integer variables (`count` and `max`), consuming constant O(1) extra memory.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `52.6 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When tracking contiguous streaks in an array, use a running counter that resets on invalidating elements, and always remember to check the final counter value after the loop ends to account for streaks that extend to the array boundary.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/max-consecutive-ones/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
