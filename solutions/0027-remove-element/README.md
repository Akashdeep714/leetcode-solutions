# 🧩 27. Remove Element

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/remove-element/)

---

## 📝 Problem

Remove all instances of a specific target value from an integer array in-place and return the count of remaining valid elements.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Two Pointers (Fast & Slow / Read & Write)

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `43.1 MB`

#### 💡 Intuition

Maintain a write pointer tracking where the next non-target element should go. As a read pointer iterates through the array, any element that does not equal `val` is copied to the write position, compacting all non-target elements to the front while preserving their relative order.

#### 🧠 Algorithmic Pattern

> **Two Pointers (Fast & Slow / Read & Write)**

#### 🚀 Approach

1. Initialize a write pointer `i = 0` to mark the boundary of valid elements.
2. Iterate through the array with a read pointer `j` from index 0 to `nums.length - 1`.
3. Whenever `nums[j] != val`, copy `nums[j]` to `nums[i]` and increment `i`.
4. Return `i` as the total count of non-`val` elements.

#### ✅ Why This Works

Elements equal to `val` are skipped by the read pointer, while elements not equal to `val` are written sequentially to index `i`. This shifts all non-`val` elements to the beginning of the array in-place.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm inspects each element of the array exactly once using the loop index `j`, performing linear `O(n)` work.** |
| Space | **O(1) — All operations modify `nums` in-place using two scalar integer variables (`i` and `j`), requiring `O(1)` auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

The fast/slow pointer technique is the standard approach for in-place array filtering when preserving relative order is preferred.

---

### 🧠 Solution 2 — Two Pointers (Opposite Ends / Boundary Reduction)

> **Language:** Java
> **Runtime:** `0 ms`  
> **Memory:** `43.7 MB`

#### 💡 Intuition

Since the problem explicitly permits changing element order, encountering `val` at index `i` allows us to instantly overwrite it with the last element of the active window (`nums[n-1]`) and decrement the valid array size `n`, avoiding unnecessary shifts.

#### 🧠 Algorithmic Pattern

> **Two Pointers (Opposite Ends / Boundary Reduction)**

#### 🚀 Approach

1. Initialize pointer `i = 0` and boundary length `n = nums.length`.
2. Loop while `i < n` to evaluate the current element `nums[i]`.
3. If `nums[i] == val`, replace `nums[i]` with `nums[n - 1]` and decrement `n` without incrementing `i` (to inspect the newly moved element).
4. If `nums[i] != val`, advance pointer `i` by 1.
5. Return `n` as the count of valid elements.

#### ✅ Why This Works

Instead of shifting all subsequent non-`val` elements forward, we discard the unwanted element by filling its spot with the element from the back of the array. The back element is then re-evaluated in the next iteration to ensure it is also valid.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — Both pointers move toward each other, doing at most `n` total steps in the worst case, resulting in linear `O(n)` time complexity.** |
| Space | **O(1) — The array is modified directly in-place using only two integer pointers (`i` and `n`), taking `O(1)` auxiliary memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

When element ordering does not matter, overwriting target values with elements from the end minimizes write operations, especially when target elements are rare.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/remove-element/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
