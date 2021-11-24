# Camera Calibration and Photogrammetry

- Camera Calibration is a method to find a camera's parameters
- Photogrammetry is a method to estimate 3D structure using two cameras

## Linear Camera Model

### Forward Imaging Model

Consider a pinhole camera, with camera coordinate $\mathcal{C}$. The parameter of $\mathcal{C}$ is unknown to us because it is sealed inside the camera. There is another known world coordinate $\mathcal{W}$.

- In Image Formation, we already know the mapping from camera coordinates $\mathbf{x}_c$ to the image plane $\mathbf{x}_i$

$$ x_i = f\frac{x_c}{z_c} \quad y_i = f\frac{y_c}{z_c}$$

- $x_i$ and $y_i$ have the same unit as $f$ (i.e. usually millimeters)
- But we are more familiar with digital images in pixels
- So we first construct a mapping from image plane to image sensors

#### Image Plane to Image Sensor

Let $m_x$ and $m_y$ be pixel density (pixels per millimeter) in $x$ and $y$ directions. Then pixel coordinates $u$ and $v$ are given by

$$ u = m_xx_i = m_xf\frac{x_c}{z_z} \quad v = m_yy_i = m_yf\frac{y_c}{z_c} $$

Further, since we are more familiar with the coordinate at the top-left of the image, we need to shift the origin from the center

$$ u = m_xf\frac{x_c}{z_z} + o_x \quad m_yf\frac{y_c}{z_c} + o_y $$

Note that the paramters $m_x,m_y,o_x,o_y$ are independent of the scenario and are only dependent on the camera

### Intrinsic Parameters

The intrinsic parameters of the camera are given by

$$ (f_x,f_y,o_x,o_y) $$

- $f_x = m_xf$, $f_y = m_yf$
- $o_x$, $o_y$ are the centriod of the lens, at the center of the optical axis

### Matrix Formulation of Perspective Projection

- Want to model the perspective projection in matrix form
- Again convert into homogeneous coordinate

$$ z_cu = f_xx_c + z_c o_x \quad z_cv = f_yy_c + z_co_y $$

$$ \begin{bmatrix}
    z_cu\\z_cv\\z_c
\end{bmatrix} = \begin{bmatrix}
    f_x & 0 & o_x & 0\\
    0 & f_y & o_y & 0\\
    0 & 0 & 1 & 0
\end{bmatrix} \begin{bmatrix}
    x_c\\y_c\\z_c\\1
\end{bmatrix}$$

#### Calibration Matrix and Intrinsic Matrix

The block

$$ K =\begin{bmatrix}
    f_x & 0 & o_x\\
    0 & f_y & o_y\\
    0 & 0 & 1
\end{bmatrix} $$

is called the **calibration matrix**, and the upper right triangle matrix $M_{int} = [K | 0]$ is called the **intrinsic matrix**

### World Coordinate to Camera Coordinate

- It's just a coordinate transformation involving rotation and translation
- The position $\mathbf{c}_w$ and orientation $R$ of the camera in the world coordinate are the **extrinsic parameters** of a camera

$$ \mathbf{x}_c = R(\mathbf{x}_w - \mathbf{c}_w) = R\mathbf{x}_w - R\mathbf{c}_w = R\mathbf{x}_w + \mathbf{t} $$

- where $\mathbf{t} = -R\mathbf{c}_w$ represents the translation

$$ \begin{bmatrix}
    x_c\\y_c\\z_c
\end{bmatrix} = \begin{bmatrix}
    r_{11} & r_{12} & r_{13}\\
    r_{21} & r_{22} & r_{23}\\
    r_{31} & r_{32} & r_{33}
\end{bmatrix} \begin{bmatrix}
    x_w\\y_w\\z_w
\end{bmatrix} + \begin{bmatrix}
    t_x\\t_y\\t_z
\end{bmatrix} $$

#### Homogeneous Formulation of World2Cam Transformation

Again the World-to-Camera transformation can be rewritten in homogeneous matrix product

$$ \begin{bmatrix}
    x_c\\y_c\\z_c\\1
\end{bmatrix} = \begin{bmatrix}
    \mathbf{R} & \mathbf{t}\\
    \mathbf{0} & 1
\end{bmatrix} \begin{bmatrix}
    x_w\\y_w\\z_w\\1
\end{bmatrix}$$

### Linear Camera Model

Combining the two models, we get the projection matrix $\mathbf{P}$

$$ \tilde{\mathbf{u}} = M_{int}M_{ext}\tilde{\mathbf{x}}_w = \mathbf{P}\tilde{\mathbf{x}}_w $$

## Camera Calibration

## Photogrammetry and Stereo
