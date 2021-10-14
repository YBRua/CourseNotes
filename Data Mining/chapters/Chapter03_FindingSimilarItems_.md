# Finding Similar Items

## Motivating Example: Finding Similar Documents

### Idea

Hash items using many different hash functions

### Procedure

```mermaid
graph LR
    Document -->|Shingling|Strings
    Strings -->|MinHashing|Signatures
    Signatures -->|LSH|Candidates
```

## Shingling

- Convert documents to sets
- Simple approaches
  - Document $\to$ set of words
  - Document $\to$ set of 'important' words
  - Do not work well
    - Order of words matters

### $k$-shingle

$k$-shingle
: aka. $k$-grams. A sequence of $k$ tokens in the document. Tokens can be words or characters.

### Compressing Shingles

- Hash shingles into bytes
- Represent the document by hash values

### Encoding of Shingles

- Each document can be represented by a 0-1 vector in the space of all $k$-shingles
  - Each unique shingle is a dimension
  - Vectors are very sparse
- Documents that have similar shingles tend to have similar texts
- Choice of $k$
  - 5 for short articles
  - 10 for long articles

### Data Cleaning for Shingling

- Stop words
  - Do not contribute to the topic
  - But useful for distinguishing main articles from other unrelated data (such as ads)
    - Use shingles starting with stop words

## Min Hashing

### Set Similarity

Jaccard Similarity
: Given two sets $C_1$, $C_2$, the Jaccard Similarity is given by the size of their intersection divided by the size of their union.

  $$|C_1 \cap C_2| / |C_1 \cup C_2|$$

Jaccard Distance
: $$ d(i,j) =  1 - |C_i \cap C_j| / |C_i \cup C_j| $$

### Motivation for Minhashing

- Consider 1M documents
  - Approximately `5e11` comparisions
  - Takes 5 days
  - Slow
- Re-formulate the problem as finding subsets that have significant intersection
  - Encode sets using 0-1 vectors
  - Perform intersect and union by bitwise AND and OR

### Minhashing

We construct a boolean matrix of documents

- Rows: shingles
- Columns: documents
  - Column similarity is the Jaccard similarity

To find similar documents, we only need to find 'similar' columns. To do this, we compress the long long columns into signatures, and compare the signatures of documents

- Find a hash function $h$
  - If $\textrm{sim}(C_1,C_2)$ is high, then with high probability $h(C_1) = h(C_2)$
  - Hash documents into different buckets and expect that similar documents are in the same bucket

The hash function depends on the similarity metric, and for Jaccard similarity, min-hashing is a suitable function

1. Permute the rows of the booleam matrix at random
2. $h(C)$ is defined to be the first row in the perumuted matrix where column $C$ has value 1.
3. Use several (say, 100) independent permutations to create a signature of a column

### The MinHash Property

Choose a (uniformly) random permutation $p$,

$$ \mathbb{P}[h(C_1) = h(C_2)] = \textrm{sim}(C_1,C_2) $$

- Sketch of Proof
  - Each shingle is equally likely to appear as the min element
  - Let $X$ be the set of all shingles and let $y$ be a shingle
  - $\mathbb{P}[h(y) = \min(h(X))] = 1/|X| $
    - It is equally likely that any $y$ is permuted to the min element
  - Let $y$ be some shingle s.t. $h(y) = \min(h(C_1\cup C_2))$ then either
    - $h(y)=\min(h(C_1))$ if $y \in C_1$
    - $h(y) = \min(h(C_2))$ if $y \in C_2$
  - Therefore the probability that both cases are true is the probability of $y \in C_1 \cap C_2$

### MinHash Signatures

Suppose we sample $n$ permutations, then we can construct a signature matrix with $M$ columns and $n$ rows, where $M$ is the number of documents.

- More perumutation samples $\to$ More rows $\to$ Higher accuracy
- We can then compute the signature similarity
  - Signature similarity can be used to approximate the original Jaccard similarity

### Row Hashing

- The random permutation is still time consuming
  - 'Simulate' a random permutation by a **random hash function** that maps row numbers to buckets
    - input row number, output 'permuted' row number

