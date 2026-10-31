# 🧩 1346. Check If N and Its Double Exist

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Two Pointers · Binary Search · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/check-if-n-and-its-double-exist/)

---

## 📝 Problem

Determine if an integer array contains two distinct elements where one is exactly twice the value of the other.

---

## 💡 Intuition

To check for a target arithmetic relation between pairs without performing an $O(n^2)$ double loop, we can store previously visited numbers in a hash set. For each number `num`, it could represent either the smaller half ($arr[j]$) or the larger double ($arr[i]$) of a valid pair. Therefore, we check if either its double (`2 * num`) or—if `num` is even—its half (`num / 2`) already exists in our set. Checking before inserting `num` into the set automatically ensures that the two elements come from distinct indices, even when handling zero.

---

## 🧠 Algorithmic Pattern

> **Hash Set**

---

## 🚀 Approach

1. Initialize an empty hash set `set` to store integers visited during iteration.
2. Iterate through each element `num` in the array `arr`.
3. Check if `set` already contains `2 * num`, indicating `num` is the half-value of a previously seen number.
4. Check if `num` is even (`num % 2 == 0`) and `set` contains `num / 2`, indicating `num` is the double of a previously seen number.
5. If either condition is true, immediately return `true`.
6. Add `num` to `set` for future element checks.
7. If the loop finishes without finding any valid pair, return `false`.

---

## ✅ Why This Works

Any valid pair of indices $(i, j)$ with $arr[i] = 2 	imes arr[j]$ has one element appearing earlier in the array than the other. By checking both `2 * num` and `num / 2` against previously stored elements before adding the current element to the set, the algorithm guarantees detection regardless of whether the double or the half appears first, while strictly enforcing $i \neq j$.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The array of length $n$ is traversed once, and each hash set lookup and insertion takes $O(1)$ time on average.** |
| Space | **O(n) — In the worst case, the hash set stores up to $n$ unique elements when no valid double pair exists.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `2 ms` |
| Memory | `45 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When searching for asymmetric pairwise relationships in an unsourced array, a single-pass hash set checking both possible directional conditions ($2 \times x$ and $x / 2$) achieves optimal linear time while enforcing distinct indices.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/check-if-n-and-its-double-exist/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
