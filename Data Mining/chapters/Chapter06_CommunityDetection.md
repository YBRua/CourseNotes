# Community Detection

The goal of community detection is to find the tightly-connected structures in a graph

## Modularity Maximization

### Modularity

- Describes how weel a network is partitioned into communities

Given a partitioning of the network into group $s \in S$, the modularity $Q$ is proportional to

$$ Q \propto \sum_{s\in S}(\#EdgesInGroup - \#ExpectedEdgesInGroup) $$

#### Null Model

##### Rewired Network

Given an actual graph $G$ of $n$ nodes and $m$ edges, construct rewired graph $G'$

- Same degree distribution
- Random connections
- Multigraph
  - Allow multiple edges between nodes
- Expected number of edges between nodes $i$ and $j$ of degrees $k_i$ and $k_j$ is $k_i\cdot k_j/2m$

Then we can use the rewired network to estimate the expected number of edges

#### Computing Modularity

Given a graph $G$ and partition $S$

$$ Q(G,S) = \frac{1}{2m}\sum_{s\in S}\sum_{i\in s}\sum_{j\in s} \left( A_{ij} - \frac{k_ik_j}{2m} \right) $$

- $Q \in [-1, 1]$
- It is positive if the number of edges within groups exceeds the expected number
- Emprically, $Q \in [0.3,0.7]$ indicates community structure

#### Equivalent Definition

$$ Q(G,S) = \frac{1}{2m}\sum_i\sum_j \left( A_{ij} - \frac{k_ik_j}{2m} \right)\delta (c_i, c_j) $$

### Louvain Method

- Greedy algorithm
- $O(n\log n)$
- Supports weighted graphs
- Provides hierarchical partitions

#### Overview

- Each pass is made of 2 phases
  1. Partitioning. Modularity is optimized by allowing only local changes of communities
  2. The identified communities are aggregated in order to build a new network of communities
- Repeat until convergence

#### Partitioning

- Put each node into a distinct community (one node per community)
- For each node $i$
  - Compute modularity gain $\Delta Q$ when putting node $i$ into the some community of neighbour $j$
  - Move $i$ to a community that yields the highest $\Delta Q$

$$ \Delta Q(i, C) = \left[ \frac{\sum_{in}+k_{i,in}}{2m} - \left( \frac{\sum_{tot}+k_i}{2m} \right)^2 \right] - \left[ \frac{\sum_{in}}{2m} - \left( \frac{\sum_{tot}}{2m} \right)^2 - \left( \frac{k_{i,in}}{2m} \right)^2 \right] $$

- $\sum_{in}$: sum of weights of links inside community $C$
- $\sum_{tot}$: sum of weights of all links to nodes in $C$
- $k_i$: sum of weights of all links to node $i$
- $k_{i,in}$: sum of weights of all links to node $i$ in $C$

#### Restructuring

- The paritions obtained in the partitioning phase are contracted into supernodes
  - Supernodes are connected if there is at least one edge between the nodes of the corresponding communities
  - Weight of edges between supernodes is the sum of weights from all edges between the corresponding partitions