1. Pick $k$ (say $k=100$) hash functions $h_k$
   - Universal hashing $(ax + b \bmod p) \bmod N$ where $p > N$ is a prime int.
2. Order under $h_i$ gives a random row permutation
3. Construct a $k \times N$ matrix where $N = \#docs$
4. Consider the $C$-th document
5. Init $sig(C)(i) =\infty$
6. Suppose row $j$ have value 1 in column $C$
   - For each $h_i$
     - If $h_i(j) < Sig(C)(i)$ then $Sig(C)(i) \leftarrow h_i(j)$

## Locality-Sensitive Hashing

- For $N$ documents, the total number for one-by-one comparision required is $C_{N}^2$.
  - This is not good.
  - Actually it is pretty bad.
- Consider hashing the document signatures into 'buckets' known as **candidate pairs**.

### Overview

- Goal
  - Finding docs with Jaccard similarity at least $s$ (say $s=0.8$)
- Idea
  - Use a function $f(x,y)$ that can efficiently indicate whether $x$ and $y$ are a candidate pair
  - Only further examine documents in the same bucket. i.e. candidate pairs.

### Procedure

- Divide the signature matrix $M$ into $b$ bands along the rows
  - Suppose each band contains $r$ rows
- For each band, hash its portion of columns to a hash table with $k$ buckets
  - Usually, only two bands that are identical are put into the same bucket
- Candidate pairs are columns that hash to the same bucket for at least one band
- Tune $b$ and $r$

### Tradeoff

- Number of min-hashes (rows of $M$)
- Number of bands $b$
- Number of rows per band $r$
- Threshold $t$

Then for any band

- Prob. that all rows are equal: $t^r$
- Prob. that some rows are not equal: $1 - t^r$
- Prob. that no bands are identical $(1 - t^r)^b$
- Prob. that at least one band is identical $1 - (1 - t^r)^b$

## Applications of LSH

### Entity Resolution

#### Problem Setting

Examining a collection of records and determining which records refer to the same entity.

#### Steps

1. Design a measure of how similar records are
2. Score all pairs of records that the LSH scheme identified as candidates
3. Report high scores as matches

### Matching Fingerprints

#### Minutiae

Represent fingureprints by sets of positions of minutiae (features of fingerprints. e.g., points where two ridges come together or a ridge ends)

- Place a grid on the fingerprint
- Represent the fingerrping by the set of grid squares where minutiae are located
- The problem becomes finding similar sets of grid squares

#### Steps

- Rows: grid squares; Columns: fingerprints; note that the matrix is not spare
- No need to minhash since the number of grid squares is not very large
- Represent each fingerprint by a bit vector
- Pick 1024 sets of 3 squares randomly
- For each set of 3 squares, two fingerprints that each have 1 for all 3 squares are candidates

### Matching News Articles

- See motivating example
- Alternative option for hashing articles: lengths of articles

## Distance Measures

- Euclidean distance
  - Norms
- Jaccard distance
  - IoU
- Cosine distance
  - angle between two vectors
- Edit distance
- Hamming distance
  - number of positions in which two bit vectors differ

## Locality-Sensitive Functions

- A hash function $h$ takes two elements $x$ and $y$ as input, and returns a decision whether $x$ and $y$ are candidates for comparision
- Suppose we have a space $S$ of pionts with distance measure $d(\cdot,\cdot)$
- A family of hash functions $H$ is said to be $(d_1,d_2,p_1,p_2)$-sensitive if
  - If $d(x,y) \le d_1$, prob. that $h(x,y) \ge p_1$ for all $h \in H$
  - If $d(x,y) \ge d_2$, prob. that $h(x,y) \le p_2$ for all $h \in H$
- For Jaccard similarity, minhashing gives a $(d_1,d_2,(1-d_1),(1-d_2))$-sensitive functions

### AND/OR of Hash Functions

- AND
  - For $h = \{h_1,\dots,h_r\}$, $h(x)=h(y)$ iff $\forall i,h_i(x) = h_i(y)$
- OR
  - For $
