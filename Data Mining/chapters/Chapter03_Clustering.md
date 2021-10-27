# Clustering

!!! cite Curse of DImensionality
    In high dimensions, almost all points have basically the same distance.

## Recap of Previously Mentioned Clustering Methods

- Hierarchical
  - Agglomerative Method
  - Divisive Method
- Point Assignment
  - K-means
  - EM-based methods

## Hierarchical Clustering

> Key Operation: Repeatedly combine two nearest clusters

- For Euclidean distances
  - Represent a cluster by its centriod
  - Measure distances of clusters by distances of centroids

### Clustroids

- For Non-Euclidean Cases
  - Choose the 'clustoid' to be the point that is the closest to other points
  - By 'closest' we mean
    - Smallest maximum/average/sum distance
    - e.g. $\min_{c\in C} \sum_{x\in C}d(x,c)^2$
    - Note that a clustroid is selected from the dataset, while a centroid may not exist in the dataset

### Distance between Clusters

#### Intercluster distance

Minimum distance between any pair of points from the two clusters

#### Cohesion

Pick a notion of cohesion of clusters

- radius: maximum distance from the clustroid

Merge clusters whose union is the most cohesive, e.g.

- diameter of merged clusters

### Stopping Criterion

1. Stop when we have $k$ clusters
2. Stop when the next merges creates a bad cluster with low cohesion
3. Stop when the average diameter takes a sudden jump

### Implementation Considerations

- Naive approach is $O(N^3)$
- Implementation with priority-queue reduces time to $O(N^2\log{N})$
  - Still expensive
- The BFR algorithm

## The BFR Algorithm

> A variant of K-means designed to handle very large datasets
> > Assumes Clusters are normally distributed around a centroid in the Euclidean space

- Points are read from disk
  - Each time we load as many points as possible to the memory
- Most points from previous memory loads are summarized by simple statistics
- Initialize with $k$ points
  - Take random points
  - Take a small sample and cluster
  - Take a sample randomly, and choose the remaining $k-1$ points such that each are as far from previous points as possible

### Three Class of Points

- Discard Set
  - Points close enough existing centroids to be summarized
- Compression Set
  - Points are close enought to each other, but not close to any existing centroids
- Retained Set
  - Isolated points weaiting to be assigned to a compression set

### Summarizing Sets of Points

#### Discard Set

- Number of points $N$
- Vector $SUM$
  - $i$th component is the sum of coordinates of the points in $i$th dimension
- Vector $SUMSQ$
  - $i$th component is the sum of squares of coordinates in $i$th dimension
- A total of $2d+1$ values
- Mean can be computed by $SUM_i/N$
- Variance can be computed by $SUMSQ_i/N - (SUM_i/N)^2$

#### Updating Sets

1. Find points that are sufficiently close to a cluster centroid and add the points to the cluster and the DS
2. Cluster the remaining points and the old RS
3. Adjust statistices of updated DS sets
4. Consider merging CS
5. If is the final iteration, merge all CS and RS points into the nearest cluster

### Implementation Details

#### Deciding 'Close Enough'

Two ways

- High likelihood
- Mahalanobis Distance less than a threshold

$$ d(x,c) = \sqrt{\sum_{i=1}^d\left( \frac{x_i-c_i}{\sigma_i} \right)^2} $$

- $c_i$: centroid

#### Merging Compressed Sets

- Compute the variance of the combined sub-cluster
  - Merge CS if the combined variance is less than a threshold
