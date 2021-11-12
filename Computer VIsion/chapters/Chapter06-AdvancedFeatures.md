# 2D Recognition with SIFT

## From Blob Detection to SIFT

### Overview

- Use **blob-like** features for 2D recognition
- Need to
  - Locate blobs
  - Determine its size
  - Determine its orientation
  - Formulate a description or signature that is independent of its size and orientation

#### Observation

- If we compute the second-order derivative of an image with a Gaussian kernel of size $\sigma$ (i.e. a Laplacian kernel of size $\sigma$), and if the size of a blob is similar to the size of the kernel, there will be a local extremum in the result $\frac{\partial^2 n_\sigma}{\partial x^2} \ast f$

#### Characteristic Scale

- Define characteristic scale to be the $\sigma$ at which the second derivative of a blob attains its local extrema

##### Scale Normalization

- We want to find the characteristic scale of the blob by convolving it with Laplacian operators at several scales and looking for the maximum response
- However, Laplacian response **decays** as the scale increases
  - This is caused by the normalizing factor of Gaussian kernels $1/\sigma\sqrt{2\pi}$, which gets smaller as $\sigma$ increases.

Therefore we want to normalize the response.

- To do this, we **normalize the Laplacian response** by multiplying it with $\sigma^2$
  - Because the $1/\sigma$ in Gaussian becomes $1/\sigma^2$ in Laplacian

#### 1D Blob Detection

Given a 1D signal $f(x)$

1. Compute $\frac{\partial^2 n_\sigma}{\partial x^2} \ast f$ at different scales of $\sigma$
2. $(x^\ast,\sigma^\ast) = \arg\max$

### Scale Space

As we increase $\sigma$, the resolution becomes lower. Define scale space by the space created by filtering results of differernt $\sigma$

$$ S(x,y,\sigma) = \pi(x,y,\sigma) \ast f(x,y) $$

#### Creating Scale Space

- Ideally, the scale space is continuous
- But computers can only handle discrete spaces
- So we difine an initial $\sigma_0$ and multiply it by power of a constant multiplier $s$

$$ \sigma_k = \sigma_0s^k $$

- Given a blob area, there will be a $\sigma^\ast$ such that the response of this blob is maximized
  - Then we will be able to know the characteristic scale and the size of the blob
- For a large flat area, no extrema w.r.t. $\sigma$ can be found

#### 2D Blob Detection

Given an image $I(x,y)$

1. Convolve the image with many NLoG of different scales

## Scale Invariant Feature Transform SIFT

- An efficient implementation of blob detector
- Use Difference of Gaussian (DoG) as an approximation of NLoG