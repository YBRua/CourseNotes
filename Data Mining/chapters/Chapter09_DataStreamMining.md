# Mining Data Streams

## Data Streams

- In many data mining scenarios, we do not know the entire data set in advance
  - Instead, the data come in streams and change with time
  - Can think of data as **infinite** and **non-stationary**

### Stream Model

- Input elements enter at a rate, at one or more input ports
  - Elements of the stream is called **tuples**
- The system **cannot** sotre the entire stream

#### SGD as Stream Algorithm

- SGD is a type of stream algorithm
- In machine learning this is referred to as **online learning**

## Sampling from Data Stream

- Two different problems
  - Sampling a fixed proportion of elements in a stream
  - Maintaining a random samples of fixed size
    - such that for all time steps, each elements that have appeared have the same probability to be sampled

### Sampling a Fixed Proportion

The naive approach is to retain an element with probability $p$ if we want to keep $p$ of the total stream

Problem

- Duplicated items exist
  - e.g. in search engines, users may issue similar or identical queries
  - Randomly sampling **queries** may lead to incorrect results
  - Instead, we randomly sample **users**

#### General Sampling Solution

Assume we are sampling a stream of tuples with keys, to get a sample of $a/b$ fraction of the stream,

- Hash each tuple's key uniformly into $b$ buckets
- Pick the tuple if its hash value is at most $a$

### Sampling a Fixed Size

We maintain a random sample $S$ of exactly $s$ tuples

- Do not know elements in advance
- Suppose at time $n$ we have seen $n$ items, we want the probability that one item is in $S$ to be $n/s$
- The naive solution would be to store all $n$ seen elements at time $n$
  - Impractical because we may not have enough memory or other resources

#### Reservoir Sampling

- Store all first $s$ elements of the stream in $S$
- Assume the $n$-th element arrives
  - Keep the element with probability $s/n$
  - If we keep the element, it replaces one of the $s$ elements in $S$ uniformly at random

##### Proof of Correctness

Assume that after $n$ elements, the sample contains each element with probability $s/n$

For each element in $S$, the probability that it is still kept in $S$ at time step $n+1$ is

$$ \left( 1 - \frac{s}{n+1} \right) + \left( \frac{s}{n+1} \right)\left( \frac{s-1}{s} \right) = \frac{n}{n+1} $$

At $n$, the probability that it is in $S$ is

$$ \frac{s}{n} $$

Therefore the final probability that it is in $S$ at $n+1$ is

$$ \frac{n}{n+1}\cdot\frac{s}{n} = \frac{s}{n+1} $$

For the new element, it has $s/(n+1)$ probability to be sampled and put into $S$. So we are done

## Sliding Windows

- Assume we have a very large window size $N$, which cannot be stored in memory or on disk
  - Or we have too many elements and the windowed results cannot fit into memory or disk

Suppose we have a stream of 0's and 1's, we want to know how many 1's are there in the window

- The intuitive solution would be to store the window and maintain the elements in the window
  - But sometimes the window is extremely large
  - So we have to approximate

### DGIM

- Gives an approximation that deviates no more than 50% from the exact value

#### Exponential Windows

Summarize **exponentially increasing** regions of the stream, looking backward

- Drop small regions if they begin at the same point as a larger region
- $O(\log^2N)$ storage consumption
- Easy update

#### DGIM Method

- Instead of summarizing fixed-length blocks, summarize blocks with specific number of 1's
  - Let the number of 1's contained in the block increase exponentially
- Assume each bit in stream has a timestamp starting from 1
  - Can represent the position of a bit in $\log_2N$

##### Buckets

A bucket in the DGIM method is a record consisting of

- The timestamp of its end point
- The number of 1's in the block
- Requirement of buckets
  - Require the number of 1's to be a power of 2
  - Require there exists at most 2 buckets of the same size
    - Merge buckets if necessary
  - Require the buckets cannot overlap
  - Require the size of blocks grows as we move backward along time line

When a new bit comes in, drop the oldest bucket if its endtime is prior to $N$ time units before the current time

- If current bit is 0, then no changes is required
- If current bit is 1, then
  1. Create new bucket of size 1 for current bit
  2. Merge buckets if necessary

To estimate the number of 1's in the most $N$ bits

## Filtering Data Streams

- Problem setting
  - Each element of data stream is a tuple
  - Given a list of keys $S$
  - Determine which tuples of stream are in $S$
  - Assume $S$ is very very large
- Application example
  - Spam filtering
  - Publish-subscribe system

An obvious idea would be to use a hash table and look for collisions, but sometimes $S$ may be too large to be stored in hash table

### Bit Array Filtering

- Create a bit array $B$ of $n$ bits initialized with $0$'s
- Choose a hash function $h$ with range $[0, n)$
- Hash each member of $s\in S$ to one of $n$ buckets, and set that bit to $1$
- Hash each element $a$ of the stream
- Only output $a$ if the hashed value corresponds to $1$

