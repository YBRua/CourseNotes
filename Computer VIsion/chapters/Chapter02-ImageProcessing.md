# Image Processing

> Part 0: Preliminary

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

> Part 1: Spatial Processing

## Pixel-level processing

- darken $f-128$
- lighten $f + 128$
- invert $255-f$
- low contrast $f/2$
- high constrast $f * 2$
- gray $0.3f_R+0.6f_G+0.1f_B$

## Convolution

$$f(x) * h(x) = \int f(\tau)h(t-\tau)\mathrm{d}\tau$$

- *Convolution implies LSI and LSI implies convolution.*

> Part 2: Spectral Processing
