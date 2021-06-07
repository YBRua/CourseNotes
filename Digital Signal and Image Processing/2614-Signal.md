# AI2614 Digital Signal and Image Processing
> Digital Signal Processing

[TOC]

# A Functional Interpretation of Signals
## Prerequisites
### Vector Spaces
A vector space $V$ is a set of functions equipped with
- Vector addition: $\forall u,v \in V \quad u + v \in V$
- Scalar multiplication: $\forall \alpha \in \mathbb{R}, \forall v \in V, \quad \alpha v \in V$

### Subspace
$S$ is a subspace of $V$ if
- $S$ is a subset of $V$
- $S$ is a vector space for the addition and scalar multiplication

### Spanned Subspace
Consider $v_1,\dots,v_N$ in a vector space $V$. Define
$$ S = \{ \alpha_1v_1 + \cdots + \alpha_Nv_N: \alpha_1,\dots,\alpha_N \in \mathbb{R} \} $$
$S$ is the subspace spanned by $v_1,\dots,v_N$, denoted by
$$ S = \mathrm{span}(v_1,\dots,v_N) $$

### Euclidean Space
A vector space $V$ is an Euclidean space if an **inner product** is defined on $V$.
- For example, the 2D Euclidean space $\mathbb{R}^2$ has inner product defined by $\langle x,y \rangle = x_1y_1 + x_2y_2$

The formal definition of an inner product is: A function $\langle \cdot, \cdot \rangle$ is called an inner product if
- $\forall u,v \in V, \langle u,v \rangle \in \mathbb{R} or \mathbb{C}$
- $\forall u,v,w\in V, \langle u+v,w \rangle = \langle u,w \rangle + \langle v,w \rangle$
- $\forall \alpha \in \mathbb{R}, \forall u,v \in V, \langle \alpha u, v \rangle = \alpha \langle u, v \rangle$
- $\forall u,v \in V, \langle u,v \rangle = \langle v,u \rangle$
- $\forall u \in V, \langle u,u \rangle \ge 0$
- $\langle u, u \rangle = 0 \Longrightarrow u = 0$

### Normed Space
Based on the inner product, we can define
- Norm: $\|x\| = \sqrt{\langle x,x \rangle}$
  - $\|x\| \ge 0$
- Distance: $d(x,y) = \|x-y\|$
- Orthogonality: $x \perp y \Leftrightarrow \langle x,y \rangle = 0$
- Orthonormal bases.
- Projection.

### Kindergarten Equation
Take $\mathbb{R}^2$ for example. Consider the orthonormal bases
$$\begin{cases}
    e_1 &= (1,0)\\
    e_2 &= (0,1)
\end{cases}
$$
Then the projection of $x=(x_1,x_2)$ can be obtained by inner product
$$\langle x, e_1 \rangle = x_1 \quad \langle x, e_2 \rangle = x_2$$

We introduce the **Kindergarten Equation**
$$ x = x_1e_1 + x_2e_2 = \langle x,e_1 \rangle e_1 + \langle x,e_2 \rangle e_2 $$

### Hilbert Space
The previous discussions can be generalized to arbitrarily large finite and even some infinite dimensions.

The inner product of $\mathbb{R}^{\mathbb{R}}$ is defined by
$$ \langle x,y \rangle = \frac{1}{T}\int_0^T x(t)y^*(t)\mathrm{d}t $$
This form is very similar to the formalism of Fourier transform.

### Fourier Series: A Functional Perspective
Suppose a $T$-periodic signal $x(t)$, its Fourier series is given by
$$ x(t) = \sum_n X[k]\cdot\exp(j2\pi k\frac{t}{T}) $$
- We use a set of orthornormal bases $\exp(j2\pi kt /T)$ to approximate the original signal.

The coefficients $X[k]$
$$ X[k] = \frac{1}{T}\int_0^T x(t)\cdot\exp(-j2\pi k \frac{t}{T})\mathrm{d}t $$
are exactly the projections of $x(t)$ on orthonrmal bases $e_k = \exp(j2\pi kt/T)$

