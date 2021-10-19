# Image Processing

---

> Part 0: Preliminary

---

## Functional Interpretation of an Image

- $f(x,y)$ is the image intensity at $(x,y)$.
- Image processing is a transoformation $t$: $t(f(x,y))$.

## Linear Shift-Invariant Systems

- Ideal lens is an LSI system
  - Defocuesd Image $g$ is a processed version of Focused Image $f$.
  - Linearity: Variation in brightness
  - Shift: Movement of scenes

## Unit Impulse Function

$$\delta(x)=\begin{cases}
    1/2\varepsilon \quad & |x| \le \varepsilon\\
    0 \quad & |x| > \varepsilon
\end{cases} \quad (\varepsilon\to 0)$$

- $\int \delta(x) \mathrm{d}x = 1$
- $\delta(x)*h(x) = h(x)$

---

> Part 1: Spatial Processing

---

## Pixel-level processing

- darken $f-128$
- lighten $f + 128$
- invert $255-f$
- low contrast $f/2$
- high constrast $f * 2$
- gray $0.3f_R+0.6f_G+0.1f_B$

## Convolution

### 1D Convolution

$$f(t) * h(t) = \int f(\tau)h(t-\tau)\mathrm{d}\tau$$

- *Convolution implies LSI and LSI implies convolution.*

### 2D Convolution

$$ g(x,y) = \iint f(u,v)h(x-u,y-v)\mathrm{d}u\mathrm{d}v $$

$$ g[i,j] = \sum_{n=1}^M\sum_{n=1}^N f[m,n]h[i-m, j-n] $$

### Border Problem and Padding

- Ignore border
- Pad with constants
- Pad with reflection

> “我们的爱因斯坦，爱酱”

## Spatial Filtering

- Impulse filtering
- Mean filtering
  - Orig - MeanFilter = Sharpened
- Box filtering
  - Does not look natural
  - Has blocky artifacts
- Fuzzy filter (Gaussian filtering)

### Gaussian Kernel

$$ n_{\sigma}[i,j] = \frac{1}{2\pi\sigma^2}e^{-\frac{i^2+j^2}{2\sigma^2}} $$

- Rule of Thumb: $KernelSize=2\pi\sigma$
- Larger kernel (or $\sigma$) results in more blurring

#### Separability of Gaussian Filter

$$g[i,j] = \frac{1}{2\pi\sigma^2}\sum_{m=-K/2}^{K/2}\sum_{n=-K/2}^{K/2}e^{-\frac{m^2+n^2}{2\sigma^2}}f[i-m, j-n] $$

$$ g[i,j] = \frac{1}{2\pi\sigma^2}\sum_m e^{-\frac{m^2}{2\sigma^2}}\cdot\sum_ne^{-\frac{n^2}{2\sigma^2}}f[i-m,j-n] $$

- A 2D Gaussian filter can be equivalently replaced by two 1D Gaussian filters
  - Lower time complexity

### Denoise with Smoothing

- Problems with Gaussian smoothing
  - Sensitive to outliers
  - Smoothens edges

#### Median Filtering

- Sort the $K^2$ values in window centered at the pixel
- Assign the median to the pixel
  - Can handle Salt and Pepper Noise
- Non-linear (involves sorting)
  - Cannot be implemented by convolution
- Drawbacks
  - Not effective when the noise is not simply salt and pepper
  - Large kernel also blurrs edges

#### Bilateral Filter

##### Gaussian Filtering Revisited

- If we apply the same Gaussian Kernel everywhere, it will blur the edges
  - Because the filter has no knowledge of foregrounds and backgrounds
- Solution
  - Add weight
  - Bias Gaussian Kernel s.t. pixels that are not similar in intensity to the center pixel have smaller weight

##### Gaussian Filtering

$$ g[i,j] =\frac{1}{W_{sb}} \sum_m\sum_n f[m,n]n_{\sigma_s}[i-m,j-n]n_{\sigma_{b}}(|f[m,n]-f[i,j]|) $$

- $n_{\sigma_s}$ is the regular spatial Gaussian filter
- $n_{\sigma_b}$ is the brightness Gaussian, used for adjusting weights
  - similar pixels have higher weights
  - non-similar pixels have lower weights
  - If $\sigma_b \to \infty$, the bilateral filter reduces to ordinary Gaussian filter.
- Non-linear operation, cannot use convolution

> “雀斑都去掉了，五官都保留了。非常好。”
> “磨皮磨得有点过。”

## Template Matching

> “经典得现在都已经没有人用了”

*How do we locate a target template $t$ in an given image $f$?*

### Formulation

Minimize

$$ E[i,j] = \sum_m\sum_n\left(f[m,n]-t[m-i,n-i] \right)^2 $$

which is equivalent to maximizing

$$ f[m,n]t[m-i,n-j] $$

### Cross-Correlation

$$ t \otimes f = R_{tf}[i,j] = \sum_m\sum_nf[m,n]t[m-i,n-j] $$

#### Convolution and Correlation

Correlation

$$ t \otimes f = \sum_m\sum_n f[m,n] t[m-i,n-j] $$

Convolution

$$ t * f = \sum_m\sum_nf[m,n]t[i-m,j-n] $$

#### Normalization

- Problem with Cross-Correlation
  - Unnormalized input can give erroneous results

$$ N_{tf}[i,j] = \frac{t \otimes f}{\|f\|_2\cdot\|t\|_2} $$

#### Drawbacks

- Border problem
- Sensitive to object pose, scale and rotation
- Not good for general object detection
  - Can only match templates
- Can be computationally expensive

---

> Part 2: Spectral Processing

---

## 2D Fourier Transform

> Any periodic function can be rewritten as a **weighted sum** of **infinite sinusoids** of different frequencies.

`LazyError: Refer to AI2614 DSIP`
