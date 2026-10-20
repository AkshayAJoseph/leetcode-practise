# DSA Pattern Revision Guide

> **Purpose:** A practical, expandable revision sheet for the LeetCode problems covered so far. It is organized by problem-solving pattern—not by problem number—so the goal is to recognize *why* a technique works and when to reuse it.
>
> **How to revise:** For each problem, first read **Recognition cues** and try to name the pattern before looking at the code. Then explain the core invariant in your own words, trace one example, and only then review the implementation.

---

## Contents

1. [Pattern map](#1-pattern-map)
2. [Prefix sums and prefix-state hashing](#2-prefix-sums-and-prefix-state-hashing)
   - [LC 303 — Range Sum Query: Immutable](#lc-303--range-sum-query-immutable)
   - [LC 525 — Contiguous Array](#lc-525--contiguous-array)
   - [LC 560 — Subarray Sum Equals K](#lc-560--subarray-sum-equals-k)
3. [Two pointers](#3-two-pointers)
   - [LC 167 — Two Sum II](#lc-167--two-sum-ii-input-array-is-sorted)
   - [LC 15 — 3Sum](#lc-15--3sum)
   - [LC 11 — Container With Most Water](#lc-11--container-with-most-water)
4. [Sliding window](#4-sliding-window)
   - [LC 643 — Maximum Average Subarray I](#lc-643--maximum-average-subarray-i)
   - [LC 3 — Longest Substring Without Repeating Characters](#lc-3--longest-substring-without-repeating-characters)
   - [LC 76 — Minimum Window Substring](#lc-76--minimum-window-substring)
5. [Heaps and top-K problems](#5-heaps-and-top-k-problems)
   - [LC 215 — Kth Largest Element in an Array](#lc-215--kth-largest-element-in-an-array)
   - [LC 347 — Top K Frequent Elements](#lc-347--top-k-frequent-elements)
   - [LC 373 — Find K Pairs With Smallest Sums](#lc-373--find-k-pairs-with-smallest-sums)
6. [Intervals and greedy scheduling](#6-intervals-and-greedy-scheduling)
   - [LC 56 — Merge Intervals](#lc-56--merge-intervals)
   - [LC 57 — Insert Interval](#lc-57--insert-interval)
   - [LC 435 — Non-overlapping Intervals](#lc-435--non-overlapping-intervals)
7. [Monotonic stacks](#7-monotonic-stacks)
   - [LC 496 — Next Greater Element I](#lc-496--next-greater-element-i)
   - [LC 739 — Daily Temperatures](#lc-739--daily-temperatures)
   - [LC 84 — Largest Rectangle in Histogram](#lc-84--largest-rectangle-in-histogram)
8. [Binary search and sorted-matrix search](#8-binary-search-and-sorted-matrix-search)
   - [LC 33 — Search in Rotated Sorted Array](#lc-33--search-in-rotated-sorted-array)
   - [LC 153 — Find Minimum in Rotated Sorted Array](#lc-153--find-minimum-in-rotated-sorted-array)
   - [LC 240 — Search a 2D Matrix II](#lc-240--search-a-2d-matrix-ii)
9. [Linked-list pointer manipulation](#9-linked-list-pointer-manipulation)
   - [LC 206 — Reverse Linked List](#lc-206--reverse-linked-list)
   - [LC 92 — Reverse Linked List II](#lc-92--reverse-linked-list-ii)
   - [LC 24 — Swap Nodes in Pairs](#lc-24--swap-nodes-in-pairs)
10. [Fast/slow pointers and cycles](#10-fastslow-pointers-and-cycles)
    - [LC 141 — Linked List Cycle](#lc-141--linked-list-cycle)
    - [LC 202 — Happy Number](#lc-202--happy-number)
    - [LC 287 — Find the Duplicate Number](#lc-287--find-the-duplicate-number)
11. [Cross-problem identification and critical-thinking checklist](#11-cross-problem-identification-and-critical-thinking-checklist)
12. [Reusable template for future problems](#12-reusable-template-for-future-problems)

---

## 1. Pattern map

| Pattern | Typical signal in a problem | Main idea | Problems covered |
|---|---|---|---|
| Prefix sum | Many range-sum queries or contiguous-subarray conditions | Store information about everything before each position | 303, 525, 560 |
| Two pointers | Sorted input, pairs/triplets, or a trade-off between two ends | Move a pointer only when the current state tells you which side cannot help | 167, 15, 11 |
| Sliding window | A contiguous substring/subarray; need longest, shortest, or best fixed-size segment | Maintain a window and update it incrementally instead of recomputing | 643, 3, 76 |
| Heap / priority queue | Need the smallest/largest next, top K, or only a small frontier of candidates | Keep promising candidates ordered by priority | 215, 347, 373 |
| Intervals / greedy | Ranges, overlaps, scheduling, or minimizing removals | Sort to make local decisions reliable | 56, 57, 435 |
| Monotonic stack | “Next greater/smaller,” wait until a future element qualifies, or rectangle boundaries | Keep unresolved candidates in monotonic order; resolve them when a new value arrives | 496, 739, 84 |
| Binary search / sorted search | Ordered search space or a monotonic condition | Discard a region that cannot contain the answer | 33, 153, 240 |
| Linked-list rewiring | Reverse, swap, or modify nodes without losing the rest of the list | Save the next reference before overwriting a link; use a dummy node when the head may change | 206, 92, 24 |
| Fast/slow pointers | Detect cycles, repeated states, or a duplicate under special constraints | Move through a deterministic sequence at different speeds | 141, 202, 287 |

### The recognition question to ask first

Before coding, ask: **What structure does the input give me, and what work is being repeated?**

- If you keep adding the same range again and again, consider **prefix sums**.
- If values are sorted or one side can be ruled out, consider **two pointers** or **binary search**.
- If the target is a contiguous segment, consider **sliding window**; if the condition is about sums that can be negative or arbitrary, a prefix-sum/hash-map method may be more suitable.
- If you only need the next best candidate, do not necessarily sort everything—consider a **heap**.
- If order and overlap are central, sort **intervals** and identify what decision becomes easy afterward.
- If an element must wait for a future element to resolve it, consider a **monotonic stack**.
- If changing links, focus on references, not values.
- If following a deterministic “next state” creates a cycle, consider **fast/slow pointers**.

---

## 2. Prefix sums and prefix-state hashing

### Shared idea

A prefix sum stores the sum of all values before or up to a position. This lets us replace repeated work over a segment with a subtraction. A related idea is to track a **prefix state** (such as the difference between the number of 1s and 0s) and use a hash map to remember where each state occurred.

A useful general identity is:

\[
\text{sum}(l\ldots r)=P[r+1]-P[l]
\]

where `P[i]` is the sum of the first `i` elements. Keeping `P[0] = 0` avoids special cases when a range starts at index 0.

### LC 303 — Range Sum Query: Immutable

**Recognition cues**
- The array does not change.
- The same object must answer many range-sum queries.
- Re-summing every requested range would repeat work.

**Core reasoning**
1. Precompute prefix sums once.
2. `prefix[i]` represents the sum of `nums[0:i]`—the first `i` elements, not the element at index `i`.
3. The sum from `left` through `right`, inclusive, is `prefix[right + 1] - prefix[left]`.

**Python quick reference**

```python
class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

**Why the extra zero matters:** If `left == 0`, then `prefix[left]` is `prefix[0] == 0`. No separate case is required.

**Complexity:** Build `O(n)` time and `O(n)` space; each query `O(1)` time.

**Generalize it when** you see many range-sum queries on static data. Similar prefix arrays can store counts, XORs, or other cumulative quantities, provided a range result can be recovered from two prefix states.

**Common trap:** Mixing inclusive ranges with half-open prefixes. Here, the range includes `right`, so the prefix endpoint is `right + 1`.

### LC 525 — Contiguous Array

**Recognition cues**
- Find the longest contiguous subarray with equal numbers of 0s and 1s.
- The condition depends on a balance, not on the exact elements.
- Replacing each 0 with `-1` and each 1 with `+1` makes a valid subarray sum to zero.

**Core reasoning**
1. Treat `0` as `-1` and `1` as `+1`.
2. Keep a running balance.
3. If the same balance occurs at indices `j` and `i`, the values between them sum to zero. The subarray is `j + 1` through `i`, with length `i - j`.
4. To maximize the length, store the **first/earliest** index at which each balance appears.
5. Seed balance `0` at index `-1`, which handles valid subarrays beginning at index 0.

**Python quick reference**

```python
class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        first_index = {0: -1}
        balance = 0
        best = 0

        for i, num in enumerate(nums):
            balance += 1 if num == 1 else -1

            if balance in first_index:
                best = max(best, i - first_index[balance])
            else:
                first_index[balance] = i

        return best
```

**Why store the earliest index?** For a repeated balance, the earliest occurrence creates the longest possible interval ending at the current index. Replacing it with a later occurrence would lose potential length.

**Complexity:** `O(n)` time and `O(n)` space.

**Generalize it when** a problem asks for the longest subarray whose transformed sum is zero, or where two categories must appear equally often. For equal counts among more categories, a vector of count differences can serve as the state key.

**Common traps:**
- Using the count of zeros and ones directly when a balance difference is simpler.
- Updating the earliest index after it has already been recorded.
- Forgetting `{0: -1}` and thereby missing a valid prefix starting at index 0.

### LC 560 — Subarray Sum Equals K

**Recognition cues**
- Count how many contiguous subarrays sum to `k`.
- Values may be negative, zero, or positive, so a simple sliding window cannot reliably decide which side to shrink.
- Need to count many possible start positions efficiently.

**Core reasoning**
1. Let `prefix` be the sum up to the current element.
2. A subarray ending here sums to `k` if an earlier prefix sum equals `prefix - k`.
3. Keep a dictionary counting how many times each prefix sum has appeared.
4. Add `frequency[prefix - k]` to the answer, then record the current prefix.
5. Seed the frequency map with `{0: 1}` so a subarray whose sum is exactly `k` from index 0 is counted.

**Python quick reference**

```python
class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        prefix_count = {0: 1}
        prefix = 0
        count = 0

        for num in nums:
            prefix += num
            count += prefix_count.get(prefix - k, 0)
            prefix_count[prefix] = prefix_count.get(prefix, 0) + 1

        return count
```

**Important order:** Query `prefix - k` before incrementing the current prefix count. The map should represent earlier prefixes, so the current element is not accidentally paired with itself.

**Complexity:** `O(n)` expected time and `O(n)` space.

**Generalize it when** you need to count subarrays with a target sum, count of some transformed quantity, or differences between prefix values. The map stores **frequency** here because every earlier matching prefix represents a distinct subarray.

**Compare LC 525 and LC 560:** Both use prefix states. LC 525 stores the *earliest index* to maximize a length; LC 560 stores the *frequency* to count all matches. Pick the map value according to what the question asks you to optimize/count.

**Common trap:** Assuming a sliding window works for every subarray sum. Negative numbers can make the sum move up or down unpredictably when a pointer moves.

---

## 3. Two pointers

### Shared idea

Two pointers are useful when the input order or a mathematical constraint lets you rule out candidates without checking them all. Always be able to explain **why moving this pointer cannot discard a better answer**. If you cannot justify the movement, it may be a guess rather than a correct algorithm.

### LC 167 — Two Sum II (Input Array Is Sorted)

**Recognition cues**
- The array is sorted.
- Find two values that sum to a target.
- Returning indices is required, but checking all pairs would be `O(n²)`.

**Core reasoning**
1. Start `left` at the smallest value and `right` at the largest.
2. If the sum is too small, move `left` rightward: the current left value paired with any value at or left of `right` cannot increase the sum enough.
3. If the sum is too large, move `right` leftward: the current right value is too large with the current left and will not become more useful paired with even smaller left candidates.
4. Stop when the sum matches.

**Python quick reference**

```python
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left, right = 0, len(numbers) - 1

        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]
            if total < target:
                left += 1
            else:
                right -= 1

        return []
```

**Complexity:** `O(n)` time, `O(1)` extra space.

**Generalize it when** sorted data asks for a pair satisfying a sum or comparison. It can also help with deduplication, partitioning, and comparing values from both ends.

**Common traps:**
- Moving both pointers after an unsuccessful comparison, which can skip the answer.
- Forgetting the problem asks for **1-based** indices.
- Using the same pointer twice; the pair must use two positions.

### LC 15 — 3Sum

**Recognition cues**
- Find triplets whose sum is zero (or a target).
- Return unique triplets, not merely one index combination.
- Three nested loops would usually be too slow.

**Core reasoning**
1. Sort the array. Now sums can be adjusted with two pointers, and duplicates become adjacent.
2. Fix an outer index `i`; the remaining task is a two-sum search for `-nums[i]` in the suffix.
3. Use `left = i + 1` and `right = n - 1`.
4. If the sum is too small, increment `left`; if too large, decrement `right`.
5. When a triplet matches, record the values and move both pointers, skipping duplicate values so the same triplet is not emitted again.
6. Skip duplicate outer values too.

**Python quick reference**

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

        return result
```

**Complexity:** `O(n²)` time after sorting; sorting costs `O(n log n)`. Extra working space depends on the sorting implementation; the result list is not counted as auxiliary space.

**Generalize it when** a triplet condition can be reduced to a pair condition after fixing one value. The same structure appears in k-sum problems, though higher values of `k` need additional recursion or loops.

**Common traps:**
- Skipping duplicates only after a match, but not skipping repeated `nums[i]` values.
- Forgetting sorting changes the original index order; this problem asks for triplet values, so that is fine.
- Moving only one pointer after a match without reasoning through duplicates and remaining candidates.

### LC 11 — Container With Most Water

**Recognition cues**
- Two vertical lines define a container.
- Area is width multiplied by the shorter line's height.
- The endpoints start far apart; the challenge is deciding which side to move.

**Core reasoning**
1. Compute `area = min(height[left], height[right]) * (right - left)`.
2. The shorter wall limits the current area.
3. Move the pointer at the **shorter wall** inward. The width must decrease either way; keeping the shorter wall and moving the taller one cannot create a larger height limit than the shorter wall already provides.
4. Repeat while the pointers have not met.

**Python quick reference**

```python
class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            best = max(best, area)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return best
```

**Complexity:** `O(n)` time and `O(1)` extra space.

**Generalize it when** a problem has two endpoints and a score constrained by the weaker/smaller endpoint, while moving inward reduces another quantity such as distance or width.

**Critical logic check:** Never say merely “move the smaller pointer because it works.” Explain the proof: moving the taller side while the shorter side stays fixed only reduces width and cannot raise the limiting height above the shorter side's current height.

---

## 4. Sliding window

### Shared idea

A sliding window represents a contiguous range `[left, right]`. Instead of recomputing each range from scratch, update the state when the window expands or contracts. The most important distinction is between **fixed-size** and **variable-size** windows.

- **Fixed-size:** the window always contains `k` elements. Add the incoming value and remove the outgoing value.
- **Variable-size:** expand to include more data, then shrink when a condition is violated—or, for minimum-window problems, shrink while a valid window can still be made smaller.

Sliding window is not automatically suitable for every subarray problem. It is easiest when adding/removing elements changes the condition in a predictable way. Negative values often break sum-based “expand if too small, shrink if too large” logic.

### LC 643 — Maximum Average Subarray I

**Recognition cues**
- Find the maximum average among all contiguous subarrays of exactly `k` elements.
- Every candidate has the same length, so maximizing average is equivalent to maximizing sum.

**Core reasoning**
1. Calculate the sum of the first `k` elements.
2. Slide one position at a time: subtract the element leaving the window and add the element entering it.
3. Track the maximum window sum.
4. Divide by `k` at the end.

**Python quick reference**

```python
class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        window_sum = sum(nums[:k])
        best_sum = window_sum

        for right in range(k, len(nums)):
            window_sum += nums[right] - nums[right - k]
            best_sum = max(best_sum, window_sum)

        return best_sum / k
```

**Complexity:** `O(n)` time and `O(1)` extra space.

**Generalize it when** the segment length is fixed: rolling sums, maximum/minimum averages, counts of conditions in windows, and many fixed-length string problems.

**Common trap:** Re-summing every window. That repeats up to `k` operations per candidate; the rolling update needs constant work per slide.

### LC 3 — Longest Substring Without Repeating Characters

**Recognition cues**
- The answer is a contiguous substring.
- It must satisfy a uniqueness constraint.
- You need the longest valid range, and duplicate characters tell you when the current window must be adjusted.

**Core reasoning**
1. Maintain `left` and scan with `right`.
2. Track the most recent index of each character.
3. If the current character was seen inside the current window, move `left` to one position after that occurrence.
4. Use `max(left, last_seen[ch] + 1)` so `left` never moves backward.
5. Update the longest length after ensuring the window is valid.

**Python quick reference — last-seen map**

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        best = 0

        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1

            last_seen[ch] = right
            best = max(best, right - left + 1)

        return best
```

**Complexity:** `O(n)` expected time and `O(min(n, alphabet size))` map space.

**Alternative:** A set-based window also works: while a repeated character exists in the set, remove characters from the left and advance `left`.

**Generalize it when** a longest contiguous string/subarray must maintain a constraint that can be restored by moving the left boundary forward.

**Common traps:**
- Moving `left` backward to a stale previous occurrence.
- Updating the best length before restoring validity.
- Confusing a substring (contiguous) with a subsequence (not necessarily contiguous).

### LC 76 — Minimum Window Substring

**Recognition cues**
- Find the **smallest** substring containing all required characters, including repeated required characters.
- The substring must be contiguous.
- Need to track character multiplicities, not just whether each character appears once.

**Core reasoning**
1. `need` stores required counts; `window` stores counts in the current window.
2. Expand `right`, updating the count for the incoming character.
3. Track how many distinct required characters have met their required frequency (`formed`).
4. Once `formed == required`, the window is valid. Record it if it is the best so far.
5. Shrink from the left while the window remains valid. When a required character drops below its needed frequency, it is no longer valid and expansion must resume.
6. If no valid window was found, return an empty string.

**Python quick reference**

```python
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""

        need = Counter(t)
        window = {}
        required = len(need)
        formed = 0
        left = 0
        best_len = float("inf")
        best_start = 0

        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1

            if ch in need and window[ch] == need[ch]:
                formed += 1

            while formed == required:
                length = right - left + 1
                if length < best_len:
                    best_len = length
                    best_start = left

                left_ch = s[left]
                window[left_ch] -= 1
                if left_ch in need and window[left_ch] < need[left_ch]:
                    formed -= 1
                left += 1

        if best_len == float("inf"):
            return ""
        return s[best_start:best_start + best_len]
```

**Complexity:** `O(|s| + |t|)` expected time and `O(|s| + |t|)` worst-case auxiliary storage for the character counts (typically bounded by the character set).

**Generalize it when** a minimum valid contiguous window is requested and validity can be represented with counts or a small set of constraints.

**Common traps:**
- Using only a set and losing duplicate counts (`"AABC"` requires two As if the target requires two).
- Treating a character as satisfied whenever it appears, even if its required count is greater than one.
- Forgetting to test/record the current window *before* removing the left character.
- Confusing `formed` (number of fully satisfied distinct character types) with the number of characters currently in the window.

**Longest vs. shortest window:** LC 3 shrinks when the window becomes invalid. LC 76 shrinks while the window is still valid to see how small it can get. That direction follows the objective.

---

## 5. Heaps and top-K problems

### Shared idea

A heap is useful when you repeatedly need the current smallest or largest candidate. It provides efficient access to one extreme without fully sorting all candidates. In Python, `heapq` is a **min-heap**: the smallest item is at index `0`.

Ask yourself:
- Do I need all items sorted, or only the best `k`?
- Can I generate candidates gradually instead of generating every possible candidate?
- Should my heap preserve the largest values or the smallest values seen so far?

### LC 215 — Kth Largest Element in an Array

**Recognition cues**
- Need the kth largest value, not the full sorted array.
- `k` may be much smaller than `n`.
- Keeping only the `k` largest values is enough to determine the answer.

**Core reasoning**
1. Maintain a min-heap of at most `k` elements.
2. Push each number.
3. If the heap grows beyond `k`, pop the smallest. It is not among the largest `k` values seen so far.
4. After processing everything, the heap contains the `k` largest values; its smallest value—the root—is the kth largest overall.

**Python quick reference**

```python
import heapq

class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        heap = []

        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)

        return heap[0]
```

**Complexity:** `O(n log k)` time and `O(k)` extra space.

**Why a min-heap for the kth *largest*?** The heap is deliberately limited to the largest `k` values. Among those, the smallest is exactly the kth largest. The direction of the heap is determined by what you want to discard, not just by the word “largest.”

**Generalize it when** a stream or array asks for top K or bottom K values and full sorting is unnecessary. For the kth smallest, a size-`k` max-heap is the corresponding bounded-heap idea; in Python, negate values or use a different strategy because `heapq` is a min-heap.

**Common traps:**
- Returning the maximum of the size-`k` min-heap instead of the root.
- Letting the heap grow to `n`, which loses the `O(k)` space benefit.
- Assuming “kth largest” requires sorting descending.

### LC 347 — Top K Frequent Elements

**Recognition cues**
- Each distinct number is ranked by its frequency.
- Return only the `k` most frequent values.
- Counting first collapses repeated values into a much smaller set of distinct candidates.

**Core reasoning (the sorting approach we used)**
1. Count each value with a dictionary or `Counter`.
2. Sort the distinct `(value, frequency)` entries by frequency, descending.
3. Return the values from the first `k` entries.

**Python quick reference**

```python
from collections import Counter

class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = Counter(nums)
        ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        return [num for num, _ in ranked[:k]]
```

**Complexity:** Let `m` be the number of distinct values. Counting is `O(n)`; sorting costs `O(m log m)`, for `O(n + m log m)` time and `O(m)` extra space.

**Generalize it when** the task ranks unique items by a score or frequency. A heap can improve the ranking step to `O(m log k)` when `k` is small; bucket sort can be useful when the score range is bounded. The dictionary is the first key move because it creates the frequencies needed to rank.

**Common traps:**
- Sorting the original array by frequency without first counting occurrences.
- Returning `(value, frequency)` tuples when only values are expected.
- Forgetting that sorting descending requires `reverse=True` or a negative sort key.

### LC 373 — Find K Pairs With Smallest Sums

**Recognition cues**
- Two arrays are sorted.
- Need the `k` pairs with the smallest sums.
- Generating all `m × n` pairs may be much more work than returning `k` pairs.

**Core reasoning**
1. Think of a grid of pairs. Each row fixes an index from `nums1`; moving right increases the `nums2` index and therefore cannot decrease the pair sum.
2. Start each selected row with its first pair `(i, 0)`.
3. Store heap entries as `(sum, i, j)` so the smallest sum is popped first. Indices provide the actual values and distinguish equal sums.
4. When `(i, j)` is popped, output that pair and add `(i, j + 1)` if it exists. This exposes the next candidate in that row.
5. Stop after producing `k` pairs or exhausting the heap.

**Python quick reference**

```python
import heapq

class Solution:
    def kSmallestPairs(
        self, nums1: list[int], nums2: list[int], k: int
    ) -> list[list[int]]:
        if not nums1 or not nums2 or k <= 0:
            return []

        heap = []
        for i in range(min(k, len(nums1))):
            heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))

        result = []
        while heap and len(result) < k:
            _, i, j = heapq.heappop(heap)
            result.append([nums1[i], nums2[j]])

            if j + 1 < len(nums2):
                next_j = j + 1
                heapq.heappush(
                    heap,
                    (nums1[i] + nums2[next_j], i, next_j)
                )

        return result
```

**Complexity:** Let `r = min(k, len(nums1))` and `q = min(k, len(nums1) * len(nums2))`, the number of pairs actually output. With the repeated `heappush` initialization shown above, time is `O((r + q) log(r + 1))`; heap space is `O(r)`, excluding the output. This avoids materializing all possible pairs.

**Generalize it when** candidates form a monotonic frontier: when you take one candidate, you can efficiently generate its next neighbor without generating every possibility. This appears in k-way merge and “k smallest combinations” problems.

**Common traps:**
- Building and sorting all pairs, which can require `O(mn)` memory.
- Putting only the sum in the heap and losing the indices needed to recover the pair.
- Pushing every possible neighbor at once, causing duplicate work or an unnecessarily large heap.

---

## 6. Intervals and greedy scheduling

### Shared idea

For interval problems, sorting often turns a global-looking problem into a local scan. Before coding, clarify the interval convention. These solutions treat endpoints as inclusive for overlap: intervals that touch at one endpoint overlap for LC 56/57, while LC 435 allows a next interval to begin exactly when the previous interval ends (`start >= last_end`). Follow the exact problem statement if endpoint semantics differ.

### LC 56 — Merge Intervals

**Recognition cues**
- Intervals may overlap and need to be combined.
- Sorting by start makes potential overlaps appear next to each other.

**Core reasoning**
1. Sort intervals by start time.
2. If the current interval starts at or before the last merged interval ends, merge them.
3. The new end is `max(last_end, current_end)` because the current interval might be completely contained inside the existing one.
4. Otherwise, start a new merged interval.

**Python quick reference**

```python
class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        if not intervals:
            return []

        intervals.sort(key=lambda interval: interval[0])
        merged = [intervals[0][:]]

        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])

        return merged
```

**Complexity:** `O(n log n)` time due to sorting and `O(n)` space for the result. The copy of the first interval avoids unintentionally mutating that nested list in the input.

**Generalize it when** you need to merge time ranges, bookings, numeric spans, or overlapping segments.

**Common traps:**
- Comparing the current start only to the previous input interval rather than the last *merged* endpoint.
- Replacing the merged endpoint with `end` instead of `max(...)`, which can shrink a range when an interval is contained inside another.
- Getting the overlap condition wrong for touching endpoints.

### LC 57 — Insert Interval

**Recognition cues**
- Existing intervals are already sorted and non-overlapping.
- Insert one new interval and return a sorted, merged result.
- Re-sorting everything is possible, but the existing order gives a simpler linear pass.

**Core reasoning: three phases**
1. **Before:** append each interval whose end is strictly before the new interval's start.
2. **Merge:** while an interval overlaps the new interval, widen the new interval using the minimum start and maximum end.
3. **After:** append the merged new interval once, then append every remaining interval.

**Python quick reference**

```python
class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        result = []
        i = 0
        n = len(intervals)
        start, end = newInterval

        while i < n and intervals[i][1] < start:
            result.append(intervals[i])
            i += 1

        while i < n and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1

        result.append([start, end])
        result.extend(intervals[i:])
        return result
```

**Complexity:** `O(n)` time and `O(n)` result space.

**Generalize it when** you are inserting one range into already sorted, non-overlapping ranges. Preserving the input's order can eliminate a sort.

**Common traps:**
- Appending the new interval before all overlaps have been merged.
- Using `<` versus `<=` without checking whether touching endpoints count as overlap.
- Forgetting to append the untouched suffix after the merge phase.

### LC 435 — Non-overlapping Intervals

**Recognition cues**
- Remove the minimum number of intervals so the remaining intervals do not overlap.
- This is equivalent to keeping the maximum number of mutually compatible intervals.
- Choosing intervals with the earliest finishing time leaves the most room for later intervals.

**Core reasoning**
1. Sort by end time (not start time).
2. Keep the first interval, which finishes earliest.
3. For each next interval, if its start is before the end of the last kept interval, it overlaps; remove it.
4. Otherwise, keep it and update the last kept end.
5. Count removals.

**Python quick reference**

```python
class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda interval: interval[1])
        removals = 0
        last_end = float("-inf")

        for start, end in intervals:
            if start < last_end:
                removals += 1
            else:
                last_end = end

        return removals
```

**Complexity:** `O(n log n)` time and `O(1)` auxiliary space apart from the sort implementation.

**Why sort by end?** If two overlapping intervals compete to be kept, the interval that ends earlier leaves at least as much future room as one that ends later. This is a greedy-choice argument—not merely a convenient sort order.

**Generalize it when** scheduling the maximum number of non-overlapping activities or choosing compatible intervals. It is a standard interval-scheduling greedy pattern.

**Common traps:**
- Sorting by start time and assuming that alone gives the optimal number of removals.
- Counting kept intervals when the question asks for removals (the answer is `n - kept`, or count removals directly).
- Treating adjacent intervals as overlapping when the problem permits `start == last_end`.

---

## 7. Monotonic stacks

### Shared idea

A monotonic stack keeps candidate values or indices in increasing or decreasing order. It is especially useful when an item cannot be answered now but can be resolved by a future item. Each element is pushed and popped at most once, which often gives `O(n)` time even though there is a `while` loop inside a `for` loop.

- **Decreasing stack:** useful for next-greater-element problems. A new larger value resolves smaller values waiting on the stack.
- **Increasing stack:** useful for next-smaller boundaries and histogram rectangles. A newly smaller value tells us that a taller bar's right boundary has been found.
- Store **indices** when distance or width is needed; values alone usually are not enough.

### LC 496 — Next Greater Element I

**Recognition cues**
- For each value, find the first larger value to its right in another array.
- A brute-force scan for each value repeats work.
- A value can remain unresolved until a larger number appears.

**Core reasoning**
1. Scan `nums2` left to right with a decreasing stack of values whose next greater element has not been found.
2. When the current number is greater than the stack top, it resolves that top. Pop it and map it to the current number.
3. Continue popping while the current number resolves more waiting values.
4. Push the current number.
5. For each query in `nums1`, return the map value or `-1` if none exists.

**Python quick reference**

```python
class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        stack = []
        next_greater = {}

        for num in nums2:
            while stack and num > stack[-1]:
                next_greater[stack.pop()] = num
            stack.append(num)

        return [next_greater.get(num, -1) for num in nums1]
```

**Complexity:** `O(n + m)` time and `O(n)` extra space, where `n = len(nums2)` and `m = len(nums1)`.

**Generalize it when** the question asks for the next greater/smaller value to the right or left. A monotonic stack is likely useful when a future value “answers” multiple unresolved previous values.

**Common traps:**
- Popping only once; one new value may resolve several stack entries.
- Storing a mapping for the current value before a larger value has been found.
- Assuming every value has a greater value; unanswered values must return `-1`.

### LC 739 — Daily Temperatures

**Recognition cues**
- For each day, find how many positions ahead the next warmer temperature occurs.
- You need the **distance** between indices, not just the future temperature.

**Core reasoning**
1. Store indices of days still waiting for a warmer temperature in a decreasing stack of temperatures.
2. When today's temperature is warmer than the temperature at the stack's top index, pop that earlier index.
3. The waiting time is `current_index - earlier_index`.
4. Initialize the result with zeros; any day never resolved by a warmer day keeps zero.

**Python quick reference**

```python
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        result = [0] * len(temperatures)
        stack = []  # indices; temperatures at these indices decrease

        for i, temp in enumerate(temperatures):
            while stack and temp > temperatures[stack[-1]]:
                prev_i = stack.pop()
                result[prev_i] = i - prev_i
            stack.append(i)

        return result
```

**Complexity:** `O(n)` time and `O(n)` space. Every index is pushed once and popped at most once.

**Generalize it when** each position asks for the distance to the next position satisfying a greater/smaller condition: stock span variants, next warmer day, next larger element, and related boundary problems.

**Common traps:**
- Storing temperatures rather than indices, then being unable to calculate the distance.
- Using `>=` when the problem requires *strictly* warmer temperatures (`>`).
- Returning the future index instead of the difference between indices.

### LC 84 — Largest Rectangle in Histogram

**Recognition cues**
- Each bar's height can form a rectangle across a contiguous range.
- The area is `height × width`.
- For each candidate height, the maximum width is bounded by the nearest shorter bar on the left and right.
- Expanding each bar in both directions is quadratic; a monotonic stack can find boundaries efficiently.

**Core reasoning**
1. Keep indices in a stack whose heights are increasing.
2. When the current bar is shorter than the top bar, the top bar's right boundary has been found.
3. Pop the bar. Its height is the rectangle height. The current index is the exclusive right boundary.
4. If the stack is empty, the rectangle extends from index `0` to `i - 1`, so width is `i`. Otherwise, the new stack top is the previous smaller boundary, so width is `i - stack[-1] - 1`.
5. Process a virtual height `0` after the final bar to flush every remaining bar from the stack.

**Python quick reference**

```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []  # indices of increasing bar heights
        best = 0
        n = len(heights)

        for i in range(n + 1):
            current_height = heights[i] if i < n else 0

            while stack and heights[stack[-1]] > current_height:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                best = max(best, height * width)

            if i < n:
                stack.append(i)

        return best
```

**Complexity:** `O(n)` time and `O(n)` space.

**Why the width formula works:** After popping an index, `i` is the first position to the right that is shorter than the popped bar. The new stack top, if present, is the nearest remaining shorter bar on the left. Bars strictly between those boundaries are the rectangle's width.

**Generalize it when** an answer depends on nearest smaller boundaries or maximal contiguous spans. Related tasks often use the same increasing-stack structure.

**Common traps:**
- Using `i - stack[-1]` instead of `i - stack[-1] - 1` when the stack is nonempty.
- Forgetting the stack-empty case, where width is `i`.
- Forgetting to flush the stack after the final real bar.
- Mixing up stack values and stack indices.

---

## 8. Binary search and sorted-matrix search

### Shared idea

Binary search is not only “look in the middle.” Its correctness comes from maintaining a range in which the answer must still exist and discarding a half based on a reliable property. For each iteration, be able to state **what the comparison proves** and **which region is safe to discard**.

### LC 33 — Search in Rotated Sorted Array

**Recognition cues**
- The array was sorted and then rotated.
- There are no duplicates under the usual LC 33 constraints.
- Ordinary binary search does not work directly because the whole interval is not sorted, but at least one half around the midpoint is sorted.

**Core reasoning**
1. Compute `mid`.
2. If `nums[mid]` is the target, return it.
3. If `nums[left] <= nums[mid]`, the left half is sorted. Check whether the target lies within that half; if so, search left, otherwise search right.
4. Otherwise, the right half is sorted. Check whether the target lies within that half and discard the other.
5. If the target is absent, return `-1`.

**Python quick reference**

```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:  # left half is sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # right half is sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

**Complexity:** `O(log n)` time and `O(1)` extra space.

**Generalize it when** a search space has a sorted portion or monotonic predicate that lets you eliminate half the candidates each step.

**Common traps:**
- Assuming both halves are sorted.
- Getting the range endpoints wrong; the checks above use inclusive `left`/`right` and strict bounds around `mid`.
- Using this exact algorithm when duplicates are allowed without reconsidering the logic; duplicates can make it impossible to identify the sorted half from endpoint comparisons alone.

### LC 153 — Find Minimum in Rotated Sorted Array

**Recognition cues**
- A sorted, unique array has been rotated.
- Need the minimum, not the target's index.
- Comparing the midpoint to one endpoint tells which side contains the rotation boundary.

**Core reasoning**
1. Compare `nums[mid]` with `nums[right]`.
2. If `nums[mid] > nums[right]`, the minimum must be to the right of `mid`; set `left = mid + 1`.
3. Otherwise, the minimum is at `mid` or to its left; set `right = mid`.
4. When `left == right`, that index is the minimum.

**Python quick reference**

```python
class Solution:
    def findMin(self, nums: list[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
```

**Complexity:** `O(log n)` time and `O(1)` extra space.

**Why use `right = mid`, not `mid - 1`?** When `nums[mid] <= nums[right]`, `mid` itself may be the minimum, so it must remain a candidate. This is a common binary-search pattern where the answer is an element inside the current inclusive range.

**Generalize it when** the task asks for a boundary or minimum/maximum in a rotated sorted array or another structured search space.

**Common traps:**
- Using `while left <= right` with update rules designed for `left < right`, causing off-by-one or non-progress errors.
- Discarding `mid` even when it might be the answer.
- Comparing to the left endpoint out of habit; this solution's decision rule is built around `nums[right]`.

### LC 240 — Search a 2D Matrix II

**Recognition cues**
- Every row is sorted left-to-right and every column is sorted top-to-bottom.
- The matrix is not necessarily globally sorted as one flat array.
- Need to search efficiently without checking every cell.

**Core reasoning**
1. Start at the top-right cell.
2. If the current value equals the target, return `True`.
3. If it is too large, every value below it in that column is at least as large, so discard the current column by moving left.
4. If it is too small, every value to its left in that row is no larger, so discard the current row by moving down.
5. If a pointer leaves the matrix, the target is absent.

**Python quick reference**

```python
class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        row, col = 0, len(matrix[0]) - 1

        while row < len(matrix) and col >= 0:
            value = matrix[row][col]
            if value == target:
                return True
            if value > target:
                col -= 1
            else:
                row += 1

        return False
```

**Complexity:** `O(m + n)` time and `O(1)` extra space for an `m × n` matrix.

**Generalize it when** a 2D grid is sorted in both directions and you can choose a corner where each comparison safely eliminates a full row or column.

**Common traps:**
- Starting from a corner where both movement directions do not produce a clear elimination rule.
- Flattening the matrix and using ordinary binary search when the rows are only individually sorted, not globally ordered.
- Forgetting empty-matrix checks when they are allowed by the interface.

---

## 9. Linked-list pointer manipulation

### Shared idea

A linked-list node stores a reference to the next node. Changing a link can make the rest of the list unreachable if the next reference was not saved first. Before updating pointers, draw a small chain and list what each reference points to.

Useful habits:
- Save `next_node = current.next` before overwriting `current.next`.
- Use a **dummy node** when the real head may change. Then return `dummy.next`, not necessarily the original `head`.
- Separate the pointer to the node *before* a region from the pointer that moves inside the region.
- Trace node references carefully; do not confuse node values with node identities.

### LC 206 — Reverse Linked List

**Recognition cues**
- Reverse all links in a singly linked list.
- Must change each node's `next` reference; changing only values is not the intended operation.

**Core reasoning**
1. Start with `prev = None` and `curr = head`.
2. Save the next node before changing the current link.
3. Point `curr.next` backward to `prev`.
4. Advance both pointers: `prev = curr`, `curr = next_node`.
5. When `curr` becomes `None`, `prev` is the new head.

**Python quick reference**

```python
class Solution:
    def reverseList(self, head):
        prev = None
        curr = head

        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        return prev
```

**Complexity:** `O(n)` time and `O(1)` extra space.

**Generalize it when** the task needs in-place singly linked-list reversal. The same pointer invariant is the foundation for reversing a sublist or sections of a list.

**Common traps:**
- Reversing `curr.next` before saving the next node, losing access to the unreversed suffix.
- Returning the original head, which becomes the tail after reversal.
- Advancing `curr` through its reversed `next` pointer rather than through the saved `next_node`.

### LC 92 — Reverse Linked List II

**Recognition cues**
- Reverse only positions `left` through `right` (1-indexed).
- The sublist may start at the head, so the head itself may change.
- The nodes before and after the reversed section must remain attached.

**Core reasoning: head insertion**
1. Create a dummy node pointing to `head`; this handles `left == 1` uniformly.
2. Move `prev` to the node immediately before position `left`.
3. Set `curr = prev.next`, the first node of the region.
4. Repeat `right - left` times: remove `curr.next` from its current spot and insert it immediately after `prev`.
5. Return `dummy.next` because the true head may have changed.

**Python quick reference**

```python
class Solution:
    def reverseBetween(self, head, left: int, right: int):
        if not head or left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next

        curr = prev.next
        for _ in range(right - left):
            next_node = curr.next
            curr.next = next_node.next
            next_node.next = prev.next
            prev.next = next_node

        return dummy.next
```

**Complexity:** `O(n)` time in the worst case and `O(1)` extra space.

**Generalize it when** a contiguous linked-list segment must be rearranged without copying nodes. Head insertion is especially useful when reversing a range in place.

**Pointer interpretation**
- `prev`: stays just before the section being reversed.
- `curr`: remains the first node of that section during head insertion; it gradually moves toward the tail of the reversed section.
- `next_node`: the node being lifted and inserted at the front of the section.

**Common traps:**
- Returning `head` instead of `dummy.next`.
- Moving `prev` during the head-insertion loop; it must remain before the sublist.
- Losing `next_node.next` or changing links in an unsafe order.
- Confusing position numbers (1-indexed) with Python's 0-indexed iterations.

### LC 24 — Swap Nodes in Pairs

**Recognition cues**
- Swap every adjacent pair in a linked list.
- The nodes themselves should be rearranged, not merely their values.
- A pairwise local rewiring can be repeated until fewer than two nodes remain.

**Core reasoning**
1. Use a dummy node before the head.
2. `prev` points to the node before the pair; `first = prev.next`, `second = first.next`.
3. Link `first` to the node after `second`.
4. Link `second` to `first`, then link `prev` to `second`.
5. Set `prev = first`, which is now the tail of the swapped pair, and process the next pair.

**Python quick reference**

```python
class Solution:
    def swapPairs(self, head):
        dummy = ListNode(0, head)
        prev = dummy

        while prev.next and prev.next.next:
            first = prev.next
            second = first.next

            first.next = second.next
            second.next = first
            prev.next = second

            prev = first

        return dummy.next
```

**Complexity:** `O(n)` time and `O(1)` extra space.

**Generalize it when** adjacent nodes or fixed-size groups must be rearranged. The key skill is defining the node before the region and reconnecting the region's entry and exit.

**Common traps:**
- Reversing link updates so a required reference is lost.
- Advancing `prev` to `second` instead of `first` after swapping; `first` is now at the end of the pair.
- Failing on an odd-length list because the loop must confirm that two nodes are available.

---

## 10. Fast/slow pointers and cycles

### Shared idea

Sometimes an input can be treated as a deterministic sequence: every state leads to exactly one next state. Such a sequence either reaches a terminal state or eventually repeats, creating a cycle. Fast/slow pointers detect cycles without storing every visited state.

- `slow` advances one step.
- `fast` advances two steps.
- If there is a cycle, they eventually meet inside it.
- A meeting proves a cycle exists; the **location of the meeting is not necessarily the cycle entrance**.

### LC 141 — Linked List Cycle

**Recognition cues**
- Determine whether a linked list loops back instead of reaching `None`.
- A visited-node set works but needs `O(n)` space.
- The list has a one-next-reference structure suitable for Floyd's algorithm.

**Core reasoning**
1. Start slow and fast at the head.
2. While `fast` and `fast.next` exist, move slow by one link and fast by two.
3. If they become the same node, a cycle exists.
4. If fast reaches `None`, there is no cycle.

**Python quick reference**

```python
class Solution:
    def hasCycle(self, head) -> bool:
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True

        return False
```

**Complexity:** `O(n)` time and `O(1)` extra space.

**Generalize it when** a list or pointer structure may contain a cycle and a constant-space answer is preferred.

**Common traps:**
- Checking `fast.next.next` without first ensuring `fast` and `fast.next` exist.
- Comparing node values rather than node identity. Two separate nodes can hold the same value; cycle detection asks whether pointers refer to the same node.

### LC 202 — Happy Number

**Recognition cues**
- Repeatedly transform a number by replacing it with the sum of the squares of its digits.
- Return `True` if the sequence reaches `1`; otherwise it falls into a repeating cycle.
- The problem is a cycle-detection problem over numbers, not necessarily a linked-list data structure.

**Core reasoning**
1. Define `next_number(n)` to calculate the sum of squared digits.
2. Each number has exactly one next number, so the sequence is deterministic.
3. A set can detect repeated states; Floyd's algorithm can do the same with constant extra space.

**Python quick reference — Floyd's cycle detection**

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def next_number(value: int) -> int:
            total = 0
            while value > 0:
                digit = value % 10
                total += digit * digit
                value //= 10
            return total

        slow = n
        fast = next_number(n)

        while fast != 1 and slow != fast:
            slow = next_number(slow)
            fast = next_number(next_number(fast))

        return fast == 1
```

**Complexity:** `O(d)` per transformation for `d` digits; total time depends on the number of states visited before reaching `1` or repeating. Auxiliary space is `O(1)` for Floyd's method. A set-based approach is often simpler to understand but uses space proportional to the number of visited states.

**Generalize it when** a repeated operation maps each state to exactly one next state and the question asks whether it reaches a destination or repeats.

**Common traps:**
- Using a list to detect repeats and repeatedly scanning it (`x in list` is linear), which may make the overall approach unnecessarily slow.
- Forgetting that repetition is the proof of a loop when `1` is never reached.
- Misreading `//` as ordinary division: `value //= 10` removes the last digit; `% 10` extracts it.

### LC 287 — Find the Duplicate Number

**Recognition cues**
- There are `n + 1` values, each in the range `1..n`.
- A value repeats, and the constraints require no modification of the array and constant extra space.
- The values can be interpreted as links: from index `i`, go to index `nums[i]`.

**Core reasoning: Floyd's algorithm in two phases**

**Phase 1 — find a meeting inside the cycle**
1. Treat each index as a node whose next node is `nums[index]`.
2. Start slow and fast at `nums[0]`.
3. Repeatedly advance slow one step and fast two steps until they meet.
4. This proves the pointer sequence has a cycle—but the meeting value is **not guaranteed to be the duplicate**.

**Phase 2 — find the cycle entrance**
1. Reset one pointer to `nums[0]`, the start of the sequence.
2. Leave the other at the phase-one meeting point.
3. Advance both one step at a time. They meet at the cycle entrance, which corresponds to the duplicate value.

**Python quick reference**

```python
class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow = fast = nums[0]

        # Phase 1: detect a cycle and find a meeting point.
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        # Phase 2: locate the entrance to the cycle.
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow
```

**Complexity:** `O(n)` time and `O(1)` extra space; the array is not modified.

**Why phase 2 is necessary:** Phase 1 finds a point *somewhere inside* the cycle. It does not identify the entrance in general. For example, with `nums = [2, 5, 9, 6, 9, 3, 8, 9, 7, 1]`, phase 1 meets at `7` while the duplicate is `9`; phase 2 moves both pointers until they meet at `9`.

**Generalize it when** the input's next-state rule makes a functional graph and the problem requires detecting its cycle entrance without a visited set. Always verify that the input constraints make the pointer interpretation valid.

**Common traps:**
- Returning the phase-one meeting point directly.
- Replacing phase 2 with a search for the value that appears twice; that can violate the required space or mutation constraints.
- Confusing a pointer's value with the array index used to look up its next value.
- Writing `fast = nums[fast]` instead of `fast = nums[nums[fast]]` in phase 1.

---

## 11. Cross-problem identification and critical-thinking checklist

### A. Convert the wording into a structure

Underline the type of object the answer is about:

- **Range/subarray/substring:** Is it contiguous? Is the size fixed? Is the objective longest, shortest, maximum sum, or count?
- **Pair/triplet:** Is the array sorted? Can sorting help? What pointer movement can be proved safe?
- **Top K / kth:** Do I need a complete ordering, or only the first `k` candidates? Can I discard candidates permanently?
- **Intervals:** Are they sorted? Do they overlap? Is the goal to combine ranges or keep a maximum compatible set?
- **Next greater/smaller:** Is there a future element that resolves a waiting element?
- **Linked list:** Am I changing nodes or just their values? Can the head change? What links must remain reachable?
- **Repeated state / cycle:** Does every state have exactly one next state? What must I return: whether a cycle exists, the entrance, or the eventual result?

### B. Define the invariant before writing the loop

An invariant is something that stays true after each iteration. A few examples from this guide:

- Prefix sum: `prefix[i]` stores the sum of the first `i` values.
- LC 560: `prefix_count` contains frequencies of earlier prefix sums only.
- Two pointers: every discarded candidate has been ruled out by the sorted order or the score's mathematical constraint.
- Sliding window: the maintained window and count structures accurately represent `s[left:right + 1]`.
- Size-k heap: after processing a prefix of the input, the heap contains the largest `k` values seen so far (or fewer if not enough values were seen).
- Merge intervals: `merged[-1]` is the result of merging all processed intervals that belong to the latest connected range.
- Monotonic stack: indices still on the stack are unresolved candidates and obey the chosen order.
- Linked-list reversal: `prev` is the reversed portion; `curr` is the start of the unprocessed portion.
- Floyd: a meeting means a cycle exists; it does not automatically mean the meeting point is the cycle entrance.

If you cannot say what a variable means *at every iteration*, pause and define it before coding.

### C. Explain each pointer or state update

For every line that changes a pointer, index, count, or boundary, ask:

1. **What does this variable represent before the update?**
2. **What will it represent afterward?**
3. **Why is this update safe?**
4. **What candidate or state is being discarded, and why cannot it be the answer?**
5. **Could this update skip an answer, move backward, or cause an infinite loop?**

This habit catches many common errors: moving the wrong two-pointer side, shrinking a valid minimum window too late, using an index where a value is required, and breaking a linked-list chain.

### D. Pick data structures by the information the question needs

| The question asks for… | Store in a map/structure… | Example |
|---|---|---|
| Earliest occurrence to maximize a distance | First index | LC 525 |
| Number of earlier states matching a condition | Frequency | LC 560 |
| Most recent index to jump a window forward | Last-seen index | LC 3 |
| Current character counts and constraint satisfaction | Frequency map + validity counter | LC 76 |
| Only the best `k` values | Bounded heap | LC 215 |
| Next greater value | Value-to-answer map + monotonic stack | LC 496 |
| Waiting positions whose distance is needed | Stack of indices | LC 739 |
| Nearest smaller boundaries | Monotonic stack of indices | LC 84 |
| A node before a possibly changing head/segment | Dummy node | LC 92, LC 24 |
| Whether a state repeats without extra storage | Fast/slow pointers | LC 141, LC 202, LC 287 |

A good data structure is not just a tool that works; it stores exactly the information needed to answer the query efficiently.

### E. Test boundaries deliberately

Before trusting a solution, walk through these cases when applicable:

- Empty or one-element input.
- The answer begins at index 0 or reaches the final index.
- No valid answer exists.
- Every item is the same / all values are distinct.
- Duplicates appear consecutively and non-consecutively.
- The interval is fully contained within another interval.
- The new interval overlaps none, one, or several existing intervals.
- The linked-list change includes the head or tail.
- The cycle entrance is not the first slow/fast meeting point.
- The window becomes valid at the first possible moment or becomes invalid immediately after shrinking.

Do not only test the happy path. A counterexample is a fast way to discover a hidden assumption.

### F. Complexity: count the work, not just the loops

- A nested loop is not always quadratic if each item is pushed/popped only a constant number of times (monotonic stacks are the classic example).
- A sort usually costs `O(n log n)` and may dominate the scan that follows.
- A hash-map lookup is `O(1)` on average, not a strict worst-case guarantee.
- For top-K, compare `O(n log k)` with sorting all `n` items in `O(n log n)`.
- Distinguish auxiliary space from output space when a result list is required.
- A technique may trade memory for speed: prefix sums and hash maps use memory to avoid repeated scans.

### G. A practical decision path

1. **Is the answer a contiguous range?** Try prefix sums or sliding window. Use prefix-state hashing for target-sum/count conditions that may include negative values; use a window when the condition supports safe incremental expansion/contraction.
2. **Is the input sorted or partially sorted?** Try binary search or two pointers. Write down the property that makes discarding a region safe.
3. **Is only the top/bottom `k` needed?** Consider a bounded heap.
4. **Are ranges overlapping or being scheduled?** Sort intervals—by start for merging, by end for maximum compatible selection.
5. **Does a future item resolve earlier items?** Consider a monotonic stack.
6. **Are links being modified?** Draw node references and use a dummy node where the head can change.
7. **Does a deterministic next-state rule repeat?** Consider cycle detection; clarify whether the answer is a meeting point, cycle entrance, or destination state.

---

## 12. Reusable template for future problems

Copy this section into the guide whenever a new problem is solved. Keep the recognition cues and invariant concise enough to scan during revision.

````markdown
### LC XXX — Problem Title

**Pattern:** <!-- e.g. variable sliding window, monotonic stack -->

**Recognition cues**
- <!-- What wording, constraint, or input structure suggests the pattern? -->

**Core reasoning**
1. <!-- First transformation or initialization -->
2. <!-- Main invariant -->
3. <!-- How the state changes and why it is safe -->
4. <!-- How the answer is obtained -->

**Python quick reference**

```python
# Add the accepted LeetCode solution here.
```

**Complexity:** `O(...)` time, `O(...)` auxiliary space.

**Generalize it when** <!-- What other problem shapes share this structure? -->

**Common traps**
- <!-- Boundary, off-by-one, data-structure, or proof mistake -->

**Critical logic check:** <!-- One sentence explaining why the key operation is safe. -->
```
````

### Recommended update workflow

When adding a new problem:

1. Add it under the existing pattern heading if it uses a known pattern; otherwise create a new pattern section and update the contents and pattern map.
2. Record the **reason** for choosing the pattern, not just the algorithm name.
3. Include one invariant that remains true through the loop.
4. Add one counterexample or boundary case that would break a tempting but incorrect approach.
5. Keep the code consistent with the assumptions and constraints of the exact LeetCode problem.

---

## Final reminder

**Pattern recognition is the beginning, not the proof.** A familiar-looking problem may use a familiar technique, but the solution is correct only when each pointer movement, map update, heap operation, or link change is justified by the problem's constraints. Practice stating that justification out loud before you code.
