# Frequent Itemsets

## Basic Concepts

- Frequent pattern
  - A pattern (a set of items, subsequences, substructures) that appear frequently in a database
- Itemset
  - A set of one or more items
  - $k$-itemset
    - An itemset of $k$ items
- (Absolute) support/ support count
  - Frequency or occurrence of an itemset
- (Relative) support
  - Fraction of transactions that contains an itemset over all transaction
- An itemset $X$ is frequent if $X$'s support is no less than a certain threshold
- Support
  - Probability that a transaction contains $X$ and $Y$
  - $P(XY)$
- Confidence
  - Conditional probability that a tranaction having $X$ also contains $Y$
  - $P(Y|X)$

### Association Rule Mining

$$P(X\Rightarrow Y) = (P(XY), P(Y|X))$$

1. Find all frequent itemsets
2. Generate strong association rules

The challenge is that there can be a huge number of itemsets that are above the threshold

Observe that if an itemset is frequent, then all of its subsets are also frequent

So we focus on mining closed frequent itemset and maximal frequent itemset

- Closed Frequent Itemset
  - $X$ is frequent and there is no super-itemset $Y \supset X$ with the same support count as $X$
- Maximal Frequent Itemset
  - $X$ is frequent and there is no super-itemset $Y \supset X$ which is also frequent

For example, consider a dataset, with threshold $1$

$$\{\alpha_1 = (a_1,\dots,a_{50}), \alpha_2 = (a_1,\dots, a_{100})\}$$

- Support counts: $\alpha_1 = 2; \alpha_2 = 1$
- Both are closed frequent itemset, but only $\alpha_2$ is the maximal frequent itemset
- We can assert any subset of $\alpha_2$ is frequent, but we cannot make assertions on the exact support count of the subset

## Apriori

> A Candidate Generation-and-Test Approach

- Downward Closure Property
  - Any subset of a frequent itemset must also be frequent

Apriori employs a **level-wise search** to find frequent itemsets bottom up

### Algorithm

1. Scan database to get frequent 1-itemsets $L_1$
   - Retain candidates with support count greather than support threshold
2. Join k-frequent itemsets $L_k$ to generate $L_{k+1}$ candidate itemsets $C_{k+1}'$
   - $C_{k+1}' = L_k \otimes L_k$. Merge itemsets with the same prefix
3. Prune $C_{k+1}'$ to get $C_{k+1}$
   - Remove $(k+1)$-itemset if one of its subsets is not in $L_k$ (by downward closure)
4. Scan the database for the count of each $C_{k+1}$ to obtain $L_{k+1}$
5. Terminate when no larger frequent itemsets can be generated

### Counting Methods

The total number of candidates can be huge, and one transaction may contain many candidates.

- Store candidate itemsets in a hash-tree
  - Each leaf node contains a list of itemsets and their counts
  - Each interior node contains a hash table

### Improving Efficienty of Apriori

#### Reducing Database scans

##### Partitioning

- Any itemset that is potentially frequent (relative support greater than a threshold) must be frequent (relative support in a partition greater than a threshold) in at least on of the partitions

1. Scan partition database and find local frequent patterns
2. Assess the actual support of each candidate to determine the global frequent itemsets

##### Dynamic Itemset Counting

- Adding candidate itemsets at different point
- Once all $k$-itemsubsets of a $(k+1)$-itemset have been scanned, the scan for the $(k+1)$-itemset can begin immediately

##### Hashing

- Hash itemsets into corresponding buckets
- A $k$-itemset whose corresponding hashing bucket count is below `min_sup` cannot be frequent

##### Sampling

1. Select sample $S$ from database
2. Mine frequent itemsets within $S$ to get $L_S$
3. Scan the actual database once to compute the actual frequencies of each itemset in $L_S$
4. If $L_S$ contains all frequent itemsets, stop.
5. Otherwise scan the database again to find possible missing items

## FP-Growth

- Depth-first search
- Avoid explicit candidate generation
- Grow long patterns from short ones using local frequent items

### Frequent-Pattern Growth

1. Scan the database once to find frequent 1-itemsets
2. Sort frequent items in frequency descending order to form an **F-List**
   - A table containing items, frequencies and pointers to nodes in the FP-Tree
3. Scan the database again to construct **FP-Tree**

#### FP-Tree

A compressed representation of the database. It maintains the association information of itemsets.

Consider two transactions `fcamp` and `fcabm`. They share the same prefix `fca`

- `fcamp` creates a list `f:1-c:1-a:1-m:1-p:1`
- `fcabm` follows `f-c-a` path, increases the count of `f`, `c`, `a` and add new nodes `b` and `m`
  - `f:2-c:2-a:2-b:1-m:1`

#### Mining on FP-Tree

1. Start from each frequent 1-pattern
   - **suffix pattern**, usually the last item in F-list
   - because the conditional prefix of a frequent suffix may ocurr more times than the suffix itself
2. Construct the **conditional pattern pase**
   - prefix paths co-ocurring with the suffix
3. Construct **Conditional FP-Tree**
   - The conditional FP-Tree should not contain nodes whose support is below threshold
4. Mine recursively until the tree is empty, or it contains only a single path
   - The single path can immediately generate all frequent items
   - The patterns are all combinations of its sub-paths
   - Similarly a shared single-prefix path can be reduced
     - The final result will be the concatenation of single-path prefix and result of branches

### Scaling FP-Tree

- If FP-Tree cannot fit into memory
  - Partition a database into a set of projected databases
  - Construct and mine FP-Tree for each projected database
  - Can further parallel this process

### Benefits

- Complete
- Compact
- Divide-and-Conquer
- No candidate generation and test
- No repeated scan over entire database
- Only contains basic operations, no pattern searching and matching

## ECLAT

> Frequent Pattern Mining with Vertical Data Format

### Vertical Data Format

- `itemset-transID_set` format
  - `transID_set` is a set of transaction IDs containing the itemset
- Frequent patterns can be detected by intersections of `transID_set`

### Diffsets

- Compressed storage of sets
  - `I1 = {1,2,3,4,5}`
  - `intersect(I1, I2) = {1,2,3}`
  - `diff(I1, I2) = {4, 5}`

## Pattern Evaluation Methods

### Lift and Correlation

- Using support and confidence only can be misleading
- Need more accurate metrics

$$ Lift = \frac{P(A,B)}{P(A)P(B)} = \frac{P(B|A)}{P(B)} = \frac{P(A|B)}{P(A)}$$

If $Lift < 1$, the pattern is considered **negatively correlated**.
