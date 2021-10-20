# Clustering and Dimensionality Reduction

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