Therefore, Fourier series gives an approximation to the original periodic function in a subspace spanned by $e_k$ in mean square sense.


# Sampling and Interpolation
## Sampling
### Definition
As has been discussed in Signals and Systems, for an arbitrary signal, we can use a Dirac comb to sample it and convert it to a discrete-time signal.
$$ s(t) = \sum_{n=-\infty}^{+\infty} \delta(t-nT) $$

$$x[n] = x(t)s(t) = x(nT)$$

### Invertibility
**Nyquist Sampling Theorem**: For a **band-limited** continuous-time signal, if we sample it with a rate higher than 2$\times$ bandwidth, then we can perfectly reconstruct the original continuous-time signal.

- However, most signals in reality are not band-limited.
- In general, sampling is **not** invertible.

## Interpolation
### Sinc Interpolation
We can reconstruct a band-limited signal by super-imposing scaled sinc function at each sampling point.
$$ \mathrm{sinc}(t) = \frac{\sin(t)}{t} $$

#### Why sinc?
For a band-limited signal $x(t)$ with spectrum $X(j\Omega)$,
$$ X(j\Omega) = \begin{cases}
    something, &\quad |\Omega| \le \Omega_0\\
    0, &\quad |\Omega| > \Omega_0
\end{cases} $$

Therefore the spectrum can be re-written as
$$ X(j\Omega) = X(j\Omega)\cdot\mathrm{rect}\left( \frac{\Omega}{\Omega_0} \right) = X_p(j\Omega)\cdot\mathrm{rect}\left( \frac{\Omega}{\Omega_0} \right) $$
where $X_p(j\Omega)$ is constructed by periodically extending $X(j\Omega)$

Since $X_p(j\Omega)$ is periodic, we can expand it by its Fourier series
$$X_p(\Omega) = \sum_{n=-\infty}^{+\infty} x[n]\exp(j2\pi n \Omega/\Omega_0)\cdot\mathrm{rect}\left( \frac{\Omega}{\Omega_0} \right)$$

The inverse Fourier transform is then given by
$$x(t) = \left( \sum_{n=-\infty}^{+\infty}x[n]\delta(t-nT_0)\right) * \Omega_0\mathrm{sinc}(\Omega_0t)$$

### Aliasing

# Discrete Fourier Transform
## Discrete Fourier Series
## Discrete Fourier Transform


## Properties of DFT

### Complex Conjugate
$$x^*[n] \leftrightarrow X^*[((-k))_N]$$

### Conjugate Symmetry of Real signals
$$ x[n]=x^*[n] \leftrightarrow X[k] = X^*[((-k))_N] $$

#### even-length

| $k$ | -4 | -3 | -2  | -1  |  0  |  1  |  2  |  3  |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $X[k]$ |  a  |  b  |  c  |  d  |  a  |  b  |  c  |  d  |
| $X^*[((-k))_N]$ | a | d | c | b | a | d | c | b |
In this case:
- For $k = 2m$, $X[k]$ must be real values
- For $k = 2m+1$, $X[k]$ and $X^*[((-k))_N]$ must be complex conjugates

#### odd-length
|$k$|0|1|2|3|4|
|:---:|:---:|:---:|:---:|:---:|:---:|
|$X[k]$|a|b|c|d|e|
|$X^*[((-k))_N]$|a|e|d|c|b|
- For $k=0$, $X[0]$ must be a real value
- For other terms, they are complex conjugates

### Circular Convolution
#### Recap: Linear Convolution
$$ x[n]*h[n] = \sum_{m=-\infty}^{+\infty} x[n-m] \cdot h[m] $$
If $x[n]$ is of length $L$ and $h[n]$ is of length $P$
- Output signal has length $L+P-1$
- Requires $LP$ multiplications

#### Definition of Circular Convolution
$$ x_1[n]*x_2[n] = \sum_{m=0}^{N-1}x_1[m] \cdot x_2[((n-m))_N] $$

**Remark.**
- The result of circular convolution **depends on** $N$
- $N$ is a **user-defined** length that can theoretically be any value

