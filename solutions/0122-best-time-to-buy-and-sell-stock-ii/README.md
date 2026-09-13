# 🧩 122. Best Time to Buy and Sell Stock II

> **Difficulty:** 🟡 Medium  
> **Topics:** Array · Dynamic Programming · Greedy  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

---

## 📝 Problem

Find the maximum total profit achievable from buying and selling stock given daily prices, with the ability to make multiple transactions but holding at most one share at a time.

---

## 💡 Intuition

Any profit made over a span of several days (buying on day A and selling on day B) can be broken down into the sum of daily price changes: prices[B] - prices[A] = (prices[A+1] - prices[A]) + (prices[A+2] - prices[A+1]) + ... + (prices[B] - prices[B-1]). Because we can trade on the same day, collecting profit across a continuous price rise is mathematically identical to capturing every positive single-day price difference. Whenever the price increases from one day to the next, we greedily lock in that incremental profit; whenever the price drops, we simply do not trade across that day.

---

## 🧠 Algorithmic Pattern

> **Greedy**

---

## 🚀 Approach

1. Initialize an integer variable `maxProfit` to `0` to accumulate the total profit.
2. Loop through the `prices` array starting from index `1` up to `prices.length - 1`.
3. For each index `i`, compare the current day's price `prices[i]` with the previous day's price `prices[i-1]`.
4. Check if `prices[i] > prices[i-1]`.
5. If the current price is strictly greater than the previous day's price, add the difference `prices[i] - prices[i-1]` directly to `maxProfit`.
6. Return `maxProfit` as the final result after iterating through all daily price pairs.

---

## ✅ Why This Works

The total profit from buying at day j and selling at day k is given by prices[k] - prices[j]. This difference can be expressed as a telescoping sum of adjacent daily differences sum_{m=j+1}^{k} (prices[m] - prices[m-1]). By adding every positive term (prices[i] - prices[i-1] > 0) and skipping every negative term, the greedy algorithm extracts the maximum possible sum over all possible valid transaction sequences while avoiding all loss-inducing price drops.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

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

When unlimited transactions are allowed, global profit maximization over continuous upward trends can be simplified into a greedy sum of all positive single-step differences.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
