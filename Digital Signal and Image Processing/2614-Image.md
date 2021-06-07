# AI2614 Digital Signal and Image Processing
> Digital Image Processing

[TOC]

# Fundamentals of Digital Images
- Natural image: The intercept of a 3D object on a 2D image plane.

## Image Processing Pipeline
1. acquisition
2. enhancement (preprocessing)
3. restoration
4. morphological processing
5. other task-specific procedures

## Human Visual System
> Sensor — Network — Compute

- contrast
- exposure
- illusion

## Acquisition and Representation of Digital Images
### Acquisition: Sampling and Quantization
#### Sampling
- Sample a discrete sample $f[x,y]$ of a continuous image $f(x,y)$.
- Each element of the array is a **pixel**.
- loss of information when downsampling

#### Quantization
- use a finite number of bits to represent real values.
- loss of information when rounding.

#### Aliasing
Not to confuse with the aliasing in signal processing.
- Aliasing occurs at edges of graphics
- Anti-Aliasing: bi-linear interpolation or bi-cubic interpolation.

#### Color Components
A colored image consists of 3 channels
- Red $R[x,y]$
- Green $G[x,y]$
- Blue $B[x,y]$

Cannot process each channel separately and combine the results. The distributions of the channels are different and therefore will cause undesired results.

For monochromatic images, the 3 channels can be considered to have the same distribution and therefore can be processed together.

# Intensity Transformation and Spatial Filtering
## Basics
What is the spacial domain?
- the plane containing the pixels of an image.
- neighborhood.

### Intensity Transformation
$$ g[x,y] = T(f[x,y]) $$

### Spatial Filtering
- mask
- kernel
- template
- window


## Intensity Transformation
### Thresholding
- Useful for segmentation, to isolate an object of interest from a background.

### Kinds of grey level transformation
- Linear
    - Negative
    - Identity
- Logarithmic
    - Log
    - Exponential
- Power (gamma)
    - $N$-th power
    - $N$-th root

### Logarithmic transformation
$$ s = c\log(1+r) $$

Maps a narrow range of low input grey level values into a wider range of output values.

### Gamma transformation
$$ s = cr^{\gamma} $$

Maps a narrow range of dark/bright input values into a wider range of output values.

# Histogram Processing
## Image Histogram
Represents the relative frequency of occurrence of the various gray level of the image.

## Histogram Equalization
### Improving Contrast
Improving the contrast of an image is spreading its histogram into a wider range.

Spreading out the frequencies in an image (or equalizing the image) is a simple way to improve dark or washed out images.

In other words, we need to implement a mapping such that any arbitrary input pdf (histogram) can be converted to a uniform distribution.
 
### Continuous Case
Let $p_r(s)$ be the input histogram (pdf), let $p_s(s)$ be our desired equalized output.

Assume $s=T(r)$, the relationship between input and output pdf is
$$ p_s(s) \left| \frac{\mathrm{d}T(r)}{\mathrm{d}r} \right| = p_r(r) $$

We want $p_s(s)$ to be a constant (uniform distribution). Suppose the range of input is from $0$ to $L-1$, then we can set $p_s(s) = 1/(L-1)$ for all $s$ and integrate over $r$
$$ T(r) = (L-1)\int_{0}^{r}p_r(w)\mathrm{d}w $$

- Slope of $T(r)$ gives the amplification. The higher the value is in the original pdf, the larger the amplification.

### Discrete Case
The pixels of digital images are usually quantized.
$$ p_r(r_k) = \frac{n_k}{MN} $$

If we rewrite the integral to a summation
$$ s_k = T(r_k) = (L-1)\sum_{j=0}^kp_r(r_j) = \frac{L-1}{MN}\sum_{j=0}^kn_j $$

This can give a quite good result, but not optimal. Performing equalization is non-trivial in discrete case.

Instead of smoothing the original pdf into a uniform distribution, the summation only adjusts the distances between the bins.
- Bins with high frequencies are “separated”
- Bins with low frequencies are “compressed”

