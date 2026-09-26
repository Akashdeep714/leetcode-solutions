# 🧩 122. Best Time to Buy and Sell Stock II

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Dynamic Programming · Greedy  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

---

## 📝 Problem

Find the maximum total profit from buying and selling a stock multiple times, holding at most one share at any time.

---

## 💡 Intuition

Since we can buy and sell on the same day, capturing any multi-day price increase (e.g., buying on day A and selling on day C) is mathematically identical to accumulating every consecutive daily price increase along that upward trend (A to B, then B to C). Therefore, we simply add up every positive price difference between consecutive days.

---

## 🧠 Algorithmic Pattern

> **Greedy Algorithm**

---

## 🚀 Approach

1. Initialize `maxProfit` to 0.
2. Iterate through the price array starting from index 1 to the end.
3. For each day `i`, compare `prices[i]` with the previous day's price `prices[i - 1]`.
4. If `prices[i] > prices[i - 1]`, add the difference `prices[i] - prices[i - 1]` to `maxProfit`.
5. Return `maxProfit` after examining all consecutive price pairs.

---

## ✅ Why This Works

Any profit over a strictly increasing sequence $p_1 \le p_2 \le \dots \le p_k$ equals $(p_k - p_1)$, which can be decomposed into $(p_2 - p_1) + (p_3 - p_2) + \dots + (p_k - p_{k-1})$. On decreasing steps, we abstain from trading (0 profit contribution). Summing all positive single-day differences captures the global optimal profit without needing explicit state management.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n) — The algorithm iterates through the `prices` array of size $n$ exactly once, performing constant-time comparisons and additions at each step.** |
| Space | **O(1) — Only a single variable (`maxProfit`) is used to maintain the running total profit, requiring $O(1)$ extra space.** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `0 ms` |
| Memory | `46.5 MB` |

---

## 💻 Solution

[View the complete Java solution →](./solution.java)

---

## 🎯 Key Takeaway

When unlimited transactions are permitted without transaction fees, maximizing total profit reduces to collecting every positive single-step gradient.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
