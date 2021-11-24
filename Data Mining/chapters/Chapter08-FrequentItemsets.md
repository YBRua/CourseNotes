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
