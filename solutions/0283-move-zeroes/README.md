# 🧩 283. Move Zeroes

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/move-zeroes/)

---

## 📝 Problem

Rearrange an integer array in-place so all zero values are moved to the end while maintaining the original relative order of non-zero elements.

---

## 💡 Intuition

To shift all zeros to the end of the array in-place without altering the order of non-zero elements, we can use a two-pointer technique. A fast pointer `i` scans through every element of the array, while a slow pointer `j` tracks the destination index for the next non-zero element. Whenever `i` finds a non-zero number, we place it at index `j` and clear index `i` by setting it to zero. Because `j` only advances when a non-zero element is processed, all non-zero elements are gathered at the front in their original order, leaving zeros to fill the remaining positions at the end.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize a slow pointer `j = 0` to mark the insertion index for the next non-zero element.
2. Iterate through the array with a fast pointer `i` from index `0` to `nums.length - 1`.
3. At each step, check if the current element `nums[i]` is non-zero.
4. If `nums[i]` is non-zero, store its value in a temporary variable `temp`.
5. Set `nums[i] = 0` to clear the position at `i`.
6. Assign `temp` to `nums[j]` to place the non-zero value at the target position.
7. Increment `j` by `1` to advance the destination marker for future non-zero elements.

---

## ✅ Why This Works

The pointer `j` maintains the invariant that all elements strictly before `j` are non-zero values placed in their exact original order. Since `i` iterates sequentially from left to right, every non-zero value is encountered and written to `j` in order. When `i > j`, `nums[j]` is guaranteed to be a zero from a previous swap, so setting `nums[i] = 0` and `nums[j] = temp` effectively swaps the non-zero element with that zero. When `i == j` (before any zero has been encountered), setting `nums[i] = 0` followed by `nums[j] = temp` restores the non-zero element at index `i` without changing it. Consequently, once `i` finishes scanning, all non-zero elements occupy indices `0` through `j - 1`, and all remaining indices are filled with zeros.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `47.8 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using a two-pointer read/write strategy allows reordering array elements in-place in a single pass while preserving their original relative order without requiring extra memory.

---

---
### 🔀 Solution 2 — Two Pointers

> **Language:** Java  
> **Runtime:** `2 ms`  
> **Memory:** `47.4 MB`

#### 💡 Intuition

Instead of swapping elements whenever a non-zero value is encountered, we can overwrite elements from the beginning of the array. By maintaining a write pointer that tracks the position for the next non-zero element, we can perform a single pass to copy all non-zero numbers to the front in their original relative order. Once all non-zero elements are placed, any remaining indices from the write pointer to the end of the array must be filled with zeroes in a second pass.

#### 🧠 Algorithmic Pattern

> **Two Pointers**

#### 🚀 Approach

1. Initialize a write pointer `j = 0` to track the destination index for non-zero elements.
2. Iterate through the array with a read pointer `i` from `0` to `nums.length - 1`.
3. For each element `nums[i]`, check if it is non-zero; if so, assign `nums[j] = nums[i]` and increment `j`.
4. After the loop finishes, `j` points to the start of the trailing section that should contain zeroes.
5. Start a second loop while `j < nums.length`.
6. Set `nums[j] = 0` and increment `j` at each step until the array end is reached.

#### ✅ Why This Works

During the first pass, the loop invariant maintains that `nums[0...j-1]` contains all non-zero elements seen so far in `nums[0...i]` while preserving their original order. When `i` finishes scanning the entire array, `j` exactly equals the total count of non-zero elements. Filling the remaining indices from `j` to `nums.length - 1` with zeroes ensures that all zero values are placed at the end without corrupting the non-zero sequence.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm processes the array in two sequential linear passes, taking O(n) total time where n is the length of the array.** |
| Space | **O(1) — The operations are performed directly on the input array using only a single integer variable `j`, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/move-zeroes/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
