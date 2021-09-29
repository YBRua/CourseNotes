# Finding Similar Items

## Motivating Example: Finding Similar Documents

## Locality-Sensitive Hashing

### Idea

Hash items using many different hash functions

### Procedure

```mermaid
graph LR
    Document -->|Shingling|Strings
    Strings -->|MinHashing|Signatures
    Signatures -->|LSH|Candidates
```

#### Shingling

- Convert documents to sets
- Simple approaches
  - Document $\to$ set of words
  - Document $\to$ set of 'important' words
  - Do not work well
    - Order of words matters

##### $k$-shingle

$k$-shingle
: aka. $k$-grams. A sequence of $k$ tokens in the document. Tokens can be words or characters.

##### Compressing Shingles

- Hash shingles into bytes
- Represent the document by hash values

##### Encoding of Shingles

- Each document can be represented by a 0-1 vector in the space of all $k$-shingles
  - Each unique shingle is a dimension
  - Vectors are very sparse
- Documents that have similar shingles tend to have similar texts
- Choice of $k$
  - 5 for short articles
  - 10 for long articles

##### Data Cleaning for Shingling

- Stop words
  - Do not contribute to the topic
  - But useful for distinguishing main articles from other unrelated data (such as ads)
    - Use shingles starting with stop words

#### Min Hashing

##### Set Similarity

Jaccard Similarity
: Given two sets $C_1$, $C_2$, the Jaccard Similarity is given by the size of their intersection divided by the size of their union.

  $$|C_1 \cap C_2| / |C_1 \cup C_2|$$

Jaccard Distance
: $$ d(i,j) =  1 - |C_i \cap C_j| / |C_i \cup C_j| $$

##### Motivation for Minhashing

- Consider 1M documents
  - Approximately `5e11` comparisions
  - Takes 5 days
  - Slow
- Re-formulate the problem as finding subsets that have significant intersection
  - Encode sets using 0-1 vectors
  - Perform intersect and union by bitwise AND and OR

##### Minhashing

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

##### The MinHash Property

Choose a (uniformly) random permutation $p$,

$$ \mathbb{P}[h(C_1) = h(C_2)] = \textrm{sim}(C_1,C_2) $$

- Sketch of Proof
  - Each shingle is equally likely to appear as the min element
  - ?

##### MinHash Signatures

Suppose we sample $n$ permutations, then we can construct a signature matrix with $M$ columns and $n$ rows, where $M$ is the number of documents.

- More perumutation samples $\to$ More rows $\to$ Higher accuracy
- We can then compute the signature similarity
  - Signature similarity can be used to approximate the original Jaccard similarity
