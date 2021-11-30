# Image Alignment, Transforms & Panoramas

## Image Warping Basics

### Image Filtering

- Change the range of an image

$$ g(x) = h(f(x)) $$

### Image Warping

- Change the domain of an image

$$ g(x) = f(h(x)) $$

#### Parametric (Global) Warping

- Warpings that can be represented by parameterized functions

$$ (x,y) \xRightarrow{T} (x',y') $$

Where $T$ is a coordinate changing function $p' = T(p)$

- The warping is the same for any point $p$
- Can be represented by just a few parameters

#### Linear Transforms

$$ \begin{bmatrix}
    x'\\y'
\end{bmatrix} = T\begin{bmatrix}
    x\\y
\end{bmatrix} $$

where $T \in \mathbb{R}^{2\times 2}$

##### Uniform Scaling

$$ T = \begin{bmatrix}
    s & 0\\
    0 & s
\end{bmatrix} \quad T^{-1} = \begin{bmatrix}
    1/s & 0 \\
    0 & 1/s
\end{bmatrix} $$

##### Rotation

Rotation clockwise by $\theta$

$$ R = \begin{bmatrix}
    \cos\theta & -\sin\theta\\
    \sin\theta & \cos\theta
\end{bmatrix} \quad R^{-1} = R^T$$

##### Shear

Shifts a rectangle into a parallel 平行四边形

$$ T = \begin{bmatrix}
    1 & s\\
    0 & 1
\end{bmatrix} $$

##### Flipping and Mirror

> However, linear transformation cannot represent translation. Translation is not a linear transformation on 2D coordinates

##### All Linear Transformations

- Scale
- Rotation
- Shear
- Mirror

###### Properties

- Origin maps to origin
- Lines map to lines
- Parallel lines are still parallel
- Closed under composition

#### Homogeneous Coordinates

Trick: Add one more dimension

$$ \begin{bmatrix}
    x\\y\\w
\end{bmatrix} \xRightarrow{To Euclidean} \begin{bmatrix}
    x/w\\y/w\\1
\end{bmatrix} \Longrightarrow \begin{bmatrix}
    x/w\\
    y/w
\end{bmatrix}$$

#### Affine Transformations

Any linear transformation in Euclidean **space** can be formulated as an affine transformation in the Homogeneous Coordinate, with the last row of $T$ fixed to $(0,0,1)$

$$ T = \begin{bmatrix}
    a & b & t_x\\
    c & d & t_y\\
    0 & 0 & 1
\end{bmatrix} $$

##### Translate

$$ \begin{bmatrix}
    1 & 0 & t_x\\
    0 & 1 & t_y\\
    0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
    x\\y\\1
\end{bmatrix} $$

##### Scale

$$ \begin{bmatrix}
    s_x & 0 & 0\\
    0 & s_y & 0\\
    0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
    x\\y\\1
\end{bmatrix}$$

##### Rotation

$$ \begin{bmatrix}
    \cos\theta & -\sin\theta & 0\\
    \sin\theta & \cos\theta & 0\\
    0 & 0 & 1
\end{bmatrix}\begin{bmatrix}
    x\\y\\1
\end{bmatrix}$$

##### Properties

- Affine transformations are combinations of
  - Linear transformation
  - Translation
- Origin does not necessarily map to origin
- Lines map to lines
- Parallel lines remain parallel
- Closed under composition

#### Projective Transformation

a.k.a. Homographies / Planar Perspective Maps

$$ H =\begin{bmatrix}
    a & b & c\\
    d & e & f\\
    g & h & 1
\end{bmatrix} $$

$$ \begin{bmatrix}
    x'\\y'\\w'
\end{bmatrix} = \begin{bmatrix}
    a & b & c\\
    d & e & f\\
    g & h & i
\end{bmatrix} \begin{bmatrix}
    x\\y\\w
\end{bmatrix} $$

- Projective transformations are
  - Affine transformations
  - Projective warping
- Origin does not necessarily map to origin
- Lines map to lines
- Parallel lines do not necessarily remain parallel
- Closed under combination

##### Converting Homographes to Euclidean Coordinates

