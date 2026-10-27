# 🧩 209. Minimum Size Subarray Sum

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Binary Search · Sliding Window · Prefix Sum  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/minimum-size-subarray-sum/)

---

## 📝 Problem

Find the minimal length of a contiguous subarray in an array of positive integers whose sum is at least target, or return 0 if no such subarray exists.

---

## 💡 Intuition

Because all elements in the array are positive integers, the window sum increases monotonically as we expand the right boundary and decreases monotonically as we shrink the left boundary. This monotonicity allows us to use a dynamic sliding window: we expand the right endpoint until the running sum reaches or exceeds target, and then immediately shrink from the left endpoint to find the shortest valid subarray ending at that right position before expanding further.

---

## 🧠 Algorithmic Pattern

> **Sliding Window**

---

## 🚀 Approach

1. Initialize `minDis` to `Integer.MAX_VALUE` to track the shortest subarray length, `left` and `right` pointers to `0`, and `runSum` to `0` for maintaining the current window's sum.
2. Iterate `right` from `0` to `nums.length - 1`, adding `nums[right]` to `runSum` in each iteration to expand the window.
3. While `runSum` is greater than or equal to `target`, attempt to shrink the window from the left.
4. Inside the inner loop, update `minDis` with the minimum of its current value and the current window length, `right - left + 1`.
5. Subtract `nums[left]` from `runSum` and increment `left` by `1` to test if a smaller window ending at `right` can still satisfy the sum constraint.
6. After the outer loop finishes examining all elements, return `0` if `minDis` was never updated (`minDis == Integer.MAX_VALUE`), otherwise return `minDis`.

---

## ✅ Why This Works

The monotonicity guaranteed by positive integers ensures that once a window `[left, right]` reaches a sum of at least `target`, expanding `right` further with the same `left` would only produce longer valid subarrays, which cannot beat the current length for that starting position `left`. Therefore, it is safe to incrementally move `left` forward to find the minimal valid window starting at or after `left` without skipping any candidate that could yield a shorter valid length.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Both the `left` and `right` pointers advance through the array at most `n` times, resulting in at most `2n` total pointer operations.** |
| Space | **O(1) — The algorithm only tracks a few integer scalar variables (`minDis`, `left`, `right`, `runSum`), using constant extra space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `69.2 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When array elements are strictly positive, subarray sums are monotonic with respect to window boundaries, allowing a two-pointer sliding window to inspect all candidate minimal subarrays in linear time.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/minimum-size-subarray-sum/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
