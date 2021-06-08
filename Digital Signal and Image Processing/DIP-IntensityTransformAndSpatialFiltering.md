# Intensity Transformation and Spatial Filtering

## Basics

What is the spacial domain?

- the plane containing the pixels of an image.
- neighborhood.

- Intensity Transformation
  - $g[x,y] = T(f[x,y])$
- Spatial Filtering
  - mask
  - kernel
  - template
  - window

## Intensity Transformation

### Thresholding

- Useful for segmentation, to isolate an object of interest from a background.

### Kinds of grey level transformation

- Linear
  - Negative
  - Identity
- Logarithmic
  - Log
  - Exponential
- Power (gamma)
  - $N$-th power
  - $N$-th root

### Logarithmic transformation

$$ s = c\log(1+r) $$

Maps a narrow range of low input grey level values into a wider range of output values.

### Gamma transformation

$$ s = cr^{\gamma} $$

Maps a narrow range of dark/bright input values into a wider range of output values.