$$ \begin{bmatrix}
    x'\\y'\\w'
\end{bmatrix} = \begin{bmatrix}
    ax + by + c\\
    dx + ey + f\\
    gx + hy + 1
\end{bmatrix} \sim \begin{bmatrix}
    \frac{ax + by + c}{gx + hy + 1}\\
    \frac{dx + ey + f}{gx + hy + 1}\\
    1
\end{bmatrix} $$

- If Denominator is zero, then the point is mapped to infinity (vanishing point)

### Implementing Image Warping

Given a coordinate transform $(x',y') = T(x,y)$, and a source image $f(x,y)$, how do we compute an transformed image $g(x',y') = f(T(x,y))$?

#### Forward Warping

- Send each pixel $f(x,y)$ to its corresponding location $(x',y') = T(x,y)$
- If a pixel lands 'between' two pixels (warped pixel is not an integer)
  - Add contribution of each pixel and normalized them later
- But can still result in 'holes' in warpped image
  - Cannot guarantee that each pixel in the warped image corresponds to some pixels in the original image

#### Inverse Warping

- Get each pixel $g(x',y')$ from its corresponding location $(x,y) = T^{-1}(x',y')$ in original image $f(x,y)$
- If a pixel lands between two original pixels, interpolate it.
  - Interpolation methods: Nearest Neighbour; Bilinear; Bicubic

## Estimating Transformations

Given a set of matches between images $A$ and $B$. We want to compute the transform $T$ from $A$ to $B$

Since there are noises and mismatches, we find the transform $T$ that 'best agrees' with the matches

### Starting from Estimating Translation

Suppose we have a set of SIFT matches $\langle (x_i',y_i'), (x_i,y_i) \rangle$

For each pair, we have

$$ x_i + x_t = x_i' \quad y_i + y_t = y_i' $$

Therefore it is a set of linear equations

