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

Any linear transformation in Euclidean space can be formulated as an affine transformation in the Homogeneous Coordinate, with the last row of $T$ fixed to $(0,0,1)$

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
