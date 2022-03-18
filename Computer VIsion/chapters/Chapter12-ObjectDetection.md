# Object Detection

## Pedestrain Detection with HoG

HoG: Histogram of Gradient

- Local object appearance and shape can often be characterized rather well by the distribution of local intensity gradients or edge directions

### Acquiring HoGs

- Divide the image into small spatial regions (cells)
  - Cells can be either rectangle or radial
- Each cell accumulates a weighted local 1-D histogram of gradient directions over pixels of the cell

### Normalization

- Contrast-normalize the local responses for better invariance to illumination and shadowing

### Dalal & Triggs Detector

- Construct an image pyramid to get the whole image at multiple resolutions
- Score every window of the feature pyramid
- Apply non-maximal suppression

## Deformable Part Models DPM

- Use part-based models and pictorial structures
- DPM = Dalal Triggs Detector + Part-based modeling
  - Add parts at a relative location and scale

### Structure of DPM

- Root filter
  - The root part of an object is modeled with HoG template
- Part filters
  - Part filters operate on a picture with 2x resolution for more fine-grained gradient information
- Deformation costs
  - Parts are allowed to slightly move around the expected location
  - Cost for the deformation between parts
  - The cost is modeled by a quadratic function

The final score is given by filter scores and spring costs

$$ Score(I, p_0) = \max \sum_{i=0}^n m_i(I, p_i) - \sum_{i=1}^n d_i(p_0, p_i) $$

### Training

- Parameters to learn
  - Biases (per component)
  - Deformation cost (per part)
  - Filter weights

#### Latent SVM

- Cannot directly train the DPM on a SVM
  - Because the parts do NOT have annotations
  - They are latent
