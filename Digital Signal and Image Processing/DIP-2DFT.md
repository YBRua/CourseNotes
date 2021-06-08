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

$$
f(x,y) = \begin{cases}
1 & \quad |x| \le X/2, |y| \le Y/2\\
0 & \quad o.w.
\end{cases}
$$

Plug into definition
$$ F(u,v) = XY\left[\frac{\sin(\pi u X)}{\pi u X}\right]\left[\frac{\sin(\pi v Y)}{\pi v Y}\right] $$

#### Gaussian Centered at Origin

The Fourier Transform of a (Univariate) Gaussian distribution is still a Gaussian distribution.

We start from the FT of 1d Gaussian
$$ f(t)=\exp\{ -\pi t^2 \} $$

By definition of Fourier transform
$$ F(f) = \int f(t)\exp\{-j2\pi ft\}\mathrm{d}t $$

$$
\begin{align*}
F(f) &= \int \exp\{ -\pi ((t+jf)^2 + \pi f^2) \} \mathrm{d}t\\
&= \exp(-\pi f^2) \int \exp\{ -\pi(t+jf)^2 \}\mathrm{d}t
\end{align*}
$$

The latter integral equals to $1$ (cdf of a Gaussian Distribution). Therefore
$$ F(f) = \exp\{-\pi f^2\} $$

For 2d the case is similar.

#### Circular Disk Centered at Origin

Suppose the disk has unit height and unit radius.

$$
f(r)=\begin{cases}
1 & \quad |r| < a\\
0 & \quad |r| \ge a
\end{cases}
$$

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
