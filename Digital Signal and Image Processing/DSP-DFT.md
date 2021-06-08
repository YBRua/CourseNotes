# DFT

## Discrete Fourier Series

## Discrete Fourier Transform

## Properties of DFT

### Complex Conjugate

$$x^*[n] \leftrightarrow X^*[((-k))_N]$$

### Conjugate Symmetry of Real signals

$$ x[n]=x^*[n] \leftrightarrow X[k] = X^*[((-k))_N] $$

#### even-length

|       $k$       | -4  | -3  | -2  | -1  |  0  |  1  |  2  |  3  |
| :-------------: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|     $X[k]$      |  a  |  b  |  c  |  d  |  a  |  b  |  c  |  d  |
| $X^*[((-k))_N]$ |  a  |  d  |  c  |  b  |  a  |  d  |  c  |  b  |

In this case:

- For $k = 2m$, $X[k]$ must be real values
- For $k = 2m+1$, $X[k]$ and $X^*[((-k))_N]$ must be complex conjugates

#### odd-length

|       $k$       |  0  |  1  |  2  |  3  |  4  |
| :-------------: | :-: | :-: | :-: | :-: | :-: |
|     $X[k]$      |  a  |  b  |  c  |  d  |  e  |
| $X^*[((-k))_N]$ |  a  |  e  |  d  |  c  |  b  |

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

| m        | 0   | 1   | 2   | 3   | 4   | 5   | 6   |
| -------- | --- | --- | --- | --- | --- | --- | --- |
| $x_1[m]$ | 1   | 1   | 1   | 1   | 1   | 0   | 0   |
| $x_2[m]$ | a   | 0   | 0   | 0   | d   | c   | b   |

- $n=1$

| m        | 0   | 1   | 2   | 3   | 4   | 5   | 6   |
| -------- | --- | --- | --- | --- | --- | --- | --- |
| $x_1[m]$ | 1   | 1   | 1   | 1   | 1   | 0   | 0   |
| $x_2[m]$ | b   | a   | 0   | 0   | 0   | d   | c   |

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

$$
x[n]*h[n] =
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
