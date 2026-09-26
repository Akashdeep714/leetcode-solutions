# 🧩 121. Best Time to Buy and Sell Stock

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Dynamic Programming  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

---

## 📝 Problem

Find the maximum profit from buying and selling a stock on a single day in the future.

---

## 💡 Intuition

To maximize profit on any given day, you should sell at the current price after having bought at the lowest price seen up to that point.

---

## 🧠 Algorithmic Pattern

> **Dynamic Programming / Greedy Single Pass**

---

## 🚀 Approach

1. Initialize `minPrice` to infinity and `maxProfit` to 0.
2. Iterate through each price in the array.
3. Update `minPrice` if the current day's price is lower than the recorded minimum.
4. Calculate potential profit (`price - minPrice`) and update `maxProfit` if it exceeds the current maximum profit.
5. Return `maxProfit` after completing the loop.

---

## ✅ Why This Works

Tracking the minimum price seen so far guarantees that for every selling day, the maximum possible profit for that day is evaluated. Scanning all days ensures the global maximum profit is captured.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm visits each price in the array of size $n$ exactly once, performing constant $O(1)$ comparisons and assignments per element.** |
| Space | **O(1) — The algorithm uses only a few primitive integer variables (`minPrice`, `maxProfit`), consuming constant $O(1)$ auxiliary space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `1 ms` |
| Memory | `94.3 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

Maintaining a running minimum during a single traversal solves the dynamic profit tracking problem efficiently without needing dynamic programming arrays or nested loops.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