> “洗白了、washed out、over-exposure” —- Yuye Ling

## Histogram Specification
In addition to uniform distribution, we can also specify other distributions (e.g. Gaussian) and force the processed image to have a specified histogram distribution.

## CLAHE: Contrast-Limited Adaptive Histogram Equalization
> Cost-Limited Adaptive Healthy Eating

In discrete case, histogram equalization may fail to produce a desired output.
- Vanilla HE will assign the best contrast to the dominant gray levels regions.
- Because slope of $T(r)$ gives the scale of amplification.

### Contrast Limitation
- We want to limit the amplification given by $T(r)$: this is equivalent to clipping the height of the histogram.
    - But clipped histogram (pdf) does not sum up to 1.
    - So we compensate the clipped values by increasing all values in the pdf.
        - clipped parts now have smoother slopes.
        - originally low frequency parts now have sharper slopes.
- Contrast Limiting is simply histogram specification.

### Adaptive
- Perform histogram equalization in a small neighborhood.
- Use interpolation to stitch them up.

# Fundamentals of Spatial Filtering
## Neighborhood Operations
Neighborhood operations operate on a larger neighborhood of pixels, instead of operating on single points.

## Filtering vs Convolution
Filtering in MATLAB. Filtering is like correlation.
$$ g[m,n] = \sum_{k}\sum_{l}h[k,l]f[m+k,n+l] $$

Convolution in MATLAB
$$ g[m,n] = \sum_{k}\sum_{l}h[k,l]f[m-k,n-l] $$

## Image Smoothing
- Averaging all pixels in a neighborhood.
- Useful in removing noise
- Linear

### Simple Averaging Filter
### Weighted Averaging Filter
### Gaussian Filter

## Nonlinear Filtering
### Minimum Filtering
### Maximum Filtering
### Median Filtering
- Useful in cancelling pepper-salt noises.

## Edge Effect
How to pad.

### Zero Padding
May cause edge effects.

### Replicate
Pad with replicating edge pixels

### Wrap Around Edges
Assume the image is “periodic”, and pad with periodic extension.

# 2D Fourier Transforms and Spectral Filtering
## Fourier Transforms and Spatial Frequencies in 2D
### Definition
$$ F(u,v) = \int\int f(x,y)e^{-j2\pi (ux+vy)}\mathrm{d}x\mathrm{d}y $$

$$ f(x,y) = \int\int F(u,v)e^{j2\pi (ux+vy)}\mathrm{d}u\mathrm{d}v $$

- $u$ and $v$ are spatial frequencies.
- In many cases, $f(x,y)$ can be separated into $f(x)f(y)$, and the calculation will be easier as the integral can be separated.
- $F(u,v)$ is complex in general.
- We decompose signals into basis $\{\exp\left\{ -j\pi (ux+vy) \right\}\}$

### Important FT Pairs
#### Rectangle Centered at Origin
Consider a rectangle centered at origin with length $X$ and width $Y$.
$$f(x,y) = \begin{cases}
1 & \quad |x| \le X/2, |y| \le Y/2\\
0 & \quad o.w.
\end{cases}$$

Plug into definition
$$ F(u,v) = XY\left[\frac{\sin(\pi u X)}{\pi u X}\right]\left[\frac{\sin(\pi v Y)}{\pi v Y}\right] $$

#### Gaussian Centered at Origin
The Fourier Transform of a (Univariate) Gaussian distribution is still a Gaussian distribution.

We start from the FT of 1d Gaussian
$$ f(t)=\exp\{ -\pi t^2 \} $$

By definition of Fourier transform
$$ F(f) = \int f(t)\exp\{-j2\pi ft\}\mathrm{d}t $$

$$ \begin{align*}
F(f) &= \int \exp\{ -\pi ((t+jf)^2 + \pi f^2) \} \mathrm{d}t\\
&= \exp(-\pi f^2) \int \exp\{ -\pi(t+jf)^2 \}\mathrm{d}t
\end{align*}$$