**Proposition.**
If $x[n]$ and $h[n]$ are two signals of length $N$, and let $Y[k]=X[k]H[k]$, then $Y[k]$ is the DFT of
$$ y[n]=\sum_{m=0}^{N-1} x[m]h[n-m\mod{N}] $$
- $y[n]$ is the circular convolution of $x[n]$ and $h[n]$.
- i.e. the product of two DFTs in frequency domain is not related to linear convolution in time domain, but related to circular convolution.

**Example.**
Let
- $x_1[n] = [1,1,1,1,1,0,0]$
- $x_2[n] = [a,b,c,d]$

The circular convolution of length $7$ can be calculated as follows
1. Flip $x_2$. $x_2[-n] = [d,c,b,a]$ starting from index $-3$
2. Pad $x_2$ to length $7$. $x_2’[-n] = [0,0,0,d,c,b,a]$ starting from index $-6$
3. Notice that when we take modulo, $[0,6]$ are in the same period, and $[-7,-1]$ are in the same period
4. Therefore the actual $x_2$ in the circular convolution is $x_2[((-n))_N]=[a,0,0,0,d,c,b]$

- $n=0$

|m|0|1|2|3|4|5|6|
|---|---|---|---|---|---|---|---|
|$x_1[m]$|1|1|1|1|1|0|0|
|$x_2[m]$|a|0|0|0|d|c|b|

- $n=1$

|m|0|1|2|3|4|5|6|
|---|---|---|---|---|---|---|---|
|$x_1[m]$|1|1|1|1|1|0|0|
|$x_2[m]$|b|a|0|0|0|d|c|

If we take $a=b=c=d=1$, the final result will be
$$y[n]=[2,2,3,4,4,3,2]$$
**Remark.**
- Inconsistent with the result of linear convolution
    - One bit less than linear convolution
    - Incorrect answer at $y[0]$
- The problem lies in that we didn’t choose a large enough $N$
- So when $n=0$, we computed both $y[0]$ and $y[7]$
- If we choose larger $N$, eg.$N=8$, we will end up with the result of linear convolution

#### Linear Convolution with DFT
Given two signals $x_1[n]$ and $x_2[n]$ of length $L$ and $P$, if we pad both $x_1$ and $x_2$ to length larger than or equal to $L+P-1$, then we can compute the linear convolution of $x_1$ and $x_2$ using DFT
$$x[n]*h[n] = 
\begin{cases}
x_{zp}[n] * h_{zp}[n] \quad & (0 \le n \le M-1)\\
0 \quad & o.w.
\end{cases}
$$
- Advantage: DFT can be computed with $O(n\log n)$
- Drawback: Must wait for all inputs in order to complete padding, incompatible with real-time applications

#### Block Convolution: Overlap-Add Method
To deal with the drawback, we can use block convolution. The basic framework of block convolution follows the idea below:
1. Break signals into blocks
2. Perform DFT to compute linear convolution
3. Combine the result in some way

**Overlap-Add Method**
If we decompose the long signal into non-overlapping segments
$$
x_r[n] = 
\begin{cases}
x[n] \quad & rL \le n < (r+1)L\\
0 \quad & o.w.
\end{cases}
$$

The output will be
$$y[n] = x[n]*h[n] = \sum_{r=0}^{\infty}x_r[n]*h[n]$$

1. Zero-pad $x_r[n]$ and $h[n]$ to $N=L+P-1$
2. Compute DFT of $h[n]$
3. Compute $h[n]*x_r[n]$ by DFT
4. Results are of length $N=L+P-1$
5. Neighboring results overlap by $P-1$
6. Summing up over $r$ yields the desired result


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
$$ X[k] = \sum_{r=0}^{N/2-1} x[2r] W_N^{2rk} + W_N^k \sum_{r=0}^{N/2-1} x[2r+1]W_N^{2rk} $$
Notice that $W_N^{2rk} = W_{N/2}^{rk}$.
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
For $ N/2 \le k \le N-1$, let $k = k’ + N/2$
$$ X[k] = G[k’ + N/2] + W_N^{k’ + N/2} H[k’ + N/2] = G[k’] - W_N^k H[k’] $$
- So we actually only have to compute the first period.
- This halves computational complexity, so the total complexity is $O(N^2/2)$

