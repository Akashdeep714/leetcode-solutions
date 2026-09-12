# 🧩 121. Best Time to Buy and Sell Stock

> **Difficulty:** 🟢 Easy  
> **Topics:** Array · Dynamic Programming  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

---

## 📝 Problem

Find the maximum profit achievable by buying a stock on one day and selling it on a future day given an array of daily prices. Return 0 if no profit can be made.

---

## 💡 Intuition

To maximize profit, we want to buy at the lowest possible price prior to selling. As we iterate through the price list, every day represents a potential selling day. To achieve the highest profit on a given selling day, we should have bought at the lowest price seen up to that point. By maintaining the running minimum price and comparing the profit from selling on the current day against our overall maximum profit, we can determine the optimal transaction in a single pass.

---

## 🧠 Algorithmic Pattern

> **Greedy / One-Pass Dynamic Programming**

---

## 🚀 Approach

1. Initialize `minPrice` to `Integer.MAX_VALUE` to keep track of the lowest stock price encountered so far.
2. Initialize `maxProfit` to `0` to store the maximum profit found.
3. Iterate through each `price` in the `prices` array.
4. If the current `price` is less than `minPrice`, update `minPrice` to `price`.
5. If `price - minPrice` is greater than `maxProfit`, update `maxProfit` to this new profit value.
6. Return `maxProfit` after iterating through all daily prices.

---

## ✅ Why This Works

At any index `i`, `minPrice` correctly holds $\min(\text{prices}[0 \dots i])$. Selling on day `i` yields maximum profit when the buying price is as small as possible, which is exactly `minPrice`. By calculating `price - minPrice` for every day `i` and taking the maximum across all days, the code checks the optimal buy price for every possible sell day, guaranteeing the global maximum profit without breaking the requirement that buying must happen before selling.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(n)** |
| Space | **O(1)** |

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

When maximizing the difference between two elements subject to a sequential order constraint (e.g., buying before selling), track the running minimum in a single pass to solve the problem in $O(n)$ time and $O(1)$ space.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- [My Solution](./solution.java)

---

⭐ Automatically synchronized from an accepted LeetCode submission.
