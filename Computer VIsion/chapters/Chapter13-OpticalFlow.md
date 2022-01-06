# Optical Flow

## Motion Field and Parallax

Let $V$, $P$ be the position and velocity of an object in real world, and let $p$ and $v$ be the position and velocity on the image plane.

We have

$$ p = f\frac{P}{Z} $$

To find image velocity $v$, we differentiate $v$ with respective to $p$

$$ v = f\frac{ZV - V_ZP}{Z^2} \quad Z = f$$

We can write the velocity along each axis

$$ v_x = f\frac{V_X-V_ZX}{Z^2} = \frac{fV_X-V_Zx}{Z} $$

The second step uses $x = fP/X$

$$ v_x = f\frac{V_Y-V_ZY}{Z^2} = \frac{fV_Y-V_Zy}{Z} $$

### Pure Translation

Assume pure translation, so $V$ is a constant everywhere.

The displacement in real world is given by

$$ P_t = P + Vt $$

The displacement on image is given by

$$ p = f\frac{P+Vt}{Z+V_Zt} $$

If $t\to\infty$, we have

$$ p_\infty =  f\frac{V}{V_Z} $$

$ p_{x\infty} = f\frac{V_X}{V_Z} = x_0 $, which is the vanishing point along the $x$ axis.

Therefore we define

$$ p_0 = \begin{bmatrix}
    x_0\\y_0\\f
\end{bmatrix} $$

to be the **focus of expansion**.

Define $v_0 = (fV_X,fV_Y)$, then

$$ v = \frac{1}{Z}(v_0-V_Zp) $$

- If $V_Z < 0$, then the camera moves toward the object
- If $V_Z > 0$, then the camera moves away from the object
- If $V_Z$ is non-zero, then each vector points toward or away from $v_0$
- If $V_Z$ is zero, then each vector is parallel to the image plane
- The length of the motion vectors is inversely proportional to the depth $Z$

## General Visual Motion

Assume there is a rigid object, and the camera moves with translational velocity $T$ and rotational velocity $\omega$

For a given point $P = (X,Y,Z)$, we have

$$ v = f\frac{ZV-V_ZP}{Z^2} $$

where

$$ V = - T - \omega \times P $$

$$ V_Z = -T_Z - \omega_XY + \omega_YX $$

Again we take the derivative and the result would be

$$ \frac{du}{dt} = (T_Zu-fT_X)/Z + f\omega_y - \omega_zv - \omega_xuv/f + \omega_yu^2/f $$

$$ \frac{dv}{dt} = (T_Zv-fT_Y)/Z + f\omega_x - \omega_zu - \omega_yuv/f + \omega_xv^2/f $$

## Motion Estimation

- Feature-based Methods
  - Extract visual features and track them over multiple frames
  - Sparse motion field
  - Robust tracking
  - Suitable when image motion is large
- Direct Methods
  - Directly recover image motion at each pixel from image brightness variation
  - Dense motion field
  - Sensitive to appearance variations
  - Suitable when image motion is small, or in videos

## Optical Flow

A direct method for estimating motion

### Definition

The **optical flow** is the apparent motion of brightness patterns in the image

- Ideally, optical flow would be the same as the motion field
- However, apparent motion can be caused by lighting changes without any actual motion
  - A stationary screen displaying motion
  - Homogeneous objects (e.g. a pure-colored ball rotating along its axis)
  - Fixed sphere with a changing source of light
- Also does not work if the object is not rigid (e.g. a running dog)

### Estimating Optical Flow

#### Key Assumptions

- **Brightness Consistency.** Projection of the same point looks the same in every frame
- **Small Motion.** Points do not move too far.
- **Spatial Coherence.** Points move like their neighbours

#### Formulation of Constraints

##### Brightness Consistency

$$ I(x,y,t-1) = I(x+u(x,y), y+v(x,y), t) $$

where $(u,v)$ is the displacement vector. By Tayor Expansion

$$ I(x,y,t-1) = I(x,y,t) + I_xu(x,y) + I_yv(x,y) $$

where $I_x = \partial I/\partial x$

By brighness consistency, we require

$$ I_xu + I_yv + I_t \approx 0 \Rightarrow \nabla I \cdot [u,v] + I_t = 0$$

- one equation, two unknowns
- Intuitively, this indicates that the flow perpendicular to the gradient (or equivalently, parallel to the edge) is unknown

##### Spatial Coherence Lucas-Kanade Estimation

Pretent the pixel's neighbours have the same $(u,v)$

- If we use a $5\times 5$ window, then that gives us 25 equations per pixel

$$ Ad = b $$

where $A = [I_x(p_i), I_y(p_i)] \in \mathbb{R}^{25\times 2}$, $d = [u,v] \in \mathbb{R}^{2\times 1}$ and $b = -[I_t(p_i)] \in \mathbb{R}^{25 \times 1}$

Yet another least squares, and the result is given by

$$ d = (A^TA)^{-1}A^Tb $$

Notice that $A^TA$ is the Hessian used in corner detection. So for this problem to be *solvable*,

- $A^TA$ should be invertible
- Eigenvalues of $A^TA$ $\lambda_1$ and $\lambda_2$ should not be too small (small eigenvalues means flat regions)
- $A^TA$ should be well-conditioned
  - $\lambda_1 / \lambda_2$ should not be too large

###### Iterative Refinement

1. Estimate velocity at each pixel using one iteration of Lucas-Kanade Estimation
2. Warp one image toward the other using the estimated flow field
   - Easier said than done
3. Refine estimation by repeating the process

###### Implementation Issues

- Warping is not easy
- Warp one image, take the derivative of the other so do not need to re-compute gradient after each iteration
- Low-pass filtering before estimation is useful

###### Aliasing

- Temporal aliasing causes ambiguity in optical flow, because images can have many pixels of the same intensity

###### Restrictions

- Fails when intensity structure in window is poor
- Fails when displacement is large
- Fails when brightness changes too much

##### Coarse-to-Fine Estimation

- Construct pyramids of image using different windows
