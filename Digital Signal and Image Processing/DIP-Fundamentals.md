# Fundamentals of Digital Images

- Natural image: The intercept of a 3D object on a 2D image plane.

## Image Processing Pipeline

1. acquisition
2. enhancement (preprocessing)
3. restoration
4. morphological processing
5. other task-specific procedures

## Human Visual System

> Sensor — Network — Compute

- contrast
- exposure
- illusion

## Acquisition and Representation of Digital Images

### Acquisition: Sampling and Quantization

#### Sampling

- Sample a discrete sample $f[x,y]$ of a continuous image $f(x,y)$.
- Each element of the array is a **pixel**.
- loss of information when downsampling

#### Quantization

- use a finite number of bits to represent real values.
- loss of information when rounding.

#### Aliasing

Not to confuse with the aliasing in signal processing.

- Aliasing occurs at edges of graphics
- Anti-Aliasing: bi-linear interpolation or bi-cubic interpolation.

#### Color Components

A colored image consists of 3 channels

- Red $R[x,y]$
- Green $G[x,y]$
- Blue $B[x,y]$

Cannot process each channel separately and combine the results. The distributions of the channels are different and therefore will cause undesired results.

For monochromatic images, the 3 channels can be considered to have the same distribution and therefore can be processed together.
