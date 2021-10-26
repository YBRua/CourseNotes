# Edge and Boundary Detection

> - What are edges?
> - Rapid changes in image intensity within small region

## Basics

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

## Gradient

- Represents the direction of most rapid change in intensity

$$ \nabla I = \left[ \frac{\partial I}{\partial x}, \frac{\partial I}{\partial y} \right] $$

### Magnitude

$$ S = \|\nabla I \| = \sqrt{\left( \frac{\partial I}{\partial x} \right)^2 + \left( \frac{\partial I}{\partial y} \right)^2 } $$

### Orientation

$$ \theta = \arctan\left( \frac{\partial I}{\partial y}/ \frac{\partial I}{\partial x} \right) $$

### Finite Difference Approximations

$$ \frac{\partial I}{\partial x} \approx \frac{1}{2\epsilon} ((I[i+1,j+1]-I[i,j+1]) + (I[i+1,j]-I[i,j])) $$

$$ \frac{\partial I}{\partial y} \approx \frac{1}{2\epsilon} ((I[i+1,j+1]-I[i+1,j]) + (I[i,j+1]-I[i,j])) $$

- $\epsilon$ is the distance between two pixels, usually $1$
- Can be implemented as convolution

$$ \frac{\partial}{\partial x} = \frac{1}{2\epsilon}\begin{bmatrix}
    -1 & 1\\
    -1 & 1
\end{bmatrix} $$

#### Common Operators

- Roberts
- Prewitt
- Sobel (3x3)
- Sobel (5x5)

#### Small and Large Operators

- Small
  - Better localization
- Large
  - Better approximation and robustness

## Non-Maximal Suppression

- Edges are thick after filtering
- Follow gradients and suppress pixels that are exceeded by a neighbor
- Can also use interpolation

## Thresholding

### Single Threshold

- $\|\nabla I(x,y)\| \le T$: Not an edge
- $\|\nabla I(x,y)\| \ge T$: Edge

### Two Threshold

- $\|\nabla I(x,y)\| \le T_0$: Not an edge
- $\|\nabla I(x,y)\| \ge T_1$: Not an edge
- $T_0 \le \|\nabla I(x,y)\| \le T_1$: Depends on neighboring pixels