- Overdetermined system
- We find the least-squares solution
  - Minimize the sum of squared residuals $r_x^{(i)} = (x_i' - x_i) - x_t$

If we formulate the problem in matrix form

$$ \mathbf{A}\mathbf{t} = \mathbf{r} $$

Where $\mathbf{A}\in\mathbb{R}^{2n\times 2}$, $\mathbf{t}\in\mathbb{R}^{2\times 1}$, $\mathbf{r}\in\mathbb{R}^{2n\times{}1}$

Then

$$ \mathbf{t} = (\mathbf{A}^T\mathbf{A})^{-1}\mathbf{A}^T\mathbf{r} $$

### Least-Squares Formulation for Affine Transformations

$$ \begin{bmatrix}
    x'\\y'\\1
\end{bmatrix} = \begin{bmatrix}
    a & b & c \\
    d & e & f\\
    0 & 0 & 1
\end{bmatrix} \begin{bmatrix}
    x\\y\\1
\end{bmatrix} $$

- Each match provides two equations (1 of the 3 equations is trivial)
- Has 6 unknown params
- Requires at least 3 matches

Define residuals by

$$ r_{x_i} = (ax_i + by_i + c) - x_i' \quad r_{y_i} = (dx_i+ey_i+f) - y_i' $$

In matrix form

$$ \begin{bmatrix}
    x_1 & y_1 & 1 & 0 & 0 & 0\\
    0 & 0 & 0 & x_1 & y_1 & 1\\
    x_2 & y_2 & 1 & 0 & 0 & 0\\
    0 & 0 & 0 & x_2 & y_2 & 1\\
    \vdots &\vdots &\vdots &\vdots &\vdots &\vdots\\
    x_n & y_n & 1 & 0 & 0 & 0\\
    0 & 0 & 0 & x_n & y_n & 1\\
\end{bmatrix} \begin{bmatrix}
    a\\b\\c\\d\\e\\f
\end{bmatrix} = \begin{bmatrix}
    r_{x_1}\\r_{y_1}\\r_{x_2}\\r_{y_2}\\\vdots\\r_{x_n}\\r_{y_n}
\end{bmatrix}$$

Then it can be solved with least squares

### Solving Homographies

$$ \mathbf{w}\mathbf{x}' = \mathbf{H}\mathbf{x} $$

- 8 parameters for homographies
- Requires at least 4 pairs of matches

$$ \begin{bmatrix}
    x'\\y'\\1
\end{bmatrix} \propto \begin{bmatrix}
    h_{00} & h_{01} & h_{02} \\
    h_{10} & h_{11} & h_{12}\\
    h_{20} & h_{21} & h_{22}
\end{bmatrix} \begin{bmatrix}
    x\\y\\1
\end{bmatrix} $$

$$ x_i' =  $$

## Image Alignment Algorithm

Given input image $A$ and $B$

1. Compute features
2. Match features
3. Compute homography using least squares

Problem: What about the mismatched outliers?

### Hypothesize-And-Test

- Try many candidate lines and keep the best one with the most inliers and least outliers
  - Which lines are candidates?

#### Random Sample Consensus RANSAC

- All the inliers will agree with each other on the translation vector
- The (hopufully small) number of outliers will (hopefully) disagree with each other
  - Does not work when bad matches are more than 50%
  - "All good matches are alike; every bad match is bad in its own way"

##### Threshold

- **Inlier threshold** related to the amount of noise we expect in inliers
  - The noise is usually modeled as a Gaussian with some standard deviation
- **Number of rounds** related to the percentage of outliers we expect, and the probability of success we'd like to guarantee

##### General Algorithm Framework

1. Randomly choose $s$ samples
   - Usually $s$ is the minimum sample size required to fit the model
   - e.g. for translation, $s=1$; for affine transformations, $s=3$
2. Fit a model (line) to the samples
3. Count the number of inliers
4. Repeat $N$ times
5. Choose the model that has the largest set of inliers

##### Pros and Cons

- Pros
  - Simple and general
  - Applicable to many different problems
  - Often works well
- Cons
  - Requires parameter tuning
  - Sometimes requires too many iterations
  - Can fail for low inlier ratios

## Panorama

Given two images, we

1. Detect features
2. Match features
3. Compute homography by RANSAC
4. Combine the images together (somehow)

But can a 360 panorama be created by estimating homographies?

- No. Because lines no longer maps to lines in a 360 panorama
- For non-360 panoramas, we can project images onto a **common plane**
- For 360 panoramas, we need to project images onto a sphere

### Spherical Projection

> Welcome to 3D coordinates

Consider mapping a point $(X,Y,Z)$ in the physical world onto a unit sphere

$$ (\hat{x}, \hat{y}, \hat{z}) = \frac{1}{\sqrt{X^2+Y^2+Z^2}}(X,Y,Z) $$

We can convert the point to spherical corrdinates

$$ (\hat{x},\hat{y},\hat{z}) = (\sin\theta\cos\phi, \sin\phi, \cos\theta\cos\phi) $$

Further convert to spherical image corrdinates

$$ (\tilde{x}, \tilde{y}) = (s\theta, s\phi) + (\tilde{x}_c, \tilde{y}_c) $$

- This is done by unwrapping the sphere into a plane and shift the origin from the center to the bottom-left corner
- $s$ is a scaling factor that defines the final size of the image
  - Often convenient to set $s$ to the focal length of the camera (in pixel)
- Therefore for spherical reprojection, we need the focal length of the camera

### Spherical Alignment

Suppose we rotate the camera by $\theta$

- In the spherical image, it corresponds to a translation by $\theta$
- Therefore we can align the spherical image by translation

#### Drifting

- During alignment, the alignment error may accumulate
- This causes the aligned image to drift

##### Solution

- Add another copy of the first image at the end
  - Gives a constraint $y_n = y_1$
    - Add displacement $(y_1-y_n)/(n-1)$ to each image after the first image
    - apply affine warp $y' = y + ax$
    - run a big optimazation problem with the constraint
      - works best, but more complicated
      - known as 'bundle adjustment'

## Blending

- Artifacts exist in the aligned image
- Want to seamlessly blend the images together

### Feathering

- Linearly decrease the intensity of images at borderline
- Window size matters
  - Smooth and without 'ghost'
