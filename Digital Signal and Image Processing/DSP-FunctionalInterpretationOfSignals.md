# A Functional Interpretation of Signals

## Prerequisites

### Vector Spaces

A vector space $V$ is a set of functions equipped with

- Vector addition: $\forall u,v \in V \quad u + v \in V$
- Scalar multiplication: $\forall \alpha \in \mathbb{R}, \forall v \in V, \quad \alpha v \in V$

### Subspace

$S$ is a subspace of $V$ if

- $S$ is a subset of $V$
- $S$ is a vector space for the addition and scalar multiplication

### Spanned Subspace

Consider $v_1,\dots,v_N$ in a vector space $V$. Define
$$ S = \{ \alpha_1v_1 + \cdots + \alpha_Nv_N: \alpha_1,\dots,\alpha_N \in \mathbb{R} \} $$
$S$ is the subspace spanned by $v_1,\dots,v_N$, denoted by
$$ S = \mathrm{span}(v_1,\dots,v_N) $$

### Euclidean Space

A vector space $V$ is an Euclidean space if an **inner product** is defined on $V$.

- For example, the 2D Euclidean space $\mathbb{R}^2$ has inner product defined by $\langle x,y \rangle = x_1y_1 + x_2y_2$

The formal definition of an inner product is: A function $\langle \cdot, \cdot \rangle$ is called an inner product if

- $\forall u,v \in V, \langle u,v \rangle \in \mathbb{R} / \mathbb{C}$
- $\forall u,v,w\in V, \langle u+v,w \rangle = \langle u,w \rangle + \langle v,w \rangle$
- $\forall \alpha \in \mathbb{R}, \forall u,v \in V, \langle \alpha u, v \rangle = \alpha \langle u, v \rangle$
- $\forall u,v \in V, \langle u,v \rangle = \langle v,u \rangle$
- $\forall u \in V, \langle u,u \rangle \ge 0$
- $\langle u, u \rangle = 0 \Longrightarrow u = 0$

### Normed Space

Based on the inner product, we can define

- Norm: $\|x\| = \sqrt{\langle x,x \rangle}$
  - $\|x\| \ge 0$
- Distance: $d(x,y) = \|x-y\|$
- Orthogonality: $x \perp y \Leftrightarrow \langle x,y \rangle = 0$
- Orthonormal bases.
- Projection.

#### Projection

Projection of $x$ onto $y$

$$z = \frac{\langle x, y \rangle}{\|y\|^2}y$$

### Kindergarten Equation

Take $\mathbb{R}^2$ for example. Consider the orthonormal bases

$$
\begin{cases}
    e_1 &= (1,0)\\
    e_2 &= (0,1)
\end{cases}
$$

Then the projection of $x=(x_1,x_2)$ can be obtained by inner product
$$\langle x, e_1 \rangle = x_1 \quad \langle x, e_2 \rangle = x_2$$

We introduce the **Kindergarten Equation**
$$ x = x_1e_1 + x_2e_2 = \langle x,e_1 \rangle e_1 + \langle x,e_2 \rangle e_2 $$

### Hilbert Space

The previous discussions can be generalized to arbitrarily large finite and even some infinite dimensions.

The inner product of $\mathbb{R}^{\mathbb{R}}$ is defined by
$$ \langle x,y \rangle = \frac{1}{T}\int_0^T x(t)y^*(t)\mathrm{d}t $$

This form is very similar to the formalism of Fourier transform.

### Fourier Series: A Functional Perspective

Suppose a $T$-periodic signal $x(t)$, its Fourier series is given by
$$ x(t) = \sum_n X[k]\cdot\exp(j2\pi k\frac{t}{T}) $$

- We use a set of orthornormal bases $\exp(j2\pi kt /T)$ to approximate the original signal.

The coefficients $X[k]$
$$ X[k] = \frac{1}{T}\int_0^T x(t)\cdot\exp(-j2\pi k \frac{t}{T})\mathrm{d}t $$

are exactly the projections of $x(t)$ on orthonrmal bases $e_k = \exp(j2\pi kt/T)$

Therefore, Fourier series gives an approximation to the original periodic function in a subspace spanned by $e_k$ in mean square sense.
