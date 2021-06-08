# Fundamentals of Spatial Filtering

## Neighborhood Operations

Neighborhood operations operate on a larger neighborhood of pixels, instead of operating on single points.

## Filtering vs Convolution

Filtering in MATLAB. Filtering is like correlation.
$$ g[m,n] = \sum*{k}\sum*{l}h[k,l]f[m+k,n+l] $$

Convolution in MATLAB
$$ g[m,n] = \sum*{k}\sum*{l}h[k,l]f[m-k,n-l] $$

## Image Smoothing

- Averaging all pixels in a neighborhood.
- Useful in removing noise
- Linear

### Simple Averaging Filter

### Weighted Averaging Filter

### Gaussian Filter

## Nonlinear Filtering

### Minimum Filtering

### Maximum Filtering

### Median Filtering

- Useful in cancelling pepper-salt noises.

## Edge Effect

How to pad.

### Zero Padding

May cause edge effects.

### Replicate

Pad with replicating edge pixels

### Wrap Around Edges

Assume the image is “periodic”, and pad with periodic extension.
