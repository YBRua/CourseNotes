# DFT

- [DFT](#dft)
  - [Discrete Fourier Series](#discrete-fourier-series)
    - [From DTFT to DFS](#from-dtft-to-dfs)
    - [Kernel: Root of Unity](#kernel-root-of-unity)
      - [Properties of $W_N$](#properties-of-w_n)
    - [Definition of DFS](#definition-of-dfs)
    - [Properties of DFS](#properties-of-dfs)
      - [Linearity](#linearity)
      - [Shift of a Sequence](#shift-of-a-sequence)
      - [Duality](#duality)
    - [Remarks on DFS](#remarks-on-dfs)
  - [Discrete Fourier Transform](#discrete-fourier-transform)
    - [Definition of DFT](#definition-of-dft)
      - [Implicit Periodicity](#implicit-periodicity)
    - [Matrix Interpretation of DFT](#matrix-interpretation-of-dft)
      - [A Deeper Functional Insight](#a-deeper-functional-insight)
    - [Properties of DFT](#properties-of-dft)
      - [Linearity](#linearity-1)
      - [Circular Time Shift](#circular-time-shift)
      - [Circular Frequency Shift](#circular-frequency-shift)
      - [Complex Conjugate](#complex-conjugate)
      - [Conjugate Symmetry of Real signals](#conjugate-symmetry-of-real-signals)
        - [even-length](#even-length)
        - [odd-length](#odd-length)
      - [DFT and IDFT](#dft-and-idft)
    - [Circular Convolution](#circular-convolution)
      - [Recap: Linear Convolution](#recap-linear-convolution)
      - [Definition of Circular Convolution](#definition-of-circular-convolution)
      - [Linear Convolution with DFT](#linear-convolution-with-dft)
      - [Block Convolution: Overlap-Add Method](#block-convolution-overlap-add-method)

## Discrete Fourier Series

### From DTFT to DFS

DTFT is continuous, and used to evaluate signal with infinite length. So it cannot be directly applied in digital signal processing.

- One possible approach is to sample DTFT in the frequency domain
  - Replace $\omega$ by $2\pi/T$
  - Sample $T$ for $N$ times
- If we are only interested in discrete signal with finite length
  - For continuous frequency $\omega$, the selection of $T$ is infinite
  - For sampled version, the selection of $N/k$ is finite

### Kernel: Root of Unity

The DFS uses a new kernel in the frequency domain
$$ \{W_N^{kn}\} = \exp\left( -j\frac{2\pi k}{N}n \right) $$

where
$$ W_N \triangleq e^{-j2\pi/N} $$

is called the **$N$-th Root of Unity**

#### Properties of $W_N$

- $W_N^0 = W_N^N = W_N^{2N} = \cdots = 1$
- $W_N^{k+N} = W_N^k$
- $\sum_{n=0}^{N-1}W_N^{kn} = N\delta[k]$

### Definition of DFS

$$ \tilde{X}[k] = \sum_{n=0}^{N-1}\tilde{x}[n]W_N^{kn} $$

### Properties of DFS

#### Linearity

$$ \alpha_1x_1[n] + \alpha_2x_2[n] \leftrightarrow \alpha_1X_1[k] + \alpha_2X_2[k] $$

#### Shift of a Sequence

$$ x[n-m] \leftrightarrow X[k]W_N^{km} $$

#### Duality

If $x[n] \leftrightarrow X[k]$, then
$$ X[n] \leftrightarrow Nx[-k] $$

### Remarks on DFS

- The DFS is **periodic in both domains**

## Discrete Fourier Transform

### Definition of DFT

Let $x[n]$ be a finite signal ranging from $0$ to $N-1$, then its DFT is given by
$$ X[k] = \sum_{n=0}^{N-1}x[n]W_N^{kn} $$

and the inverse DFT is
$$ x[n] = \frac{1}{N}\sum_{k=0}^{N-1}X[k]W_N^{-kn} $$

#### Implicit Periodicity

Always remember that the DFT/IDFT is implicitly defined over the entire space by **periodic extension**, so it always implicitly assumes that the input signal is periodic.

- So we may need to pad zeros after the original input.
- As we increase padding (or equivalently, increase $N$), the DFT will asymptotically approach DTFT.
  - By extending the length of input sequence in time domain, the spectral sampling interval is reduced, and the digital resolution is improved.

### Matrix Interpretation of DFT

The DFT can also be interpretated in the matrix form

$$
\begin{bmatrix}
  X[0]\\ X[1]\\ X[2]\\ \vdots\\ X[N-1]
\end{bmatrix} =
\begin{bmatrix}
  1 & 1 & 1 & \cdots & 1\\
  1 & W_N^1 & W_N^2 & \cdots & W_N^{N-1}\\
  1 & W_N^2 & W_N^4 & \cdots & W_N^{2(N-1)}\\
  \vdots & \vdots & \vdots & \ddots & \vdots\\
  1 & W_N^{N-1} & W_N^{2(N-1)} & \cdots & W_N^{N(N-1)}\\
\end{bmatrix}
\begin{bmatrix}
  x[0]\\ x[1]\\ x[2]\\ \vdots\\ x[N-1]
\end{bmatrix}$$

Or equivalently
$$ \mathbf{X} = \mathbf{F}\mathbf{x} $$

where $\mathbf{F}$ is the DFT matrix.

#### A Deeper Functional Insight

Decompose $\mathbf{F}$ by its rows
$$\mathbf{F} = \begin{bmatrix}
  \varphi_0^*\\ \varphi_1^*\\ \vdots\\ \varphi_{N-1}^*
\end{bmatrix}$$

Similarly
$$\mathbf{F}^* = \begin{bmatrix}
  \varphi_0 & \varphi_1 & \cdots & \varphi_{N-1}
\end{bmatrix}$$

- $\varphi_n$ are the basis in the time domain

Obviously $\mathbf{F}\mathbf{F}^* = N\mathbf{I}$

- $\frac{1}{\sqrt{N}}\mathbf{F}$ is a unitary matrix

### Properties of DFT

#### Linearity

Directly inherited from the DFS

#### Circular Time Shift

$$ x[((n-m))_N] \leftrightarrow X[k]W_N^{km} $$

#### Circular Frequency Shift

$$ x[n]W_N^{-nl} \leftrightarrow X[((k-l))_N] $$

#### Complex Conjugate

$$x^*[n] \leftrightarrow X^*[((-k))_N]$$

#### Conjugate Symmetry of Real signals

$$ x[n]=x^*[n] \leftrightarrow X[k] = X^*[((-k))_N] $$

##### even-length

|       $k$       | -4  | -3  | -2  | -1  |  0  |  1  |  2  |  3  |
| :-------------: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|     $X[k]$      |  a  |  b  |  c  |  d  |  a  |  b  |  c  |  d  |
| $X^*[((-k))_N]$ |  a  |  d  |  c  |  b  |  a  |  d  |  c  |  b  |

In this case:

- For $k = 2m$, $X[k]$ must be real values
- For $k = 2m+1$, $X[k]$ and $X^*[((-k))_N]$ must be complex conjugates

##### odd-length

|       $k$       |  0  |  1  |  2  |  3  |  4  |
| :-------------: | :-: | :-: | :-: | :-: | :-: |
|     $X[k]$      |  a  |  b  |  c  |  d  |  e  |
| $X^*[((-k))_N]$ |  a  |  e  |  d  |  c  |  b  |

- For $k=0$, $X[0]$ must be a real value
- For other terms, they are complex conjugates

#### DFT and IDFT

We can use DFT to compute IDFT
$$N(\mathrm{IDFT}[X[k]])^* = \mathrm{DFT}[X^*[k]] $$

$$ \mathrm{IDFT}[X[k]] = \left(\frac{1}{N}\mathrm{DFT}[X^*[k]]\right)^* $$

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
2. Pad $x_2$ to length $7$. $x_2'[-n] = [0,0,0,d,c,b,a]$ starting from index $-6$
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
