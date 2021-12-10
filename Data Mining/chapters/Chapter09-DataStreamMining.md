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
- Application example
  - Spam filtering


