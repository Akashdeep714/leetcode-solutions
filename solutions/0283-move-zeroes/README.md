# 🧩 283. Move Zeroes

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/move-zeroes/)

---

## 📝 Problem

Rearrange an integer array in-place so all non-zero elements retain their relative order at the beginning, followed by all zeroes at the end.

---

## 💡 Intuition

Instead of repeatedly swapping elements, we can compress all non-zero elements towards the front of the array in a single pass. By using a write pointer `j` alongside a read pointer `i`, every non-zero value encountered at `nums[i]` can be copied directly to `nums[j]`. Once all non-zero elements are placed sequentially at indices `0` through `j - 1`, the remaining positions from `j` to the end of the array are simply filled with zeroes.

---

## 🧠 Algorithmic Pattern

> **Two Pointers**

---

## 🚀 Approach

1. Initialize a write pointer `j` to `0`, representing the index where the next non-zero element should be stored.
2. Iterate through the array with a read pointer `i` from index `0` to `nums.length - 1`.
3. For each index `i`, check if `nums[i]` is non-zero (`nums[i] != 0`).
4. If `nums[i]` is non-zero, assign `nums[j] = nums[i]` and increment `j` by `1`.
5. After the loop finishes scanning all elements, all non-zero values occupy indices `0` through `j - 1` in their original relative order.
6. Execute a second loop while `j < nums.length` to set `nums[j] = 0` and increment `j` until the end of the array is reached.

---

## ✅ Why This Works

The read pointer `i` inspects elements in sequential left-to-right order, ensuring non-zero elements are written into contiguous positions `0` to `j - 1` without altering their original sequence. Because `j` is always less than or equal to `i`, overwriting `nums[j]` never destroys an unread value ahead of `i`. Filling all remaining indices from `j` to `nums.length - 1` with zeroes completes the required transformation while preserving the array's original length and element count.

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
| Memory | `47.4 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

To compact filtered values in an array in-place without altering order, use a write pointer to shift valid elements forward sequentially and fill any remaining tail elements in a subsequent pass.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/move-zeroes/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
