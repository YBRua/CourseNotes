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

### World Coordinate to Camera Coordinate, Extrinsic Parameters

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
    \mathbf{R}_{3\times 3} & \mathbf{t}_{3\times 1}\\
    \mathbf{0}_{1\times 3} & 1
\end{bmatrix} \begin{bmatrix}
    x_w\\y_w\\z_w\\1
\end{bmatrix}$$

### Linear Camera Model

Combining the two models, we get the projection matrix $\mathbf{P}$

$$ \tilde{\mathbf{u}} = M_{int}M_{ext}\tilde{\mathbf{x}}_w = \mathbf{P}\tilde{\mathbf{x}}_w $$

where $\mathbf{P} \in \mathbb{R}^{3\times 4}$ is a projetion matrix with 12 parameters

Note that proejction matrix acts on homogenous corrdinates. Therefore the scale of $\mathbf{P}$ does not matter.

## Camera Calibration

### Calibration with Known 3D Object

1. Capture the image of an object with known geometry
2. Identify correspondence between 3D scene points and captured image
3. For each correponding pair of points, we can construct an equation
4. Solve the equations by least squares

$$ \begin{bmatrix}
    u\\v\\1
\end{bmatrix} = \begin{bmatrix}
    p_{11} & p_{12} & p_{13} & p_{14}\\
    p_{21} & p_{22} & p_{23} & p_{24}\\
    p_{31} & p_{32} & p_{33} & p_{34}
\end{bmatrix} \begin{bmatrix}
    x_w\\y_w\\z_w\\1
\end{bmatrix} $$

Expand the matrix as linear equations and rewrite it into matrix form

$$ \mathbf{A}\mathbf{p} = \mathbf{0} $$

where $\mathbf{A}$ is known and $\mathbf{p} = \mathrm{vec}(\mathbf{P)}$ is to be determined

Since projection matrix can be determined up to a scale factor, any $k\mathbf{p}$ suffices as a solution. So we restrict $\|\mathbf{p}\|^2=1$

$$ \min \|\mathbf{A}\mathbf{p}\|^2 \quad \text{s.t.} \quad \|\mathbf{p}\|^2=1 $$

### Calibration with Known 2D Object

If we use a 2D checkboard (instead of a 3D object) to calibrate the camera, since all points lie in the same plane, we can assume that $z_w = 0$, and we can also remove the 3rd column of the extrinsic parameter matrix

### Distortion

#### Types of Distortions

Pinhole cameras do not exhibit distortions, but lenses do. The mathematical model for a model camera have to incorporate the distortion coefficients.

##### Radial Distortion

##### Tagential Distortion

## Photogrammetry and Stereo

### Backward Projection

Projection of an image point back into the scene results in an outgoing ray. We can know the direction of the ray, but we cannot know the exact position of the original point.

But what if we use **two** cameras?

### Simple Stereo

Consider two cameras placed together with horizontal baseline $b$ (i.e. the distance between the two cameras is $b$). Assume the pinhole of one camera $\mathfrak{C}_L$ is at origin $(0,0,0)$ and the pinhold of the other $\mathfrak{C}_R$ is at $(b,0,0)$

Consider a real-world position $(x,y,z)$, which is mapped to $(u_l,v_l)$ and $(u_r,v_r)$ respectively.

We know that

$$ u_l = f \cdot \frac{x}{z} \quad v_l = f\cdot \frac{y}{z}$$

$$ u_r = f \cdot \frac{x-b}{z} \quad v_r = f \cdot \frac{y}{z} $$

Therefore

$$ u_l-u_r = f\cdot\frac{b}{z} \Longrightarrow z = f\cdot\frac{b}{u_l-u_r} $$

Once we know $z$, we can efficiently solve for $x$ and $y$, thus reconstructing the scene

Define $(u_l-u_r)$ to be the **Disparity**. Given the baseline $b$ and focal length $f$, the scene depth can be determined by determining disparity.

Depth is inversely proportional to disparity

#### Finding Disparity

The two cameras depicts the same scenes, and therefore a template matching method can be used to determine disparity.

$v_l = v_r$, therefore corresponding scene points should lie on the same horizontal line. So the search only need to be performed along horizontal line.

##### Window-based Method

- Select a rectangular window in image $L$
- Move the window along the same horizontal line on image $R$ and do template matching

##### Size of Windows

- Small window
  - Noisy
- Large window
  - Too coarse

##### Adaptive Region-based Method

- Decide the range of disparsities to search
- Assume a non-verged system (horizontal offset between cameras only)
  - $d = fb/z$ where $d$ is the disparsity
  - Given a range of $z_{min}$ and $z_{max}$ we compute
    - $d_{min} = fb/z_{max} $
    - $d_{max} = fb/z_{min}$
- Thus for each point $u$, we search points $u + d_{min}$ to $u + d_{max}$
- Note that we can turn around and search for $u - d_{max}$ to $u - d_{min}$
