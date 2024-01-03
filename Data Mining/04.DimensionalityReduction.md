# Dimensionality Reduction

## Singular Value Decomposition

Gives dense $U$, $V$ and sparse $\Sigma$

### Motivating Example

Consider a point cloud in 3D space, represented by a matrix where each row is a point

$$ \begin{bmatrix}
    1 & 2 & 1\\
    -2 & -3 & 1\\
    3 & 5 & 0
\end{bmatrix} $$

Notice that the rank is $2$, so $A,B,C$ are linearly dependent, and we can change the basis into $[1,2,1]$ and $[-2,-3,1]$. In this way $A'=[1,0]$, $B'=[0,1]$ and $C'=[1,-1]$

### Formulation of SVD

$$ A_{m\times n} = U_{m \times r}\Sigma_{r\times r}V^T_{n\times r} = \sum_i \sigma_i u_i \circ v_i^T $$

- $A$: Input matrix of $m \times n$
  - e.g. $m$ documents, $n$ terms
- $U$: Left singular vectors of $m\times r$
  - e.g. $m$ documents, $r$ concepts
  - $U^TU=I$
- $\Sigma$: Diagonal matrix whose diagonal elements are singular values
  - e.g. Strength of each 'concept'
  - $r$: rank of $A$
- $V$: Right singular vecotors
  - e.g. $n$ terms, $r$ concepts
  - $V^TV=I$
- Usually $r \ll n$

### SVD as Dimension Reduction

- Similar to PCA
- Sort the singular values in descending order
- Set the smallest singular values to zero
- SVD minimizes the reconstruction error in terms of Frobenius Norm
- Usually keeps 80%=90% Energy

### Computing SVD

- $A^TA=V\Sigma^2V^T$
- $AA^T=U\Sigma^2U^T$
- We can reduce solving for SVD into solving for EVD

#### Iterative Numerical Method for Eigenvalues

> The Power Iteration

- Let $M = AA^T$

1. Start with any guess $x_0$
2. $x_{k+1} = \frac{Mx_k}{\|Mx_k\|_F}$
3. Repeat until $x_{k}$ changes little
4. $x_k$ converges to a eigenvector
5. $M' = M-\lambda xx^T$
6. Compute next vector using $M'$

- Complexity: $O(nm^2)$ or $O(n^2m)$

### SVD and PCA

- The same if the matrix is zero-centered

## CUR Decomposition

Express $A$ as a product of matrices $C,U,R$ s.t. $\|A - CUR\|_F$ is small, Gives sparse $C$ and $R$ and dense $U$

- $C$ is sampled randomly from columns of $A$
  - Samples can be repeated
- $R$ is sampled randomly from rows of $A$
- $U$ is the pseudo-inverse of intersections of $C$ and $R$

### Sampling Rows and Columns

- Probability is based on values
- e.g. for columns
- $P(x) = \sum_i A(i,x)^2 / \sum_i\sum_j A(i,j)^2$

### Computing $U$

- Let $W$ be the matrix formed by the intersection of $C$ and $R$
- Let $XZY^T$ be the SVD of $W$
- Then $U = YZ^+X^T$ where $Z^+$ is the reciprocals of non-zero singular values $Z_{ii} = 1/Z^+_{ii}$

## Factor Analysis
