# MultiView

Method to eliminate 3D structure from two arbitrary images of a scene captured with cameras whose intrinsic parameters are known.

## Binocular Field of View

The **Binocular Fied of View** is the overlapping (intersection) filed of view in a binocular system. The field of view of the system is the union of the field of view of two cameras.

We can only estimate depth within the binocular field of view because we need two cameras for estimation.

### Vergence

- If we verge the two cameras, the field of view of the system becomes smaller, but the binocular field of view becomes larger
  - FoV decreases
  - Accuracy of depth estimation increases

## Binocular Stereo

### Relative Position and Orientation

- $\mathbf{t}_{3\times 1}$: Position of Right Camera in Left Camera coordinate frame
- $\mathbf{R}_{3\times 3}$: Rotation from Right to Left camera coordinate frame

$$ \mathbf{x}_l = \mathbf{R}\mathbf{x}_r + \mathbf{t} $$

1. Assume intrinsic params are known
2. Find relative camera position $\mathbf{t}$ and orientation $\mathbf{R}$ from the two images
3. Find correspondence for each pixel in the two images
4. Compute depth for each pixel

Solving 2. is quite difficult, but we already know how to solve 3.

## Epipolar Geometry

### Epipole

The image point of the origin/pinhole of one camera as viewed by the other camera is called the **epipole**. i.e. The projection of the pinhole of one camera onto the image plane of the other camera.

Denote the epipole on the left/right image plane by $\mathbf{e}_l,\mathbf{e}_r$. For a given stereo system, $\mathbf{e}_l$ and $\mathbf{e}_r$ are unique.

Notice that $\mathbf{O}_l, \mathbf{O}_r, \mathbf{e}_l, \mathbf{e}_r$ lies on the same line. The line only depends on the stereo system.

### Epipolar Plane

The camera origins $O_l,O_r$, the epiholes $\mathbf{e}_l,\mathbf{e}_r$ and any given scene point $P$ all lie on a plane called the **Epipolar Plane**

### Epipolar Line

Intersection of the image and the epipolar plane is called the **epipolar line**

Each scene point corresponds to two epipolar lines. The epipolar lines are determined by two points: the epihole and the projected scene points.

All epipolar lines intersect at the epihole

### Epipolar Constraint

Given a point in one image, the corresponding point in the other image must lie on the epipolar line

- Given a point on the image, since the origin of the camera is known, we can reconstruct a ray. The ray and the epihole determines the epipolar plane, and therefore we know the epipolar line on the other image

Define

$$ \mathbf{n} = \mathbf{t}\times\mathbf{x}_l $$

$\mathbf{n}$ is perpendicular to $\mathbf{x}_l$

$$ \mathbf{x}_l\cdot\mathbf{t}\times\mathbf{x}_l = 0 $$

$$ \begin{bmatrix}
    x_l & y_l & z_l
\end{bmatrix} \begin{bmatrix}
    0 & -t_z & t_y\\
    t_z & 0 & -t_x\\
    -t_y & t_x & 0
\end{bmatrix}\begin{bmatrix}
    x_l\\y_l\\z_l
\end{bmatrix} = 0$$

We know that

$$ \begin{bmatrix}
    x_l\\y_l\\z_l
\end{bmatrix} = \begin{bmatrix}
    r_{11} & r_{12} & r_{13} \\
    r_{21} & r_{22} & r_{23} \\
    r_{31} & r_{32} & r_{33} \\
\end{bmatrix}\begin{bmatrix}
    x_r\\y_r\\z_r
\end{bmatrix} + \begin{bmatrix}
    t_x\\t_y\\t_z
\end{bmatrix} $$

Plug this into the epipolar constraint,

$$ \begin{bmatrix}
    x_l & y_l & z_l
\end{bmatrix} \begin{bmatrix}
    e_{11} & e_{12} & e_{13} \\
    e_{21} & e_{22} & e_{23} \\
    e_{31} & e_{32} & e_{33} \\
\end{bmatrix} \begin{bmatrix}
    x_r\\y_r\\z_r
\end{bmatrix} = 0 $$

Therefore we can define the **essential matrix**

$$ \mathbf{E} = \mathbf{T}_\times\mathbf{R} $$

## Essential Matrix

The essential matrix relates the position of scene point in left camera coordinate to position in the right camera coordinate

$$ \mathbf{x}_l\cdot\mathbf{E}\mathbf{x}_r = 0 $$

### Fundamental Matrix

The fundamental matrix $\mathbf{F}$ relates the position of a scene point in left image to the position of the same scene point in right image

$$ \tilde{\mathbf{u}}_l \cdot \mathbf{F}\tilde{\mathbf{u}}_r=0 $$

Notice that $\mathbf{F}$ is defined in the homogeneous coordinate. So it can be determined only up to a scale factor.

### Epipolar Line and Fundamental Matrix

If $\mathbf{F}$ is known, then given a point $(u_l, v_l)$ in the left image, we can find the line in the right image that the corresponding point must lie on; and vice versa

### Estimating Funamental Matrix

In an uncalibrated binocular stereo, $\mathbf{F}$ is unknown, but we can know the point correspondence by graph matching. So the goal is to estimate $\mathbf{F}$

### Extracting Essential Matrix

$$ \mathbf{E} = \mathbf{K}_l^T\mathbf{F}\mathbf{K}_r $$

Then $\mathbf{T}_\times$ and $\mathbf{R}$ can be decoupled by performing SVD on $\mathbf{E}$