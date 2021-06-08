# Short Time Fourier Transform and Spectral Analysis

[TOC]

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

### Definition of STFT

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
$$
h_k[n] * x[n] = \bar{X}[n,k]
$$

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

### Definition of ISTFT

The STFT of $x$ is invertible provided that at least one entry of the window $w[m]$ is non-zero.

So we can perform the IDTFT on one frame.
$$ x[n+m]w[m]=\frac{1}{2\pi}\int_{-\pi}^{\pi}\bar{X}[n,\lambda)\exp(j\lambda m)\mathrm{d}\lambda $$

By fixing $w[m]$ to an entry that is non-zero, we can reconstruct $x[n]$.

The same argument applies to discrete-time STFT
$$ x[n+m]w[m]=\frac{1}{N}\sum_{k=0}^{N-1}\bar{X}[n,k]\exp\left( j\frac{2\pi km}{N} \right) $$

### Naive Inverse Approach

$$
x_r[n] =\begin{cases}
\frac{1}{Nw[n-rR]}\sum_{k=0}^{N-1}\exp\left(j\frac{2\pi k(n-rR)}{N}\right) &\quad rR \le n \le rR + L - 1\\
0 &\quad o.w.
\end{cases}
$$

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
