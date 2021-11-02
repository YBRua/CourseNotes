# Applications of Computer Networks

## Chord: A P2P-based File Storage Network

### Introduction

- Distributed File Storage
  - Robust
  - At the cost of file access efficiency

### Chord

#### Architecture

- Hosts are logically connected as a ring
- The address of a host in the ring is determined by a hashing of its IP address via SHA-1 Algorithm
  - Maps an IP address into am $m$-bit bitstring
  - Capacity: $2^m$ hosts
- Files are also mapped into $m$-bit bitstrings by SHA-1
- Store files in the node with the minimum HostId that is greater than or equal to the FileID

#### Finger Table

> For efficient file access

- Each node has a finger table, with entries `i`, `finger[i].start` and `successor`

##### Computing `finger[i].start`

- For each `i` in $m$
  - `finger[i].start = (n + 2**i) % (2**m)`
  - `n` is the current node where the finger table is being computed

##### Computing `successor`

- The $i$-th successor is the first peer with $id \ge n + 2^i \bmod 2^m$

#### Searching for Files

- At node $n$, to find the file with ID $k$
  - Find the greatest successor whose entry $\le k$
- If no such successor exists
  - Send query to next successor
- Complexity $O(\log(n))$

## Task Assignment in Crowdsourcing

### Hungarian Algorithm

- Formulate task assignment as bipartite matching

### Weighted Matching

$$\max \sum_{i}\sum_{j}I_{ij}v_{ij} $$

- $N$ tasks, $M$ workers
- $v_{ij}$ is the value (usually a 'profit') the system can get when matching $i$ with $j$

#### KM Algorithm

### Multiple Matching

- When a worker can do multiple tasks