### Decimation-in-time Algorithm
**Fact.** An $N$ point DFT can be decomposed into two $N/2$ DFTs, by dividing it into even terms and odd terms. This procedure is **recursive**. 
**Example.** A 8-bit array $[a,b,c,d,e,f,g,h]$ is re-arranged into
$$[[a,e],[c,g],[b,f],[d,h]]$$
$$\begin{cases}
X[k]&=G[k] + W_N^kH[k]\\
X[k+N/2] &= G[k] - W_N^k H[k]
\end{cases}$$

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
$$\begin{cases}
X[k]&=G[k] + W_N^kH[k]\\
X[k+N/2] &= G[k] - W_N^k H[k]
\end{cases}$$
Let $\mathbf{G}$ and $\mathbf{H}$ be the vectors corresponding to $G[k]$ and $H[k]$,
$$\mathbf{X} = \mathbf{W_N}\cdot\mathbf{x} =
\begin{bmatrix}
\mathbf{I_{N/2}} & \mathbf{\Omega_{N/2}}\\
\mathbf{I_{N/2}} & -\mathbf{\Omega_{N/2}}
\end{bmatrix}
\begin{bmatrix}
\mathbf{G} \\
\mathbf{H} 
\end{bmatrix}$$
where $\mathbf{I}$ is the identity matrix and $\mathbf{\Omega}$ is a diagonal matrix $\text{diag}(W_N^0,W_N^1,\dots,W_N^{N-1})$

By doing this recursively, we have
$$\mathbf{X} = \mathbf{W_N}\cdot\mathbf{x} = \mathbf{B_N}
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

# Short Time Fourier Transform and Spectral Analysis
## Windowing
The DFT assumes implicit periodicity. Therefore the DFT of a speech signal “123” is almost the same as “231” or “312” because the underlying sequence is “$\dots 123123\dots$”.

Therefore we need proper windowing to perform DFT at an exact given time.

### Motivating Example
Suppose we want to sample a continuous-time signal
$$x_c(t) = \cos(\pi t/3.3) + \cos(\pi t /5.4)$$

If we use sampling frequency $T=1$, the result we get will be an aperiodic signal.
$$ x[n] = \cos(\pi n/3.3) + \cos(\pi n/5.4) $$
- Since the result is aperiodic, we will have to take infinitely many points.
- If we only take a finite number $L$ samples, we actually added an **rectangular window** on the signal.
- Therefore the DTFT or DFT results will be different from what we expect.

Let $x[n]$ denote the infinitely long sampled signal, let $w[n]$ be a rectangular window, then
$$\bar{x}[n] = w[n]x[n]$$
is the actual input we get, and if we perform DTFT on $\bar{x}[n]$,
$$\bar{X}(e^{j\omega}) =  $$

### Rectangular Windowing
Let $w[n]$ be a rectangular window of length $L$.
$$W(e^{j\omega}) = \frac{\sin(\omega L/2)}{\sin(\omega/2)}e^{-j\omega(L-1)/2}$$

- The **first zero-crossing point** is $2\pi / L$.
- The area between first zero-crossing points is called the **main lobe**. The remaining parts are called the side lobes.
- We lose physical resolution due to the finite width of the main lobe.
- We want the main lobe to be as **thin** as possible.
- This can be done by increasing $L$
    - main lobe becomes thinner
    - side lobes become higher

Rectangular window causes discontinuity on edges.
- Side lobes cause **spurious peaks**.
- Can be viewed as the result of slow decay of $|W(e^{j\omega})|$
- Can be mitigated by designing a proper window function that tapers gradually to zero
    - But at the expense of a wider main lobe.

## Short-Time Fourier Transform
The Short-Time Fourier Transform is a basic tool for spectral analysis of time-varying signals.
- It is hard to globally evaluate the frequenncy domain behavior ofa signal
- We use a moving window to select different blocks of the signal
- Then compute the DTFT at the given time.

