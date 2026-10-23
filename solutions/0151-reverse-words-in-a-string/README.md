# 🧩 151. Reverse Words in a String

> **Difficulty:** 🟡 Medium  
> **Topics:** Two Pointers · String  
> **Solutions:** 2 unique approach(es)  
> **Language:** Java

[🔗 View Problem on LeetCode](https://leetcode.com/problems/reverse-words-in-a-string/)

---

## 📝 Problem

Reverse the order of words in a string containing potential extra spaces.

---

## 🛠️ Solutions

This folder contains **2 unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

### 🧠 Solution 1 — String Parsing / Built-in Abstraction

> **Language:** Java
> **Runtime:** `9 ms`  
> **Memory:** `43.8 MB`

#### 💡 Intuition

Instead of manually managing character pointers and spaces, leverage high-level string manipulation. Strip surrounding spaces, split on space sequences using regular expressions, reverse the word order, and join them back.

#### 🧠 Algorithmic Pattern

> **String Parsing / Built-in Abstraction**

#### 🚀 Approach

1. Trim leading and trailing whitespace from string `s`.
2. Split the trimmed string into an array of words using regex `\\s+` to automatically collapse multiple spaces.
3. Convert the array to a list and reverse it using `Collections.reverse()`.
4. Join the reversed words back into a single space-separated string using `String.join()`.

#### ✅ Why This Works

Splitting by `\\s+` isolates individual words into array elements while discarding all whitespace. Reversing the array flips the word sequence, and joining with `" "` formats the result according to problem requirements.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — Trimming, splitting using regex, reversing the array of words, and joining them into the result string all execute in linear time relative to the length $N$ of string `s`.** |
| Space | **O(N) — Creating the intermediate string array and list of words requires $O(N)$ extra memory.** |

#### 💻 Solution

[View the complete Java solution →](./solution.java)

#### 🎯 Key Takeaway

When string mutability isn't supported directly or memory constraints allow O(N) overhead, regex splitting and collection reversal provide clean and bug-resistant solutions.

---

### 🧠 Solution 2 — Two Pointers / Double Reversal Strategy

> **Language:** Java
> **Runtime:** `7 ms`  
> **Memory:** `43.7 MB`

#### 💡 Intuition

Reversing the entire character sequence flips the overall order of words, but leaves each word spelled backwards. Reversing each word individually restores original spelling while maintaining the reversed word order.

#### 🧠 Algorithmic Pattern

> **Two Pointers / Double Reversal Strategy**

#### 🚀 Approach

1. Trim leading/trailing spaces and iterate through input `s`, copying valid non-duplicate space characters into a `StringBuilder`.
2. Reverse the entire content of the `StringBuilder` using two pointers moving towards the middle.
3. Iterate through the `StringBuilder` to find word boundaries (substrings between space characters).
4. Reverse each word in-place within the `StringBuilder` using two pointers.
5. Convert the `StringBuilder` to string and return.

#### ✅ Why This Works

The overall reverse operation transforms sequence $W_1 W_2 \dots W_k$ into $W_k^R \dots W_2^R W_1^R$. Reversing each individual word $W_i^R$ undoes internal reversal, yielding $W_k \dots W_2 W_1$.

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **O(N) — Filtering extra spaces, reversing the complete string, and reversing each word individually each take $O(N)$ time, leading to an overall time complexity of $O(N)$.** |
| Space | **O(N) — Because Java strings are immutable, a `StringBuilder` of size up to $N$ is required to perform in-place character swaps.** |

#### 💻 Solution

[View the complete Java solution →](./solution-2.java)

#### 🎯 Key Takeaway

The double reversal strategy (reverse full string, then reverse sub-segments) is a classic algorithmic pattern that enables in-place array manipulation without using external memory for storing words.


---

## 🎯 Key Takeaway

This repository currently contains 2 unique approaches for this problem. Comparing them makes the trade-off between their time, space, and implementation ideas easier to see.

---

## 🔗 Useful Links

- [LeetCode Problem](https://leetcode.com/problems/reverse-words-in-a-string/)
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
