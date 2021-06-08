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

$$
X(j\Omega) = \begin{cases}
    something, &\quad |\Omega| \le \Omega_0\\
    0, &\quad |\Omega| > \Omega_0
\end{cases}
$$

Therefore the spectrum can be re-written as
$$ X(j\Omega) = X(j\Omega)\cdot\mathrm{rect}\left( \frac{\Omega}{\Omega_0} \right) = X_p(j\Omega)\cdot\mathrm{rect}\left( \frac{\Omega}{\Omega_0} \right) $$
where $X_p(j\Omega)$ is constructed by periodically extending $X(j\Omega)$

Since $X_p(j\Omega)$ is periodic, we can expand it by its Fourier series
$$X_p(\Omega) = \sum_{n=-\infty}^{+\infty} x[n]\exp(j2\pi n \Omega/\Omega_0)\cdot\mathrm{rect}\left( \frac{\Omega}{\Omega_0} \right)$$

The inverse Fourier transform is then given by
$$x(t) = \left( \sum_{n=-\infty}^{+\infty}x[n]\delta(t-nT_0)\right) * \Omega_0\mathrm{sinc}(\Omega_0t)$$

### Aliasing

What happens to the sinc function when aliasing occurs?

- With increased signal frequency, the sinc function can no longer span the signal space
- Therefore aliasing occurs

#### Anti-Aliasing Filters

### Interpolating with Different Bases

#### Piecewise Constant

$$ V = \{ \text{piecewise constant functions on intervals } [kT, (k+1)T] \} $$

#### Linear

$$ V = \{ \text{piecewise linear functions on intervals } [kT, (k+1)T] \} $$

### Brief Remarks on Sampling

- Theoretically, it is impossbile to reconstruct the original continuous-time signal from its finite samples
- However, based on
  - Our knowledge about the signal
  - Our tolerance on the resonstruction accuracy
  - We could design a proper basis and kernel to represent and reconstruct the signal

## Discrete-Time Processing of Continuous-Time Signals

### Basic Workflow

Theoretically,

- Sample CT signal
- Do DT processing
- Interpolate back to CT signal

But this process is **seriously non-trivial**

C/D convertion: $x[n] = x_c(nT)$
The DFTF of $x[n]$ is
$$X(e^{j\omega}) \frac{1}{T}\sum_{-\infty}^{+\infty}X_c\left[ j\left( \frac{\omega}{T} - \frac{2\pi k}{T} \right) \right]$$

D/C conversion: $y_r(t) = \sum_{n=-\infty}^{+\infty}y[n]\frac{\sin[\pi(t-nT)/T]}{\pi(t-nT)/T}$
The DTFT of $y[n]$ is realted to the FT of $y_r$ by
$$Y_r(j\Omega) = H_r(j\Omega)Y(e^{j\Omega T})$$

If the DT system is LTI, we have
$$ Y(e^{j\Omega T}) = H(e^{j\Omega T})X(e^{j\Omega T}) $$

If $X_c$ is bandlimited, there is no aliasing, and
$$Y_r(j\Omega) = H(e^{j\Omega T})X_c(j\Omega)$$

- $x_c(t)$ must be bandlimited
- C/D must satisfy Nyquist sampling theorem.
- DT system must be LTI

### Low-Pass Filtering before Sampling

By applying a low-pass filter in the spectral domain, we will be able to sample signals that are originally impossible to sample, but this comes with the cost in precision.

## Quantization

- Input/output quantization
- Filter coefficient quantization
- Product roundoff
- (Potential) overflow in sums

Notice that quantization makes the system nonlinear. To make our analysis tractable, denote the quantized value as
$$\hat{x} = \mathcal{Q}(x) = x + \epsilon$$
where $\epsilon$ is the quantization error.

Define $\Delta = \frac{2X_m}{2^{B+1}} = \frac{X_m}{w^B}$ where $2X_m$ is the full-scale range of quantizer and $B+1$ is the number of quantizer bits.

Therefore the quantizer can be seen as the addition of original signal $x[n]$ and noise signal $e[n]$

- $e$ is uniformly distributed random variable between $-\Delta/2$ and $\Delta/2$
- $e$ is a stationary stochastic process, its statistics do not change over time
- $e$ is a white sequence, uncorrelated with $e[m]$ for all $n \neq m$
- $e$ correlated with $x$

### Major Types of Quantization

- Truncation
- Rounding