### Definition
$$ \bar{X}[n,\lambda) = \sum_{m=-\infty}^{\infty}x[n+m]w[m]e^{-j\lambda m} $$
- Complex-valued function of two variables.
    - discrete time $n$
    - continuous frequency $\lambda$

### Discrete Time STFT
In reality, we approximate the STFT using discrete time sampling in the frequency domain.

$$ \bar{X}[n,\lambda] = \sum_{m=0}^{L-1} x[n+m]w[m]\exp\left\{ -j\frac{2\pi k m}{N} \right\} $$
$$ \bar{X}[n, k] = \sum_{m=0}^{N-1} x[n+m]w[m]W_N^{km} $$
- $L$ is the length of a window, and we assume $N > L$.

There is no need to move the window one step at a time, we can perform sub-sampling in time domain to simplify computation. Let $R$ be the step size of frame shift
$$ \bar{X}[r,k] = \bar{X}[rR,k] $$

## Filter-bank Interpretation
### STFT as a Convolution
Recall
$$ \bar{X}[n,k] = \sum_{m=0}^{N-1} x[n+m]w[m]\exp\left\{ -j\frac{2\pi km}{N} \right\} $$
Let
$$ h_k[n] = w[-n]\exp\left\{ j\frac{2\pi kn}{N} \right\} $$
Then
$$h_k[n] * x[n] = \bar{X}[n,k]$$
Notice that $h_k[n]$ depends on both $n$ and $k$, so different $k$ represents different filters.
- Before FFT, the STFT is implemented by a filter bank.

### Uncertainty in Time-Frequency Localization
The filter bank interpretation reveals a trade-off in constructing $h_k[n]$.
- To get higher time-domain localization, we want the window to be narrower.
    - However, this will lead to a poor frequency-domain resolution.
- To get higher frequency-domain localization, we want the window to be wider.
    - However, this will lead to a poor time-domain resolution.
- High time-domain resolution and high freq-domain resolution cannot be achieved at the same time.

## Invertibility and Practical Inversion
**Fact.** The inversion of STFT is non trivial. The inversion sometimes does not even exist.

Let $R$ be the the window shift and let $L$ be the window length.

- When $R>L$, obviously the ISTFT does not exist.
- When $R<L$, the inverse mapping may not be unique.
    - Overlaps between windows cause problems.
- When $R=L$, the STFT fall backs to DFT and is invertible.

### Definition
The STFT of $x$ is invertible provided that at least one entry of the window $w[m]$ is non-zero.

So we can perform the IDTFT on one frame.
$$ x[n+m]w[m]=\frac{1}{2\pi}\int_{-\pi}^{\pi}\bar{X}[n,\lambda)\exp(j\lambda m)\mathrm{d}\lambda $$

By fixing $w[m]$ to an entry that is non-zero, we can reconstruct $x[n]$.

The same argument applies to discrete-time STFT
$$ x[n+m]w[m]=\frac{1}{N}\sum_{k=0}^{N-1}\bar{X}[n,k]\exp\left( j\frac{2\pi km}{N} \right) $$

### Naive Inverse Approach
$$x_r[n] =\begin{cases}
\frac{1}{Nw[n-rR]}\sum_{k=0}^{N-1}\exp\left(j\frac{2\pi k(n-rR)}{N}\right) &\quad rR \le n \le rR + L - 1\\
0 &\quad o.w.
\end{cases}$$

- Notice that when $R<L$, there will be overlaps, so one sample can be reconstructed from multiple windows.

### Practical Approach: Overlap and Add
IDFT gives
$$ \hat{x}_r[m] = x[rR+m]w[m] $$

We can shift back by $rR$ and add them up
$$ \hat{x}_{OLA} = \sum_r $$
`NotImplementedError: Too Fast.`

Windows used in OLA method
- Bartlett (triangle) window
- Hann window

### Practical Approach: Minimum Norm Approach
Want to construct a signal that is as close to the original signal as possible.

Take a $l_2$ norm as example
$$ \min_x\sum_{r,k}\| S\{x\}[r,k] - X[r,k] \|^2 $$