# Binary Image Processing

## Binary Images

- Can only have two values (0 and 1)
- Simple to process and analyze

### Representation

- A grey image (after sampling and quantization) is represented as a matrix
- A binary image is a grey image whose grey level equals to $2$

### Converting Gray Image to Binary Image

- Usually by setting a threshold
- Choice of threshold
  - Using histograms

#### Histograms

- Let $H(x)$ denote the number of pixels with intensity $x$
- If there's a gap between white and dark pixels in the histogram, then set the threshold to be some value in the gap
- Invariant to orientation transformation

### Geometric Properties of Binary Images

> Assume for now that the image $h(x,y)$ is continuous

#### Area

a.k.a. Zeroth Moment

$$ A = \iint_I b(x,y)\mathrm{d}x\mathrm{d}y $$

- In discrete case, it is the sum over all $b_{ij}$

$$ A = \sum_i\sum_j b_{ij} $$

#### Position

Center of area. a.k.a. First Moment

$$ \bar{x} = \frac{1}{A}\iint_I xb(x,y)\mathrm{d}x\mathrm{d}y $$

$$ \bar{y} = \frac{1}{A}\iint_I yb(x,y)\mathrm{d}x\mathrm{d}y $$

$$ \bar{x} = \sum_i\sum_j\frac{1}{A} ib_{ij} $$

$$ \bar{y} = \sum_i\sum_j\frac{1}{A} jb_{ij} $$

#### Second Moments

$$ a' = \sum_i\sum_j i^2 b_{ij} $$

$$ b' = \sum_i\sum_j ij b_{ij} $$

$$ c' = \sum_i\sum_j j^2 b_{ij} $$

#### Orientation

- Axis of the least second moment

$$ \min E = \iint_I r^2 b(x,y) \mathrm{d}x\mathrm{d}y $$

where $r$ is the distance of a point on the image to the axis

- Use $x\sin\theta - y\cos\theta + \rho = 0$ as the equation for the axis
  - $\rho$ and $\theta$ are finite

For any point $(x,y)$, we can show that

$$ r = x\sin\theta + y\cos\theta + \rho $$

Therefore we minimize

$$ \iint_I (x\sin\theta + y\cos\theta + \rho)^2 b(x,y) \mathrm{d}x\mathrm{d}y $$

Let $\frac{\partial E}{\partial \rho} = 0$, we can get

$$ A(\bar{x}\sin\theta - \bar{y}\cos\theta + \rho) = 0 $$

- The axis passes through center $(\bar{x},\bar{y})$
- We can then shift the coordinate system and move the origin to the center

$$ x' = x - \bar{x} \quad y'=y-\bar{y} $$

We can then eliminate $\rho$

$$ x\sin\theta + y\cos\theta + \rho = x'\sin\theta - y'\cos\theta $$

Plug this back to $E$

$$ E = a\sin^2\theta - b\sin\theta\cos\theta + c\cos^2\theta $$

where $a,b,c$ are second moments

Take derivative w.r.t. $\theta$ and set it to zero, we get

$$\tan 2\theta = \frac{b}{a-c}$$

We know that $$\tan 2\theta = \tan(2\theta+\pi)$$

$\theta$ will have two solutions, one gives the minimum, the other gives the maximum

- $\theta = \theta_1$
- $\theta = \theta_2 = \theta_1 + \pi/2$

So we continue to compute the second-order derivative, and it can be verified that $\theta_1$ is the minimum, $\theta_2$ is the maximum

Therefore, the orientation is given by

$$ \theta=\theta_1=\frac{1}{2}\arctan\left( \frac{b}{a-c} \right) $$

#### Roundedness

Define roundedness by

$$ Roundedness = \frac{E_{min}}{E_{max}} = \frac{E(\theta_1)}{E(\theta_2)} $$

### Segmentation of Images

#### Region Growing Algorithm

1. Find unlabeled seed point with $b=1$
2. Assign new label to seed point
3. Assign same label to neighbours
4. Assign same label to neighbours of neighbours
5. Repeat until no unlabeld neighbours exist
6. Repeat from 1

#### Neighbours

> A closed curve should separate the image into 2 connected regions

- 4-Connectedness
- 8-Connectedness
- Neither is perfect

|   1   |   2   |   3   |
| :---: | :---: | :---: |
|   0   |   1   |   0   |
|   1   |   0   |   1   |
|   0   |   1   |   0   |

##### Solution

- Use 8-C for foreground
- Use 4-C for background

#### Sequential Labeling Algorithm

|   1   |   2   |   3   |
| :---: | :---: | :---: |
|   D   |   B   |   0   |
|   C   |   A   |   0   |
|   0   |   0   |   0   |

Suppose we are labeling A, and B, C, D are already labeled

- $A=0$: Background
- $A=1, Others=0$: New label
- $A=1,D=1$: Same label as $D$
- $A=1,B=1; Other=0$ or $A=1,C=1; Other=0$: Same label as $B$ or $C$
- $A=1, B=1, C=1, D=0$, but $B$ and $C$ have different labels
  - Use an equivalence table and note down $label(B) = label(C)$
  - Perform second pass to merge equivalent labels

## Morphological Operators

### Binary Dilation

Let $R$ be the original image, $S$ be a dilation template.

$$ D(R,S) = R \oplus S = \{u-v|u\in R,v \in S\} $$

- Intuitively, this is the set of all possbile positions of the center of $S$, such that the two patterns overlap by at least one element

### Binary Erosion

$$ E(R,S) = R\ominus S = \{u|\forall v \in S, u+v \in R\} $$

- Intuitively, this is the set of all positions of the center of $S$ such that the pattern $S$ is contained in $R$

### Binary Closing

$$ C(R,S) = E(D(R,S),S) $$

- Fill the holes that are smaller than the structiong elements
- Smooth the contours by filling the cavities

### Binary Opening

$$ O(R,S) = D(E(R,S),S) $$

- Suppress the structures smaller than the structuring elements
- Delete the link between weak connected components
- Smooth the contours by deleting the outgrowths

!!!note
    The close and open operations can also be nested to remove the noice perturbation
