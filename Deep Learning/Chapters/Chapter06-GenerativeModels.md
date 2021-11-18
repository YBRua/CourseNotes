# Generative Models

## Model Structure

```text
                             ┌──────────────────┬──────────────┐
                             │                  │              │
┌───────────────┐       ┌────▼────┐             │              │
│random variable├──────►│generator├──┐          │              │
└───────────────┘       └─────────┘  │   ┌──────▼──────┐  ┌────┴────┐
                                     ├──►│discriminator├─►│real/fake│
                        ┌─────────┐  │   └─────────────┘  └─────────┘
                        │real data├──┘
                        └─────────┘
```

- Generator $G$
  - Generate fake data from random variable $z$
  - The generator maps a low-dimensional distribution $z$ (e.g. Multivariate Gaussian) to a high-dimensional distribution
- Discriminator $D$
  - Discriminate fake and real data
- Alternately train discriminator ($k$ steps) and generator (1 step)

### Goal

- Balance
  - Nash Equilibrium
- Optimality
  - $P_{gen} \approx P_{real}$

## Vanilla GAN

$$ \min_G\max_D V(D,G) = \mathbb{E}_{x\sim p_r(x)}[\log D(x)] + \mathbb{E}_{z\sim p_z(x)}[\log(1-D(G(z)))] $$

- $G$: Generator
- $D$: Discriminator
- $p_r$: Real distribution
- $p_z$: Noise distribution

### Optimizing Discriminator

$$ L_D = -V(D,G) = -\frac{1}{n}\sum_x\log D(x) - \frac{1}{n}\sum_z(1-D(G(z))) $$

### Optimizing Generator

$$ L_G = \mathbb{E}_{z\sim p_z(x)}[\log(1-D(G(z)))] = \frac{1}{n}\sum_z(1-D(G(z))) $$

### Network Architecture

- The vanilla GAN uses MLPs as the generator and discriminator

### Drawbacks

- Gradient vanishing
  - Hard to train
- Mode collapse
  - Ideal distribution has multiple modes
  - But the distribution learned by the model has fewer modes
    - Some modes 'vanished' (collapsed)
- Designed only for continuous data (like images)
  - Cannot handle discrete data (like texts)
- Evaluation is subjective

## Evaluation Metrics

### Inception Score IS

$$ IS(P_g) = \exp(\mathbb{E}_{x\sim P_g}KL(p_M(y|x)||p_M(y))) $$

- $p_M(y|x)$ should be peaked because given $x$, the model should know that the image is
- $p_M(y)$ should be close to uniform because we want image diversity
- Written together, we want the two distributions to be as far away as possible

### Frechet Inception Distance FID

Assumes the embedded data (feature space) follows a multivariate Gaussian distribution. We compute the Frechet distance between the Guassian distributions

$$ FID = \|\mu_x - \mu_y\|^2 + \mathrm{Tr}[\Sigma_x + \Sigma_y - 2(\Sigma_x\Sigma_y)^{1/2}] $$

## Conditional GAN

- Generate specific data
  - Have control on some specific attributes of the generated data (e.g. gender of faces)
- Conditioned on extra information $y$ (labels)
- Feed $y$ into $D$ and $G$
  - Concat the data with labels

$$ \min_G\max_D V(D,G) = \mathbb{E}_x[\log D(x|y)] + \mathbb{E}_z [\log(1-D(G(z|y)|y))] $$

or

$$ \min_G\max_D V(D,G) = \mathbb{E}_{x,y}[\log D(x,y)] + \mathbb{E}_{z,y}[\log(1-D(G(z,y),y))] $$

### Deep Convolutional Generative Adversarial Networks DCGAN

- Can be unstable
- Architecture guidelines
  - Replace pooling with strided convolution (for $D$) and fractional-strided convolutions (for $G$)
  - Use batchnorm
  - Remove FC hidden layers for deep architectures
  - Use ReLU in $G$, except for the last layer, which uses $\tanh$
  - Use LeakyReLU for $D$

## Info-GAN

- Goal
  - Unsupervised learning of disentangled representations
  - Want to decouple different dimensions of features
- Approach
  - GAN + Maximize mutual information

### Mutual Information

$$ I(X,Y) = \sum_i\sum_jp(x_i,y_j)\log\frac{p(x_i,y_j)}{p(x_i)p(y_j)} $$

- Difficult to compute
- Can be approximated with a lower bound (variational maximization)
  - Define an auxillary distribution $Q(c|x)$ to approximate $P(c|x)$

## Wasserstein Distance and JS Divergence

- Cross entropy for GAN is essentially JS Divergence
  - It cannot distinguish two distributions, if both do not intersect with the real distribution
  - which may cause gradient vanishing because no difference means zero gradient
- Can use Wasserstein Distance instead
  - Related with the optimal transport problem
  - Complicated

### Wasserstein Distance

$$ W_1(P_r,P_g) = \min_{\pi\in U(P_r,P_g)}\mathbb{E}_{(x,y)\sim\pi}\|x-y\| $$

Dual distance

$$ W_1(P_r,P_g) = \max_{\|f\|_L \le 1} \mathbb{E}_{x \sim P_r}[f(x)] - \mathbb{E}_{x \sim P_g}[f(x)] $$

- Requires $f$ to be smooth enough
  - $\|f\|_L = \frac{|f(x)-f(y)|}{|x-y|}$

### WGAN

$$ \min_{P_r}\max_{\|f\|_L \le 1}\mathbb{E}_x[f(x)] - \mathbb{E}_z[f(G(z))] $$

- But hard to describe Lipschiz restriction of $f$
  - Original work applies weight clipping to ensure the change is smooth enough

#### Gradient Penalty

- Alternative method for weight clipping
- For discriminator, add a term for restricting gradient
  - $\lambda(\|\nabla_{\hat{x}}D(\hat{x})\|_2 - 1)^2$
  - $\hat{x}$ is sampled between $x$ and $\tilde{x}$
