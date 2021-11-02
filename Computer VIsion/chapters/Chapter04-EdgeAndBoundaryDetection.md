# Edge and Boundary Detection

> - What are edges?
> - Rapid changes in image intensity within small region

## Edge Detection Basics

### Causes of Edges

- Surface normal discontinuity
- depth discontinuity
- surface color discontinuity
- illumination discontinuity

### Types of Edges

- Step edges
- Roof edge
- Line edges

### Problems

- Noisy and discrete

### Goal

- Location
- Magnitude
- Orientation

### Gradient

- Represents the direction of most rapid change in intensity

$$ \nabla I = \left[ \frac{\partial I}{\partial x}, \frac{\partial I}{\partial y} \right] $$

#### Magnitude

$$ S = \|\nabla I \| = \sqrt{\left( \frac{\partial I}{\partial x} \right)^2 + \left( \frac{\partial I}{\partial y} \right)^2 } $$

#### Orientation

$$ \theta = \arctan\left( \frac{\partial I}{\partial y}/ \frac{\partial I}{\partial x} \right) $$

#### Finite Difference Approximations

$$ \frac{\partial I}{\partial x} \approx \frac{1}{2\epsilon} ((I[i+1,j+1]-I[i,j+1]) + (I[i+1,j]-I[i,j])) $$

$$ \frac{\partial I}{\partial y} \approx \frac{1}{2\epsilon} ((I[i+1,j+1]-I[i+1,j]) + (I[i,j+1]-I[i,j])) $$

- $\epsilon$ is the distance between two pixels, usually $1$
- Can be implemented as convolution

$$ \frac{\partial}{\partial x} = \frac{1}{2\epsilon}\begin{bmatrix}
    -1 & 1\\
    -1 & 1
\end{bmatrix} $$

##### Common Operators

- Roberts
- Prewitt
- Sobel (3x3)
- Sobel (5x5)

##### Small and Large Operators

- Small
  - Better localization
- Large
  - Better approximation and robustness

#### Non-Maximal Suppression

- Edges are thick after filtering
- Follow gradients and suppress pixels that are exceeded by a neighbor
- Can also use interpolation

#### Thresholding

##### Single Threshold

- $\|\nabla I(x,y)\| \le T$: Not an edge
- $\|\nabla I(x,y)\| \ge T$: Edge

##### Two Threshold

- $\|\nabla I(x,y)\| \le T_0$: Not an edge
- $\|\nabla I(x,y)\| \ge T_1$: Not an edge
- $T_0 \le \|\nabla I(x,y)\| \le T_1$: Depends on neighboring pixels

### Second-Order Methods

- For gradient
  - Local extrema indicate edges
- For second derivative
  - Zero-crossing indicate edges

#### Laplacian Operator

$$ \nabla^2 I  = \frac{\partial^2I}{\partial x^2} + \frac{\partial^2I}{\partial y^2} $$

$$ \nabla^2 I = (f \ast [-1, 1]) \ast ([-1,1]) = f \ast [1, -2, 1] $$

- No need for thresholding
- But no info for magnitude

### Comparision between Gradient and Laplacian

|            Gradient            |    Laplacian    |
| :----------------------------: | :-------------: |
| Location, Magnitude, Direction |    Location     |
|      Maxima thresholding       |  Zero crossing  |
|   Non-linear[^NonLinearity]    |     Linear      |
|        Two convolution         | One convolution |

[^NonLinearity]: Non-linearity is introduced when computing $G = \sqrt{G_x^2 + G_y^2}$

### Noise

- Edge detector may fail when rapid-varying noise exists
- Can be solved by first applying a Gaussian smoothing
- Since Gaussian smoothing is also implemented by convolution, it can be combined with the edge detector before applying to the image

### Canny Edge Detector

#### Procedure

- Smooth image with 2D Gaussian $n_\sigma$
- Compute gradient with sobel operator
- Find magnitude by Sobel operator
- Find orientation by $\hat{n} = \frac{\nabla n_{\sigma} \ast I}{|\nabla n_{\sigma} \ast I|}$
- Compute Laplacian along the gradient direction $\frac{\partial^2 \nabla n_{\sigma} \ast I}{\partial \hat{n}^2}$
- Find zero crossing

## The Hough Transform

### Line Detection

Given edge points $(x_i,y_i)$ detected by edge detection algorithms, we want to detect straight lines $l:y=mx+c$ in the given image

Consider point $(x_i, y_i)$, if it lies on the line $l$, it should satisfy

$$ y_i = mx_i + c $$

We can re-write this equation as

$$ c = -x_im + y_i $$

Points on the same line in the $xy$ plane will intersect at point $(m,c)$ in the $mc$ plane

#### Algorithm

- Quantize parameter space $(m,c)$
- Create accumulator array $A[m,c]$
- Set $A[m,c] = 0$
- For each edge point $(x_i,y_i)$
  - $A[m,c] = A[m,c] + 1$ if $(m,c)$ lies on line $c = -x_im+y_i$
- Find local maxima in $A[m,c]$

#### Parameterization

- Slope of the line $m \in (-\infty, \infty) $
  - Requires large accumulator array
  - More memory and computation
  - Cannot represent vertical lines
- Use $x\sin\theta - y\cos\theta + \rho = 0$
  - $\theta \in [0,2\pi]$
  - $\rho \in [p, \rho_{max}]$
    - $\rho_{max}$ is the length of the diagonal of the image

In this parameterization, for each point $(x,y)$

$$ x\sin\theta - y\cos\theta + \rho = 0 $$

- There can be more than one intersection point
  - Because this function is periodic
- For images, we can restrict $-\pi/2 \le \theta \le \pi/2$ and $\rho_{max} = ImageDiagonal$

### Circle Detection

> "Click the circles:musical_note:"

#### Known Radius

$$ (x-a)^2 + (y-b)^2 = r^2 \Longrightarrow (a-x)^2 + (b-y)^2 = r^2$$

- Accumulator array $A[a,b]$
- Points on the same circle intersects at the same point

#### Unknown Radius

- Accumulator array $A[a,b,r]$
- Transforms into a cone in the 3D $(a,b,r)$-space

### Concluding Remarks

- Works on disconnected edges
- Relatively insensitive to occlusion and noise
- Effective for simple shapes with parameterized equations

## Fitting Lines to Edges

### Problem setting

- We know that some points lies on a line
- Want to fit this line accurately to the edge

#### Least-Squares

Given edge points $(x_i,y_i)$, want to find the exact $(m,c)$. This can be done by performing a least-squares regression

$$ m = \frac{\sum_i(x_i-\bar{x})(y_i - \bar{y})}{\sum_i(x_i - \bar{x})^2} \quad c = \bar{y} - m\bar{x}$$

#### Parameterization

```c
//TODO: Complete this note
```
