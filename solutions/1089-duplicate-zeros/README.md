# 🧩 1089. Duplicate Zeros

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Two Pointers  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/duplicate-zeros/)

---

## 📝 Problem

Duplicate every zero in a fixed-length array while discarding elements that overflow the original array length.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — Auxiliary Space Buffer

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `47 MB`

#### 💡 Intuition

Modifying the array in place from left to right causes unread elements to be overwritten. By creating a temporary destination array, we can safely write elements forward without losing original values.

#### 🧠 Algorithmic Pattern

> **Auxiliary Space Buffer**

#### 🚀 Approach

1. Create a destination array `dest` of the same length as the input array `arr`.
2. Use a source pointer `s` to read from `arr` and a destination pointer `d` to write to `dest`.
3. Iterate while both pointers are within valid array boundaries.
4. If `arr[s]` is zero, set `dest[d]` to zero, increment `d`, and if `d` is still within bounds, set `dest[d]` to zero again.
5. If `arr[s]` is non-zero, copy `arr[s]` directly to `dest[d]`.
6. Increment both pointers and repeat until the array is filled.
7. Copy all elements from `dest` back to `arr`.

#### ✅ Why This Works

The auxiliary buffer isolates write operations from read operations, eliminating the write-conflict problem inherent in forward in-place modification.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — We iterate through the array once to fill the destination array and once more to copy elements back, resulting in 2 * N steps, which is O(n).** |
| Space | **O(n) — An auxiliary array `dest` of size N is allocated, using O(n) additional space.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

Using extra space simplifies in-place overwriting problems into simple array construction when memory constraints are relaxed.

---

### 🧠 Solution 2 — Two Pointers / Two-Pass In-Place Modification

> **Language:** Java
> **Runtime:** `1 ms`  
> **Memory:** `47.2 MB`

#### 💡 Intuition

Writing elements forward in-place overwrites data before it can be read. However, if we know where the final elements will end up, we can write from right to left (backwards) without overwriting unread elements.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Two-Pass In-Place Modification**

#### 🚀 Approach

1. Pass 1: Count how many zeros will be duplicated before reaching the logical boundary of the original length.
2. Handle the edge case where a zero sits exactly at the boundary and can only be written once without duplication.
3. Pass 2: Iterate backwards from the determined boundary index towards index 0.
4. If the current element is a zero, write zero twice at the shifted destination indices and decrease the shift offset.
5. If the current element is non-zero, place it at its new shifted position.

#### ✅ Why This Works

Working backwards ensures that elements are moved to their final destination indices after those destination positions have already been processed, preventing data loss.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The array is traversed twice: once to calculate the final boundary and once to shift elements, running in O(n) total time.** |
| Space | **O(1) — Only a few scalar variables are used to track zero counts and pointer indices, requiring O(1) auxiliary space.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

When array modifications shift elements to the right, iterating backwards from right to left enables O(1) space in-place operations.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/duplicate-zeros/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
