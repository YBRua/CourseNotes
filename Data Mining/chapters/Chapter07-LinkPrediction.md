# Link Prediction

## Feature Learning in Graphs

### Network Embedding

The task is to map each node in a network to a point in a low-dimensional space

- Similarity in embedding indicates similarity in structure

#### Difficulties

- Complex topographical structure
- No fixed node ordering
- Dynamic and have multimodal features

#### Node Embedding

- The goal is to construct an encoding module for node embedding
- So that the similarity in the embedded space approximates similarity in original graph

$$ Sim(u,v) \approx \mathbf{z}_u^T\mathbf{z}_v $$

- To do this, we need
  - A node similarity measurement $Sim$
  - And of course, an encoder

#### Shallow Embedding

$$ Encoder(v) = \mathbf{Z}\mathbf{v} $$

- An embedding-lookup
  - Widely applied to many embedding models
- $\mathbf{Z}$ is the embedding metrix to be learned
  - Each column is a embedding for a certain node
- $\mathbf{v}$ is a one-hot vector

## DeepWalk

Let $\mathbf{z}_u^T\mathbf{z}_v$ approximate the probability that node $u$ and $v$ co-occur in a random walk in the network

- Expressivity
  - Flexible stochastic definition that incorporates both local and higher-order neighbourhood information
- Efficiency
  - Do not need to consider all pairs of nodes. Only a sequence of random walk is needed

### Neighbourhood Definition

Let $N_R(u)$ be the neighbourhood of node $u$ obtained by some strategy $R$

### Objective

$$ \max_z \sum_{u\in V}\log P(N_R(u)|z_u) $$

- $N_R(u)$ is the neighbourhood of $u$

Assume the conditional likelihood factorize over the set of neighbours, i.e. nodes are independent

$$ \log P(N_R(u)|z_u) = \sum_{v\in N_R(u)} \log P(z_v|z_u) $$

We estimate $P(z_v|z_u)$ by Softmax

$$ P(z_v|z_u) = \frac{\exp(z_v\cdot z_u)}{\sum_{n\in V}\exp(z_n\cdot z_u)} $$

Therefore we minimize the negative log likelihood

$$ L = \sum_{u\in V}\sum_{v\in N_R(u)} -\log\left( \frac{\exp(\mathbf{z}_v^T\mathbf{z}_u)}{\sum_{n\in V}\exp(\mathbf{z}_n^T\mathbf{z}_u)} \right) $$

Unfortunately the computational overhead is large due to the Softmax funtion iterating over the entire vertex set and computing exponentials

#### Negative Sampling Approximation

Simplify the problem into a binary classification.

- Maximize the probability that a node co-occurs with its neighbouring node
- Minimize the probability that the node co-occurs with some randomly chosen nodes

Approximate log softmax by log sigmoid.

$$ \log\left( \frac{\exp(\mathbf{z}_v^T\mathbf{z}_u)}{\sum_{n\in V}\exp(\mathbf{z}_n^T\mathbf{z}_u)} \right) \approx \log(\sigma(\mathbf{z}_u^T\mathbf{z}_v)) - \sum_{i=1}^k \log(\sigma(\mathbf{z}_u^T\mathbf{z}_{n_i})) $$

- Where $n_i$ is randomly sampled from the entire vertex set
- Choice of $k$ is usually proportional to $k$
  - Higher $k$ gives robust estimation
  - Emprical value is between 5 and 20

### Algorithm

1. Run short fixed-length random walks starting from each node using strategy $R$ (typically uniform at random)
2. For each node $u$ collect $N_R(u)$, the multiset of nodes visited on random walks starting from u
   - $N_R(u)$ can have repeat elements because nodes can be visited multiple times on random walks
3. Optimize the objective with gradient descent

## Node2Vec

Uses flexible, biased random walks that can trade off between local and global views of the network

### Interpolation of BFS and DFS

- BFS characterizes the micro view of the neighbourhood
- DFS characterizes the macro view of the neighbourhood

Node2Vec implements a biased fixed-length random walk

- Return parameter $p$
  - Return back to the previous node
- In-out parameter $q$
  - Moving outwards (DFS) or inwards (BFS)
  - Intuitively, it is the radio of DFB/BFS

Consider the unnormalized probabilities

- With probability $1/p$, it returns to previous node
- With probability $1/q$, it moves further from the starting node
- With probability $1$, it stays close to the preceding node

A BFS-like walk has low $p$, and a DFS-like walk has low $q$

### Algorithm

1. Compute random-walk probabilities
2. Simulate $r$ random walks of length $l$ starting from each node $u$
3. Optimize objective function

- Linear time comlexity
- All 3 steps are individually parallelizable

## Embedding in Downstream Tasks

- Usage of embedding
  - Clustering or community detection
  - Node classification
  - Link prediction
    - Predict edge $(i,j)$ based on $f(z_i, z_j)$
    - $f$ can be various operations such as
      - Concatenation
      - Hadamard (element-wise product)
      - Summation or average
      - Distance

## Graph Embedding

Embedding an entire graph

### By Node Embedding

- Run a standard node embedding algorithm
- Sum or average the node embedding

### Metanodes

- Introduce 'virtual node's to represent a subgraph of the graph and run a standard node embedding algorithm
