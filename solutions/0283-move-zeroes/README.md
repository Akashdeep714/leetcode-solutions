# 🧩 283. Move Zeroes

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/move-zeroes/)

---

## 📝 Problem

Relocate all zero values to the end of an array while maintaining the relative order of non-zero elements in-place.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Two Pointers / Two-Pass Array Modification

> **Language:** Java
> **Runtime:** `2 ms`  
> **Memory:** `47.4 MB`

#### 💡 Intuition

Instead of shifting elements every time a zero is encountered, we can compress all non-zero elements toward the front using a write pointer. Once all non-zero elements are copied in order, every remaining array slot from the write pointer to the end must be filled with zero.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Two-Pass Array Modification**

#### 🚀 Approach

1. Initialize a write pointer `j` to 0.
2. Iterate through the array with a read pointer `i` from index 0 to `nums.length - 1`.
3. If `nums[i]` is non-zero, write `nums[i]` to `nums[j]` and increment `j`.
4. After completing the first pass, run a second loop from `j` to `nums.length - 1`, setting each position to 0.

#### ✅ Why This Works

Processing non-zero elements from left to right preserves their relative ordering. Because the write pointer `j` never advances faster than the read pointer `i`, non-zero values are safely copied forward without overwriting unread values. The second loop fills the remaining `n - j` trailing slots with zeroes.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The array is traversed twice: first to copy non-zero elements, and second to fill zeroes. Both passes take linear time relative to the length of the array $n$, resulting in overall $O(n)$ time complexity.** |
| Space | **O(1) — The algorithm operates directly on the input array in-place using two integer pointer variables, requiring $O(1)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

Decoupling array compaction into 'collecting non-zero elements' followed by 'filling zeroes' simplifies in-place array reordering without extra memory.

---

### 🧠 Solution 2 — Two Pointers / Single-Pass In-Place Partitioning

> **Language:** Java
> **Runtime:** `2 ms`  
> **Memory:** `47.8 MB`

#### 💡 Intuition

Maintain a write pointer `j` that tracks where the next non-zero element should be placed. As we scan the array, whenever we encounter a non-zero element at `i`, we move it to `j` and immediately clear position `i` to 0 (handling the case where `i == j` gracefully). This zeroes out old positions on the fly without a second loop.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Single-Pass In-Place Partitioning**

#### 🚀 Approach

1. Initialize a write pointer `j` to 0.
2. Iterate through the array with `i` from index 0 to `nums.length - 1`.
3. When `nums[i]` is non-zero, store its value, set `nums[i] = 0`, and assign the saved value to `nums[j]`.
4. Increment `j` after placing the non-zero element.

#### ✅ Why This Works

When `i == j` (before any zeroes are encountered), setting `nums[i] = 0` followed by `nums[j] = temp` leaves the element unchanged. When `i > j`, `nums[i]` was a non-zero value that gets moved to index `j`, leaving `nums[i]` correctly zeroed out. This maintains the invariant that all elements before `j` are non-zero and all elements between `j` and `i` are zeroes.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm processes each element of the array exactly once in a single pass, performing $O(1)$ constant-time operations per element, giving an overall time complexity of $O(n)$.** |
| Space | **O(1) — The array is modified entirely in-place with a single extra index pointer `j` and a temporary scalar variable, taking $O(1)$ auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Combining element placement and zeroing within a single iteration reduces total array write operations and eliminates the need for a post-processing fill loop.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/move-zeroes/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
