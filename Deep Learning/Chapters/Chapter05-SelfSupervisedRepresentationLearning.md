# Self-Supervised Representation Learning

## Self-Supervised Learning

> "Can we train networks without human-annotated labels?"

- Supervised learning
  - Learning with labeled data
- Semi-supervised learning
  - Learning with both labeled and unlabeled data
  - Generate pseudo-labels for unlabeled data
- Unsupervised learning
  - Learning with unlabeled data
- Self-supervised learning
  - Representation learning with unlabeled data
  - A category of unsupervised learning
  - Learn useful feature representations from unlabeled data through pretext tasks
  - Create labels based on inherent structures of images

### Example

- Pretext task
  - Train a model to predict the rotation degree of rotated images with cats and dogs
  - Labeling is not required
- Downstream task
  - Use transfer learning and fine-tuning for classification of cats and dogs with very few labeled examples

### Advantages

- Saves cost for labeling
- Make use of large amounts of unlabeled data
- Transfers better

### Challenges

- Select suitable pretext task
- Define loss functions

## Evaluation Protocol

### Baseline

- Supervised learning model

### Pre-Training

- Pre-train a self-supervised model

### Linear Classification

- Fix pre-trained model
- Append a linear layer after the pre-trained model
- Evaluate the appended model

### Efficient Classification

- Fix or tune pre-trained model
- Evaluate model with half-supervised learning

### Transfer Learning

- Fix or tune pre-trained model
- Evaluate by transfering the model to another downstream task

## Methods

### Overview of Pretext Tasks

#### Data Prediction

$$ x \xRightarrow{Network} x' $$

- Colorization
- Super-resolution
- Inpainting

#### Transformation Prediction

$$ T(x) \xRightarrow{Network} T(\cdot) $$

- Rotation
- Relative patch position
- Jigsaw puzzle

#### Contrastive Learning

$$ T(x), T'(x) \xRightarrow{Network} Sim/Disim $$

- Instance discrimination
  - MoCo
  - SimCLR
  - SWaV
  - BYOL

### Image Colorization

Predict the colors of the objects in grayscale images (which are originally colorful)

- Encoder-decoder CNN network
- $l_2$ loss

### Image Rotation

> “至于为什么Rotation比Colorization好，我也不知道。炼丹嘛。”
> “还没有形成化学。”

Predict the rotation of an image. The image is rotated by a multiple of $90\degree$ at random

- 4-class classification

### Relative Patch Position

Extract multiple patches from images. Train a model to predict the relationship between the patches.

- e.g. Predict the relative positions of a 3x3 patches.
  - For the center patch, there are 8 possible positions (8 classes)
- Input
  - Center patch and its random neighbour

#### Patch Selection

- Avoid the model catching only trivial information
- Add gaps between patches
- Add small jitters to positions of neighbouring patches
- Downsampling and Color-changing

### Jigsaw Puzzle

Predict the permutation of randomly permuted patches

### Deep Clustering

Given clusters of images (e.g. clusters of mountains, temples, etc.), predict the cluster to which an image belongs

### Instance Discrimination

Train a non-parametric classifier to do instance discrimination

- Want to discriminate each single input as an independent instance (a class)

#### InfoNCE Loss - Contrastive Loss

- NCE: Noise-Contrastive Estimation

$$ L_i = \log\frac{\exp(f_i\cdot v_i/\tau)}{\sum_j \exp(f_i \cdot v_j /\tau)} $$

#### Memory Bank

- For an end-to-end task, the training requires an extremely large batch size
  - `RuntimeError: CUDA out of memory`
- Can save negative samples in the memory (memory bank)
  - The encoder is updating during the training process
  - Features stored in the memory bank are inconsistent

#### MoCo

- Memory-bank-based method
- Uses a momentum encoder

```python
for x in loader:
    x_q = augment(x)
    x_k = another_augment(x)

    q = f_q.forward(x_q)
    k = f_k.forward(x_k)

    raise NotImplementedError('People are lazy')

    # compute gradient
    # compute loss
    # update params by momentum
```

$$ \theta_k = m\theta_k + (1-m)\theta_q $$

- The encoder updates at a relatively slow pace
- To maintain consistency in the memory bank

#### SimCLR

> “没关系，我们有TPU”

- Randomly sample a mini(actually quite large)-batch and apply two different data augmentation operations $t$, $t'$
- Yield $2n$ samples $x_i=t(x)$ and $x_j=t'(x)$
- Apply a base encoder $f$ to obtain $h_i = f(x_i)$ and $h_j = f(x_j)$
- Apply another prediction head encoder $g$ (a fully-connected layer) to obtain $z_i=g(h_i)$ and $z_j=g(h_j)$
- Compute similarity and loss
- When applying to downstream tasks, use $h$ instead of $z$
  - Experiment results show that $h$ performs better

> “遇事不决MLP”

##### Augmentation

SimCLR applies a wide range of data augmentation techniques

- Crop
- Resize
- Flip
- Color distortion
- Rotation
- Cutout
- Gaussian noise
- Gaussian blur
- Sobel filtering

#### MoCo V2

- Strong data augmentation
- MLP projection head
- Cosine learning rate decay (trick)

### Masked Image Pretraining

#### BERT Pretraining

##### Masked Language Model

- Given an input sentence, randomly mask 15\% of tokens
- Predict the masked word with a model

#### Masked Image Modeling

##### ViT

- Tokenize image into 16x16 patches by colors
  - Large search space

##### BEiT

- Tokenize image by VAE
- Encode image into indices
  - Requires a pre-trained tokenizer

##### DINO