The latter integral equals to $1$ (cdf of a Gaussian Distribution). Therefore
$$ F(f) = \exp\{-\pi f^2\} $$

For 2d the case is similar.

#### Circular Disk Centered at Origin
Suppose the disk has unit height and unit radius.
$$f(r)=\begin{cases}
1 & \quad |r| < a\\
0 & \quad |r| \ge a
\end{cases}$$

Consider $x=r\cos\theta$, $y=r\sin\theta$, $u=\rho\cos\varphi$, $v=\rho\sin\varphi$.
$$ F(\rho, \varphi) = \int\int f(r,\theta)\exp(-j2\pi \rho r(\cos\theta\cos\varphi + \sin\theta\sin\varphi))\mathrm{d}r\mathrm{d}\theta $$

Therefore
$$ F(\rho,\varphi) = \int_{0}^ar\mathrm{d}r\int_0^{2\pi}\exp(-j2\pi \rho r \cos(\theta-\varphi))\mathrm{d}\theta $$

The integral does not have analytical solution. Define Bessel function
$$ J_0(x) = \frac{1}{2\pi}\int_0^{2\pi}\exp(-jx\cos(\theta-\varphi))\mathrm{d}\theta $$

Therefore
$$ F(\rho,\varphi) = \int_0^a 2\pi J_0(2\pi\rho r)r\mathrm{d}r = aJ_1(\pi a \rho)/\rho $$

- Bessel functions $J_1()$ are usually considered similar to sinusoids. And $J_1(x)/x$ is called the **Jinc Function**

#### Delta Function (Impulse)
$$ f(x,y) = \delta(x,y) = \delta(x)\delta(y) $$

$$F(u,v) = 1$$

#### Symmetric Delta Function Pairs
Corresponds to sinusoids.

### 2D Fourier Transform on Images
Usually the 2D FT of natural images have a Gaussian distribution. In many cases, structured patterns (symmetric peaks, etc.) corresponds to the image of some artifacts.

### Magnitude vs Phase
- Magnitude: informative. Amplitude of sinusoids.
- Phase: less intuitive. May have similar patterns with the magnitude spectrum, but looks messy due to random noises.

$$ \angle\left( \sum ae^{-j2\pi t} + n \right) $$

- For regions with high snr, magnitude and phase spectrums have similar pattens
    - the magnitude of an image usually decreases with the frequency
- For regions with low snr, random noise dominates the phase.
    - the phase of an image is generally uniformly distributed

However, phases are important because they contain more information about the original image.

## Convolution Theorem and Frequency Filtering
**Filtering** in the frequency domain consists of modifying the Fourier Transform of an image and the Inverse Fourier Transform of the modified spectrum.

### 2D Convolution Theorem
For an LTI system
$$ f(x,y)*h(x,y) = F(u,v)H(u,v) $$

**Linear** spatial filtering operations can be carried out by multiplications in the Fourier domain.
- Nonlinear filtering such as median filtering cannot be performed in frequency domain.

#### Basic Steps
1. Compute FT
2. Multiply FT’s
3. IFT

#### Technical Details
- How to multiply if the size of images and kernels are different
    - Padding. But in frequency domain or in temporal domain?
        - Temporal domain.
        - Increasing the resolution in frequency domain.
- Some filters may be easier to specify in one domain than in another, due to sampling and quantization.
        
## 2D Sampling
### 2D Sampling Function
$$ \sum_{n=-\infty}^{+\infty}\sum_{m=-\infty}^{+\infty} \delta(x-nX)\delta(y-mY) $$

$$ F(u,v) = \frac{1}{XY} $$

### Aliasing in 2D
Alias occurs if the signal has frequencies above the Nyquist sampling rate.

#### Handling Aliasing
- Increase sample rate: buy new display or new camera. (`NoMoneyException`)
- Preprocess: Downsampling or filtering (remove high frequencies)

# Image Restoration
## Image Degradation
### Degradations
- Optical Blur
- Motion Blur
- Spatial Quantization
- Additive Intensity Noice

