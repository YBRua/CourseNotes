# Fast Fourier Transform

EE people’s favorite algorithm.
The **Fast Fourier Transform** is a family of algorithms for efficiently computing the DFT.

## Motivation

Computing DFT by definition is slow.

- $O(n^2)$ complex multiplications and complex additions.

## Divide-and-Conquer

### Theory

Recall the definition of DFT
$$ X[k] = \sum_{n=0}^{N-1} x[n] W_N^{kn} $$

Assume $N$ is a power of 2
$$ X[k] = \sum_{r=0}^{N/2-1} x[2r] W*N^{2rk} + W_N^k \sum_{r=0}^{N/2-1} x[2r+1]W*N^{2rk} $$

Notice that $W_N^{2rk} = W*{N/2}^{rk}$.
$$X[k]= \sum_{r=0}^{N/2-1} x[2r] W^{rk}_{N/2} + W_N^k \sum_{r=0}^{N/2-1} x[2r+1] W_{N/2}^{rk}$$

Therefore
$$X[k] \triangleq G[k] + W_N^k H[k]$$

We have divided the original problem into 2 sub-problems.
$$G[k] = \sum_{r=0}^{N/2-1} x[2r]W_{N/2}^{rk}$$

$$H[k] = \sum_{r=0}^{N/2-1} x[2r+1] W_{N/2}^{rk}$$

- $G[k]$ and $H[k]$ are arrays of length $N$.
- They are the DFT of $x[2r]$ up-sampled (inserted 0 between elements) in time-domain.
- $G[k]$ and $H[k]$ can be computed on $N/2$ samples.
- Computing $G[k]$ and $H[k]$ require $O(N^2/2)$ respectively because they are of length $N$.
- So the total complexity is still $O(N^2)$.

However, $G[k]$ and $H[k]$ are $N/2$-periodic.
For $0 \le k \le N/2-1$
$$ X[k] = G[k] + W_N^k H[k] $$
For $ N/2 \le k \le N-1$, let $k = k' + N/2$
$$ X[k] = G[k' + N/2] + W_N^{k' + N/2} H[k' + N/2] = G[k'] - W_N^k H[k'] $$

- So we actually only have to compute the first period.
- This halves computational complexity, so the total complexity is $O(N^2/2)$

### Decimation-in-time Algorithm

**Fact.** An $N$ point DFT can be decomposed into two $N/2$ DFTs, by dividing it into even terms and odd terms. This procedure is **recursive**.
**Example.** A 8-bit array $[a,b,c,d,e,f,g,h]$ is re-arranged into
$$[[a,e],[c,g],[b,f],[d,h]]$$

$$
\begin{cases}
X[k]&=G[k] + W_N^kH[k]\\
X[k+N/2] &= G[k] - W_N^k H[k]
\end{cases}
$$

#### Bit-reversed sorting

Notice that the FFT re-arranges an input array by whether the index is even or odd.

1. Given an input, we can rewrite its indices into binary form. $x[n_2n_1n_0]$
2. Then we divide and sort the elements starting from the Least Significant Bit. $n_0 \to n_1 \to n_2$

#### Complexity

- An $N$-element input can be divided into $\log_2N$ levels.
- At each level we need $O(N)$ computations.
- The total complexity is $O(n\log_2n)$

### Decimation-in-frequency Algorithm

In the previous algorithm, we divide the input into even terms and odd terms in the **time-domain**.
The decimation-in-frequency algorithm starts from the output’s prospective, by dividing the output into even terms and odd terms, or equivalently, by dividing the input into the first $N/2$ and last $N/2$.
For even terms in frequency domain,
$$ X[2r] = \sum_{n=0}^{N/2-1} x[n]W_N^{(2r)n} + \sum_{n=0}^{N/2-1} x[n + N/2] W_N^{2r(n+N/2)} = \sum_{n=0}^{N/2-1}(x[n]+x[n+N/2])W_{N/2}^{rn} $$

Similarly, for odd terms in frequency domain,
$$ X[2r+1] = \sum_{n=0}^{N/2-1}(x[n]-x[n+N/2])W_{N/2}^{rn} $$

**Remark.**

- The decimation-in-frequency algorithm directly reduces an input of length $N$ into two arrays of length $N/2$.
- Both methods exploit the feature that $W_N$ is periodic.

### IFFT

To compute the IFFT, we simply take the conjugate of the FFT as the input and take another conjugate in the output.

## Matrix Interpretation of FFT

Recall that the DFT can be re-written in matrix form. The matrix has full rank and is dense. Directly computing the matrix multiplication requires $O(n^2)$.

However, recall the decimation-in-time algorithm.

$$
\begin{cases}
X[k]&=G[k] + W_N^kH[k]\\
X[k+N/2] &= G[k] - W_N^k H[k]
\end{cases}
$$

Let $\mathbf{G}$ and $\mathbf{H}$ be the vectors corresponding to $G[k]$ and $H[k]$,

$$
\mathbf{X} = \mathbf{W_N}\cdot\mathbf{x} =
\begin{bmatrix}
\mathbf{I_{N/2}} & \mathbf{\Omega_{N/2}}\\
\mathbf{I_{N/2}} & -\mathbf{\Omega_{N/2}}
\end{bmatrix}
\begin{bmatrix}
\mathbf{G} \\
\mathbf{H}
\end{bmatrix}
$$

where $\mathbf{I}$ is the identity matrix and $\mathbf{\Omega}$ is a diagonal matrix $\text{diag}(W_N^0,W_N^1,\dots,W_N^{N-1})$

By doing this recursively, we have

$$
\mathbf{X} = \mathbf{W_N}\cdot\mathbf{x} = \mathbf{B_N}
\begin{bmatrix}
\mathbf{B_{N/2}} & 0 \\
0 & \mathbf{B_{N/2}}
\end{bmatrix}
\begin{bmatrix}
\mathbf{G’}\\
\mathbf{H’}\\
\mathbf{G’’}\\
\mathbf{H’’}
\end{bmatrix} =
\mathbf{B_N}
\begin{bmatrix}
\mathbf{B_{N/2}} & 0 \\
0 & \mathbf{B_{N/2}}
\end{bmatrix}
\begin{bmatrix}
\mathbf{B_{N/4}} & 0 & 0 & 0\\
0 & \mathbf{B_{N/4}} & 0 & 0\\
0 & 0 & \mathbf{B_{N/4}} & 0\\
0 & 0 & 0 & \mathbf{B_{N/4}}
\end{bmatrix}\cdots
\mathbf{P^T}
\mathbf{x}
$$

- $\mathbf{P^T}$ is a permutation matrix that re-arranges $\mathbf{x}$ into a correct order.
- The dense matrix is now decomposed into a sparse and well-structured matrix.
- Can be computed efficiently.

### Computing the FFT in matrix form

- No need to compute $\mathbf{B_2}$ because it is $[[1,1],[1,-1]]$.
- For other $\mathbf{B}$, only need to compute the $\mathbf{\Omega}$ on the upper-right.
- The total complexity is still $O(n\log n)$
