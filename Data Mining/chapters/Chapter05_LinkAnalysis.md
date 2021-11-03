# Link Analysis

## Web as a Graph

- Nodes: Websites
- Edges: Hyperlinks

### Organization of Webs

- Web directories
- Search engines

#### Challenges of Web Search

1. Determining which websites are trust-worthy
   - Trick: trustworthy pages may link to each other
2. Finding the best reply to a user query
   - Trick: e.g. pages that know about newspapers may point to many newspaper websites

### Link Analysis

- Rank the importance of webpages by the link structure

## PageRank

### Intuition of PageRank

- Use links as votes
  - A page is more important if it has more links
  - Use incoming-links as votes
  - Links from important pages have more importance

### Random Surfer

- Webpages are important if people visit them a lot
- But cannot track all web users
- Assume people follow links randomly as a surrogate model
- Random Surfer Model
  - Start at a random page and follow outlines repeatedly
  - PageRank is defined by the limiting probability of visiting a page

### PageRank

- Importance of a page = its share of the importance of each of its predecessor pages
- Technically, the importance is given by the principal eigenvector of the matrix

### Flow Formulation

- Each link's vote is proporional to the importance of its source page
- If page $j$ with importance $r_j$ has $n$ outgoing links, then each link gets $r_j/n$ votes
- The importance of a page $j$ is the sum of the votes on its incoming links
- The rank of a page is given by

$$ r_j = \sum_{i\to j}\frac{r_i}{d_i^{(out)}} $$

- $d_i^{(out)}$ is the degree of outgoing edges

#### Linear Equation Formulation

- We can write the flow equations as a set of linear equations
- The equation has more than one solutions
  - So we manually force the sum of all ranks to be $1$
- Can be solved by Gaussian elimination
- Works with small graphs
  - But not suitable for large networks like the Internet due to high time complexity

### Matrix Formulation

Define a stochastic transition matrix $M$. Let page $i$ has $d_i$ outgoing links

- If $i\to j$, then $M_{ji} = \frac{1}{d_{i}}$
- Otherwise $M_{ji}=0$
- A column stochastic matrix
  - Note this is the transpose of the transition matrix mentioned in Stochastic Processes

Then the limiting probability distribution is given by

$$ r = M \cdot r $$

The distribution $r$ is an eigenvector of matrix $M$, with eigenvalue $1$

- In fact $r$ is the first or principal eigenvector
- Because $M\cdot r \le 1$

#### Power Iteration

1. Init $r = [1/N, 1/N, \dots, 1/N]$
2. Update $r_{t+1} = M\cdot r_t$
3. Stop when $|r_{t+1} - r_t| < \epsilon$

- Actually the power iteration iteratively computes $M^t r$

### PageRank as a Markov Chain

#### Problems

- Unlike the random walk on an undirected graph, the graph of websites are directed
- Which causes problems

##### Deadends

- Random surfer goes into a node with no outgoing edges
- The matrix is no longer column stochastic so the initial assumption fails

##### Spider Traps

- Random surfer gets stuck in a loop
- Eventually the loop absorbs all importance
- The distribution does not converge to the distribution we want

##### Teleports

- A solution proposed by Google
- At each node
  - Follow a link at random with probability $\beta$
  - Jump to a random page with probability $1 - \beta$
  - Typical value of $\beta$ is $0.8 \sim 0.9$

$$ r_j = \sum_{i \to j}\beta \frac{r_i}{d_i} + (1-\beta)\frac{1}{N} $$

$$ A = \beta M + (1-\beta) \left[\frac{1}{N}\right]_{N\times N} $$

Then we solve for $r = A\cdot r$
