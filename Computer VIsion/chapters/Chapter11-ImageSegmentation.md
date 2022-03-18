# Image Segmentation

## Principles of Perceptrual Organization and Gestalt

- Similarity
- Parallelism
- Symmetry
- Common Fate
- Proximity
- Figure-Ground
- Continuity
- Closure

### Intuitions

- Whole is greater than sum of its parts
- Relationships among parts can yield new properties

## Overview of Segmentation

### Goal

- Group pixels into meaningful or perceptually similar regions
- Separate images into coherent objects

### Workflow

- Bottom-up
  - Group tokens with similar features
- Top-down
  - Group tokens that are likely belong to the same object

## Bottum-Up Segmentation via Clustering

- For very basic toy images, we can easily perform segmentation by grouping pixels according to their intensities
- For more complicated images, if we still group pixels by intensity, then we will need clusters of intensities

Best cluster centers are those that minimizes the SSD between all points and their nearst cluster center

### K-Means

- Algorithm
  - Omitted
- Properties
  - Will always converge to the same solution
  - Can be a local minimum

#### Choosing Features

- Intensity
- RGB
- Position

#### Pros and Cons

- Pros
  - Simple
  - Converges to local minimum
- Cons
  - Choice of $k$
  - Sensitive to outliers
  - Can only handle convex structures
  - Assumes means can be computed

### Mean Shift

> A versatile technique for cluster based segmentation

#### Kernel Density Estimation

$$ \hat{f}_h(x) = \frac{1}{nh}\sum_{i=1}^n K\left( \frac{x-x_i}{h} \right) $$

where $K$ is a kernel function, for example Gaussian kernel

$$ K\left( \frac{x - x_i}{h} \right) = \frac{1}{\sqrt{2\pi}}e^{-\frac{(x-x_i)^2}{2h^2}} $$

#### Overview of Mean Shift

1. Compute mean shift vector $m(x)$
2. Translate the Kernel window by $m(x)$

#### Attraction Basins and Clusters

- Attraction Basin
  - The region for which all trajectories lead to the same mode
- Cluster
  - All data points in the attraction basin of a mode

#### Procedure

1. Choose a kernel and a bandwidth
2. For each point
   1. Center a window on the point
   2. Compute the mean of the data in the search window
   3. Center the search window at the new mean location
   4. Repeat 2,3 until convergence
3. Assign points that lead to nearby modes to the same cluster

#### Implementation Considerations

- Speedup
  - Use bins instead of individual points
  - Individual points are represented by a bin whose center is the center of mass of this group of points
  - Use k-d Tree or approximate NN for fast neighbour search
  - Updated all windows in an iteration for faster convergence
- Other tricks
  - Use KNN to determine window sizes adaptively

#### Pros and Cons

- Pros
  - Good general-purpose segmentation
  - Flexible in number and shape of regions
  - Robust to outliers
- Cons
  - Choice of kernel size
  - Not suitable for high-dimensional data

## Segmentation as Graph Partition

- Segmentation can be implemented via Graph Cut
- MinCut is not suitable because it favours isolated pixels

### Normalized Cut (NCut)

$$ NCut(A, \bar{A}) = \frac{cut(A,\bar{A})}{assoc(A,V)} + \frac{cut(A,\bar{A})}{assoc(\bar{A},V)} $$

where

$$ assoc(A,V) = \sum_{u\in A,t\in V} w(u,t) $$

- NP-hard

#### Approximation Formulation

Assume we parition the graph into 2 parts. We use a vector to represent which part each node has been assigned to. Let $1$ denote $v \in A$ and $-1$ denote $v \notin A$.

$$ NCut(A,\bar{A}) = \frac{\sum_{x_i>0,x_j<0}-w_{ij}x_ix_j}{\sum_{x_i>0}d_i} +\frac{\sum_{x_i<0,x_j>0}-w_{ij}x_ix_j}{\sum_{x_i<0}d_i} $$

Let $W$ be the affinity matrix encoding edge weights, and let $D$ denote a diagonal matrix with $d_i$ on its main diagonal. Then

$$ NCut(x) = \min_{x}\frac{y^\top(D-W)y}{y^\top Dy} $$

where

$$ y = \frac{1}{2}[(1+x) - b(1-x)] \quad b= \frac{\sum_{x_i>0}d_i}{\sum_{x_i<0}d_i}$$

Therefore

$$ y^\top(D-W)y = 0 $$

Let $\mathcal{L} = I - D^{-1/2}WD^{-1/2}$, we perform EVD on $\mathcal{L}$ and choose the second larges eigenvector as the solution (to avoid trivial solutions)
