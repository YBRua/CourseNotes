# Visual Recognition (Pre-DeepLearning)

> “哦你们都是00后？”
> “失敬失敬”

## Overview

### Image Representation

#### Descriptors

- SIFT
- HOG
- CodeWords

### Feature Learning

#### Discriminative and Generative Models

- Discriminative models model posterior ratio
  - Find a 'dicision boundary'
- Generative models model the likelihood ratio

## Apperance Recognition by PCA

### Offline Stage

Given $M$ learning images $\{I_1^{(q)},\dots,I_M^{(q)}\}$ for each of the $Q$ training objects. $q \in \{ 1,\dots,Q \}$

1. Normalized all images to remove brightness variations $I' = I / \|I\|$
2. Convert image $I'$ to feature vector $f'$
3. Compute mean feature vector $c$
4. Remove mean $f = f' - c$
5. Compute correlation matrix $R$
6. Compute PCA $E=[e_1,\dots,e_K]$ and project learning images to eigenspace $p = Ef$

### Online Stage

Given an input image $I$

1. Normalize image
2. Convert to feature vector
3. For each object $q$ in the database
   1. Remove mean $f^{(q)} = f' - c^{(q)} $
   2. Project into eigenspace
   3. Find object $q$ that minimizes the distance $d^{(q)}$

## Bag of 'Features'

### Bag of Features for Detection

1. Take a bunch of images
2. Extract features
3. Build up a dictionary of features
4. Given a new image, extract features and build a histogram for each feature
5. Find the closest visual 'word' in the dictionary

### Outline

1. Extract visual features
2. Learn 'visual vocabulary'
3. Quantize features using visual vocabulary
4. Represent images by frequencies of visual words

### Feature Detection and Representation

#### Detection

- Regular grids
- Interest point detector
- Other methods
  - Random sampling
  - Segmentation based patches

#### Representation

SIFT descriptors of patches can be a good choice

### Constructing Visual Dictionary

- Idea
  - Common categories should have clusters of similar features
- So we find the clusters and check which cluster tend to support which categories
- K-Means or EM can be applied to do this

The visual dictionary (codebook) is then used to quantize features

- A vector quantizer takes a feature vector as input and maps it to the index of the nearest codevector in a codebook

## TF-IDF Weighting

- Use **inverted files** to speed up computation of TF-IDF
  - Inverted file is a mapping from a feature to all documents that have the feature