This method may produce **false positives** (due to collision of hashing) but **no false negatives**. If an item hashes to $0$, it cannot be in the filter.

#### Analysis

We analyze the number of false positives. Assume we throw $m$ balls into $n$ bins, what is the probability that a certain bin gets at least one ball? In our scene, balls are hashed values and bins are bits.

$$ p = 1 - \left( 1-\frac{1}{n} \right)^m = 1 - \left( 1-\frac{1}{n} \right)^{n\cdot (m/n)} \to 1 - e^{-m/n} $$

### Bloom Filter

Assume $m$ items, $n$ bits, and $k$ independent hash function $h_1,\dots,h_k$

1. Initialized all bits to be 0
2. Hash each element with $h_i(s)$ and set $B[h_i(s)]=1$ for each $i$ in $k$
3. For input $x$, if $B[h_i(x)] = 1$ for all $i$, then $x$ is in $S$. Otherwise drop $x$

In this case, the probability that we create false positives is $(1 - e^{-km/n})$. The optimal $k$ is $n/m \cdot \ln(2)$.

## Counting Distinct Elements

Suppose elements come from a set of $N$ items. We want to count the number of distinct items seen so far. Again assume we cannot maintain a set of all seen items due to memory restrictions. Buy new RAM!

### Flajolet-Martin Approach

- Pick a hash function $h$ that maps each of the $N$ elements to at least $\log_2N$ bits
- For each element $a$, let $r(a)$ be the number of trailing 0's in $h(a)$
  - i.e. position of the first 1 counting from the least significant bit
- Let $R = \max_a r(a)$, and the estimated number of distinct items is $2^R$

#### Analysis

##### Intuition of FM Approach

Assume $h$ hashes $a$ with equal probability to any of $N$ integers, then $h(a)$ is a sequence of $\log_2N$ bits.

$2^{-r}$ fraction of all $a$'s have a tail of $r$ zeros

- About 50% of $a$'s hash to $***0$
- Aoubt 25% hash to $**00$, etc.
- So it takes about $2^r$ distinct items to produce a trailing of $r$ zeros
  - For example, if we have seen $**00$, then we have probably seen $4$ distinct items

##### Formal Proof

Let $m$ be the number of distinct items seen so far. We will show that the probability of finding a tail or $r$ zeros goes to $1$ if $m\gg 2^r$, and goes to $0$ if $m \ll 2^r$.

- This indicates that $2^R$ will always be a number around $m$

The probability of not seeing a tail of length $r$ among $m$ elements is

$$ (1 - 2^{-r})^m \approx e^{-m\cdot 2^{-r}} $$

Therefore $m$ will have to be around $2^{r}$

- Notice that probability halves when $R \to R+1$, but the estimated number doubles
- Workaround involves using more than one hash functions, and combine different $R_i$'s -- But how?
  - All estimations are powers of 2, taking average may be easily biased to large numbers; taking median always results in another power of 2
- Solution: Average of medians
  - Partition samples into groups
  - Take median of groups
  - Average the medians

## Computing Moments

Can be seen as a generalized version of counting distinct items.

Assume elements are from a set $A$ of $N$ items. Define the $k$-th moment by

$$ \sum_{i \in A}m_i^k $$

- $k = 0$: distinct items
- $k = 1$: Length of the stream
- $k = 2$: A measure of how uneven the distribution is (deviation if the data is zero-meaned)

### AMS Method

> AMS: Abbrevation of 3 names of persons

The AMS method works for all moments and gives an unbiased estimation

For each variable, we store $X_{el}$ and $X_{val}$

- $X_{el}$ corresponds to item $i$
- $X_{val}$ corresponds to the count of item $i$

#### Finite Stream Version

- Assume input stream has length $n$
- We start from any time $t$ uniformly at random
- If the time $t$ has item $i$, we set $X_{el} = i$
- Then we maintain count $c$ of the number of $i$'s in the stream starting from $t$.
  - $c$ will be stored in $X_{val}=c$
- The estimate of second moment is given by $f(X) = S = n(2c - 1)$
- We keep track of multiple $X$ and the final estimate will be

$$ \frac{1}{k}\sum_k f(X_k) $$

- For $k=2$, we use $n(2c-1)$
- For $k=3$, we use $n(3c^2 - 3c + 1)$
- The number is chosen by $\sum_c c^2 - \sum_c (c-1)^2$ so that the expectation of result sum up to $m_i^2$

##### Practical Implementation

- Compute as many $f(X)$ as possible
- Average the result in groups
- Take median of averages

##### Extension to Infinite Streams

Suppose we can only store $k$ $X$'s, we drop some $X$ if we do not have enough space.

If the input stream is infinite, we want to sample a fixed size $k$ s.t. each starting time $t$ is selected with probability $k/n$. This reduces to a fixed-size sampling.

## Counting Itemsets

Given a stream, we want to know which items appear more than a threshold of $m$ times in a window.
