# Corner Detection and Matching

## Features

### What Makes a Good Feature

- Repeatability
  - The same feature can be found in several images despite geometric and photometric transformations
- Saliency
  - Each feature has a distinctive description
- Compactness and Efficiency
  - Many fewer features than image pixels
- Locality
  - A feature occupies a relatively small area of the image: robust to clutter and occlusion

### Application

- Motion tracking
- Image alignment
- 3D reconstruction
- Object recognition
- Indexing and database retrieval
- Robot navigation

## Corner Detection

### Corners

- In the region around a corner, image gradient (edge) has two or more dominant directions
- Repeatable and distinctive

### Basic Idea

- If a corner exists, shifting a window in any direction should give a large change in intensity
- $G_x$ and $G_y$ have different signs in the corner region

### Mathematic Model

Consider shifting a window $W$ slightly by $(u,v)$, then we compare each pixel before and after the shift by summing up the squared differences (SSD)

$$ E(u,v) = \sum_{(x,y)\in W}\left[ I(x+u, y+v) - I(x,y) \right]^2 $$

#### Small Motion Assumption

Consider the first-order Taylor expansion of $I$

$$ I(x+u,y+v) = I(x,y) + \frac{\partial I}{\partial x}u + \frac{\partial I}{\partial y}v + higher $$

We can use the first-order approximation if the motion $(u,v)$ is sufficiently small.

$$ I(x+u,y+v) \approx I(x,y) + \begin{bmatrix}
  I_x & I_y
\end{bmatrix} \begin{bmatrix}
  u\\ v
\end{bmatrix} $$

Therefore

$$ \begin{aligned}
  E(u,v) &= \sum_{(x,y)\in W} (I(x,y) + I_xu + I_yv - I(x,y))^2\\
  &=\sum_{(x,y)\in W} (\begin{bmatrix}
    I_x & I_y
  \end{bmatrix}\begin{bmatrix}
    u\\ v
  \end{bmatrix})^2\\
  &= \sum_{(x,y)\in W} \begin{bmatrix}
    u & v
  \end{bmatrix} \begin{bmatrix}
    I_x^2 & I_xI_y\\
    I_yI_x & I_y^2
  \end{bmatrix}\begin{bmatrix}
    u \\ v
  \end{bmatrix}\\
  &= \begin{bmatrix}
    u & v
  \end{bmatrix}\sum_{(x,y)\in W} \begin{bmatrix}
    I_x^2 & I_xI_y\\
    I_yI_x & I_y^2
  \end{bmatrix}\begin{bmatrix}
    u \\ v
  \end{bmatrix}
\end{aligned} $$

where

$$ H = \sum_{(x,y)\in W} \begin{bmatrix}
    I_x^2 & I_xI_y\\
    I_yI_x & I_y^2
  \end{bmatrix} $$

is the Hessian matrix

Therefore

$$ E = x^THx $$

Notice that $E \ge 0$, and therefore $H$ is positive-semidefinite

Therefore there exist 2 eigenvalues $\lambda_+ \ge \lambda_- \ge 0$ and corresponding eigenvectors $e_+,e_-$. So we can re-write $x$ into linear combinations of $e_+$ and $e_-$

$$ x = c_+e_+ + c_-e_- $$

where $c_+,c_-\in [0,1]$ and $c_+ + c_- = 1$

Plut $x$ back into $E$

$$ E = (c_+e_+ + c_-e_-)^T A (c_+e_+ + c_-e_-) = c_+^2\lambda_+ + c_-^2\lambda_-$$

Therefore $\max E = \lambda_+$ when $x=e_+$, and $\min E = \lambda_-$ when $x=e_-$

Intuitively

- $\lambda_+$ is the largest variation in $E$ caused by shifting $W$
  - For edges and corners, $\lambda_+$ can be large
- $\lambda_-$ is the smallest variation in $E$ caused by shifting $W$
  - When a corner exists, $\lambda_-$ can be large

##### Eigenvalues and Corners

- For flat regions, $\lambda_+\sim\lambda_-$ and both are small
- For edges, $\lambda_+ \gg \lambda_-$
- For corners, $\lambda_+ \sim \lambda_-$ and both are large

#### General Procedure for Corner Detection

- Compute the gradient
- Compute the Hessian
- Compute the eigenvalues
- Find points with large response where $\lambda_- > threshold$
- Choose points where $\lambda_-$ is a local maximum as features

#### Emprical Formular for Corner Detection

Define corner response function $R$

$$ R = \lambda_+\lambda_- - k(\lambda_+ + \lambda_-)^2 $$

- $k$ is usually in the range of $0.04\le k \le 0.06$
- Large $R$ may indicate a corner

### Harris Detector

#### Steps

1. Compute Gaussian derivatives (gradient)
2. Compute second moment matrix $H$ in a Gaussian window around each pixel
3. Compute corner response function $R$
4. Threshold $R$
5. Apply NMS

#### Invariance and Covariance

- Invariance
  - Features do not change even if image is transformed
- Covariance
  - Features should be detected in the same locations for two transformed version of an image

##### Analysis for Corner Detector

- Rotation
  - Eigenvectors rotate, but eigenvalues do not change
  - Invariant to rotation
- Scaling
  - Scaled corners will be detected as edges
  - Requires a larger window
  - Not invariant to scaling
- Affine intensity change
  - Invariant to constant addition
  - Not invariante to constant multiplication (intensity scaling)

## Feature Matching

### Feature Matching by XCorr

$$ XCorr(P_1,P_2) = \frac{1}{N}\sum_{i}^N P_1[i]P_2[i] $$

- Ordinary cross-correlation is not invariant to affine photometric transformation