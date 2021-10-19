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

- Let $H(x)$ denote the number of pixels with intensity $x$.
- Invariant to orientation transformation
