# Histogram Processing

## Image Histogram

Represents the relative frequency of occurrence of the various gray level of the image.

## Histogram Equalization

### Improving Contrast

Improving the contrast of an image is spreading its histogram into a wider range.

Spreading out the frequencies in an image (or equalizing the image) is a simple way to improve dark or washed out images.

In other words, we need to implement a mapping such that any arbitrary input pdf (histogram) can be converted to a uniform distribution.

### Continuous Case

Let $p_r(s)$ be the input histogram (pdf), let $p_s(s)$ be our desired equalized output.

Assume $s=T(r)$, the relationship between input and output pdf is
$$ p_s(s) \left| \frac{\mathrm{d}T(r)}{\mathrm{d}r} \right| = p_r(r) $$

We want $p_s(s)$ to be a constant (uniform distribution). Suppose the range of input is from $0$ to $L-1$, then we can set $p_s(s) = 1/(L-1)$ for all $s$ and integrate over $r$
$$ T(r) = (L-1)\int_{0}^{r}p_r(w)\mathrm{d}w $$

- Slope of $T(r)$ gives the amplification. The higher the value is in the original pdf, the larger the amplification.

### Discrete Case

The pixels of digital images are usually quantized.
$$ p_r(r_k) = \frac{n_k}{MN} $$

If we rewrite the integral to a summation
$$ s_k = T(r_k) = (L-1)\sum_{j=0}^kp_r(r_j) = \frac{L-1}{MN}\sum_{j=0}^kn_j $$

This can give a quite good result, but not optimal. Performing equalization is non-trivial in discrete case.

Instead of smoothing the original pdf into a uniform distribution, the summation only adjusts the distances between the bins.

- Bins with high frequencies are “separated”
- Bins with low frequencies are “compressed”

> “洗白了、washed out、over-exposure” —- Yuye Ling

## Histogram Specification

In addition to uniform distribution, we can also specify other distributions (e.g. Gaussian) and force the processed image to have a specified histogram distribution.

## CLAHE: Contrast-Limited Adaptive Histogram Equalization

> Cost-Limited Adaptive Healthy Eating

In discrete case, histogram equalization may fail to produce a desired output.

- Vanilla HE will assign the best contrast to the dominant gray levels regions.
- Because slope of $T(r)$ gives the scale of amplification.

### Contrast Limitation

- We want to limit the amplification given by $T(r)$: this is equivalent to clipping the height of the histogram.
  - But clipped histogram (pdf) does not sum up to 1.
  - So we compensate the clipped values by increasing all values in the pdf.
    - clipped parts now have smoother slopes.
    - originally low frequency parts now have sharper slopes.
- Contrast Limiting is simply histogram specification.

### Adaptive

- Perform histogram equalization in a small neighborhood.
- Use interpolation to stitch them up.
