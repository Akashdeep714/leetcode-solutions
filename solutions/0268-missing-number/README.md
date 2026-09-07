# 🧩 268. Missing Number

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Hash Table · Math · Binary Search · Bit Manipulation · Sorting  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/missing-number/)

---

## 📝 Problem

Find the single missing number from an array containing n distinct numbers in the range [0, n].

---

## 💡 Intuition

The bitwise XOR operation has two crucial properties: any number XORed with itself equals 0 (a ^ a = 0), and any number XORed with 0 remains unchanged (a ^ 0 = a). If we XOR every number from the full range [0, n] together with every number actually present in the array, all present numbers will appear twice and cancel each other out, leaving only the missing number.

---

## 🧠 Algorithmic Pattern

> **Bit Manipulation**

---

## 🚀 Approach

1. Initialize a variable `xor` to `nums.length`, which represents the upper bound `n` of the range [0, n].
2. Loop through the array using index `i` from `0` to `nums.length - 1`.
3. In each iteration, update `xor` by XORing it with the current index `i`.
4. Further update `xor` by XORing it with the array value `nums[i]`.
5. Continue the loop until all indices and array values have been processed.
6. Return `xor`, which holds the value of the missing number.

---

## ✅ Why This Works

XOR is commutative and associative, meaning order does not matter. By starting with `n` and XORing every index `i` from `0` to `n-1` alongside every element `nums[i]`, we effectively perform XOR across the set of all range numbers [0, n] and all elements in `nums`. Since every present number appears exactly twice (once as an index/upper bound and once inside `nums`), they cancel out to 0. The missing number appears only once, so the final result is the missing number.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `N/A` |
| Memory | `47100000` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Using XOR is a clever way to find missing or unique elements in O(1) space because identical numbers cancel out (a ^ a = 0) without risk of integer overflow.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/missing-number/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