### Formulation
#### Overview
We can assume that the pattern of blurred point is preserved

Therefore imaging can be modeled as an LSI system.
- the convolution kernel is called the **point spread function** (PSF).

#### Maths: Inverse Problem
An observed image can be modeled as
$$ g(x,y) = h(x,y) * f(x,y) + n(x,y) $$

where $h$ is the PSF of the imaging system, and $n$ is the additive noise.

Observing $g$, we want to solve for $f$, but this problem is non-trivial.

#### Challenge: Loss of Information
Take a Gaussian filter for example, the filter dropped many information in high frequencies.

Knowing the output and solving for the input is underdetermined.

So we need many assumptions and priors.

## Image Restoration
### Inverse Filtering
#### 1D Vector Explanation
Consider $g=h*f$, if we ignore the boundaries, it can be re-written into matrix form
$$ g = Af $$

where $A$ can be constructed from $h$.

So the problem is solved by inverting $A$.
$$ f=A^{—1}g $$

- Matrix inversion is difficult.
- If the boundary is not ignored, then $A$ is not a square matrix, and we have to use pseudo-inverse.

#### Fourier Perspective: Inverse Filtering
$$ G = HF + N $$

If we ignore the noise $N$,
$$ \hat{F} = G/H $$
- works perfectly fine if there is no noise
- fails immediately if noise exists

#### Noise Amplification
If noise exists
$$ \hat{F} = F + N/H $$

As we divide $N$ by $H$, the noise gets amplified and dominates high frequencies, because $1/H$ has larger values in high frequencies.

### Wiener Filtering
Still applies inverse kernel, but avoids divide-by-zero by adding damping factors.
$$ \hat{F} =\frac{|H|^2}{|H|^2+1/SNR}\cdot\frac{G}{H} = \frac{H^*}{|H|^2+K}\cdot G $$
where the first term is an amplitude-dependent damping factor.
- If $K=0$, Wiener Filtering reduces to standard inverse filtering.
- Choosing $K$
  - Manual parameter tuning
  - Prior: Choose some part of the image that is assumed to be uniformly distributed, and estimate SNR in that region.
  - BM3D: State-of-the-art
- Intuitively, Wiener filtering drops frequencies that is considered dominated by noises.

#### Maths
Wiener filter is designed to minimize the mean squared error
$$ E = \iint |f(x,y)-\hat{f}(x,y)|^2\mathrm{d}x\mathrm{d}y $$
- Assumes the noise is additive Gaussian noise

By Parseval’s Theorem
$$ E = \iint |F(u,v) - \hat{F}(u,v)|^2\mathrm{d}u\mathrm{d}v $$
where $\hat{F}=WG=WHF-WN$

Therefore
$$F-\hat{F}=(1-WH)F-WN$$

$$E=\iint |(1-WH)F-WN|^2\mathrm{d}u\mathrm{d}v$$

If we assume the two terms are not correlated,
$$ E=\iint |(1-WH)F|^2+|WN|^2\mathrm{d}u\mathrm{d}v $$

To minimize the error, we take the derivative with respective to $W$.
$$ 2(-(1-W^*H^*)F^*HF+W^*N^*N)=0 $$

#### Example: Motion Blur
The motion blurring can be modeled as a shift-and-add process
$$ g = \frac{1}{T}\int_{-T/2}^{T/2}f(x-x_0(t),y)\mathrm{d}t $$

To apply Wiener filtering, we need to derive $H$. By definition and properties of Fourier transform
$$ G = \frac{1}{T} \int_{-T/2}^{T/2}Fe^{-j2\pi{}ux_0(t)}\mathrm{d}t $$

Therefore
$$ H = \frac{1}{T}\int_{-T/2}^{T/2}e^{-j2\pi{}ux_0(t)}$$

Suppose $x_0(t)=st$,
$$ H = \textrm{sinc}(\pi{}ud) $$

So $H$ still have zeros, and we should use Wiener filtering.

### MAP Formulation
`NotImplementedError: 讲不完力`