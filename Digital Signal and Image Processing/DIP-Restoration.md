# Fundamentals of Image Restoration

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
$$ g = \frac{1}{T}\int\_{-T/2}^{T/2}f(x-x_0(t),y)\mathrm{d}t $$

To apply Wiener filtering, we need to derive $H$. By definition and properties of Fourier transform
$$ G = \frac{1}{T} \int\_{-T/2}^{T/2}Fe^{-j2\pi{}ux_0(t)}\mathrm{d}t $$

Therefore
$$ H = \frac{1}{T}\int\_{-T/2}^{T/2}e^{-j2\pi{}ux_0(t)}$$

Suppose $x_0(t)=st$,
$$ H = \textrm{sinc}(\pi{}ud) $$

So $H$ still have zeros, and we should use Wiener filtering.

### MAP Formulation

`NotImplementedError: 讲不完力`
