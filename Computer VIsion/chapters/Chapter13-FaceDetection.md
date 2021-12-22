# Face Detection (Pre-Deep-Learning)

## Face Detection in Computers

- Use a sliding window to search for face models
- For each window
  - Extract features
  - Match face model (Classifier)

## Haar Features

- A set of correlation responses to rectangular Haar filters
- A Haar filter is a filter consisting of regions of 1's and -1's (denote 1's by 'white' regions, and denote -1's by 'black' regions)

$$ V_A = I \otimes H_A = \sum I[\text{white regions}] - \sum I[\text{black regions}] $$

- Haar features capture the **directional pattern**

### Computational Cost

Assume the filter is $N\times M$, then it would be $(N\times M)$ additions per pixel per filter per scale.

- Expensive

### Integral Image

- Integral image helps compute Haar features effectively
- An integral image is a table that holds the sum of all pixel values to the left and top of a given pixel, inclusive
- The integral image enables fast summations of arbitrary rectangles
- Reduces summation of arbitrary rectangle regions to 3 additions
