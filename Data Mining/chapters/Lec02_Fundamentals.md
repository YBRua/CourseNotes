# Data Mining Fundamentals

## Concepts

### Data Objects

- AKA. samples, instances, data points
- Data sets are made up of data objects

### Attributes

- AKA. dimensions, features, variables
- A data field, representing a characteristic or feature of a data object
- Values for a given attribute is called an **observation**

#### Types of Attributes

##### Nominal

- Categorical
- No meaningful order

##### Binary

- A special nominal attribute with only two categories or states: 0 and 1 (`False` and `True`)
  - **Symmetric binary**: Both states are equally important
  - **Asymmetric binary**: States are not equally important

##### Ordinal

- An attribute with values that have a meaningful order
- But the magnitude between successive values are unknown

##### Numeric

- Quantitative
- Integers or real values
- **Interval-scaled**: Measured on a scale of equal-size units. Can be compared. Can quantify the difference between values.
  - e.g. Temperature (No ratios)
- **Ratio-scaled**: A numeric attribute with an inherent zero-point.

#### Discrete and Continuous Attributes

##### Discrete

- Has a finite or countably infinite set of values

##### Continuous

### Handling Missing Values

- Ignore the tuple
- Manually filling in the values
- Using global constants (`unk`)
- Using global attribute mean
- Using class-wise attribute mean
- Using the most probable value

## Statistical Descriptions

### Central Tendency

Measuring the location of the middle or center of a data distribution.

#### Mean

$$ \bar{x} = \frac{\sum_N x_i}{N} $$

- Weighted mean
- Trimmed mean: The mean value obtained after chopping off values at high and low extremes

#### Median

The middle value in a set of ordered data values.

- A better measurement of the center of skewed (asymmetric) data

##### Approximation

1. Assume the data are grouped in intervals and the number of values in each interval (frequency) is known.
2. Compute median of all frequencies.
3. Let the interval containing the median frequency be the median interval.

$$ \textrm{median} = L_1 + \frac{N/2 - \sum_{lower}\textrm{freq}}{\textrm{freq}_{median}} \cdot \textrm{width} $$

where $L_1$ is the lower bound of the median interval, $\sum_{lower}\textrm{freq}$ is the sum of frequencies of intervals lower than the median interval, and $\textrm{width}$ is the width of the median interval.

#### Midrange

- Average of the largest and smallest values

#### Mode

- Value that occurs most frequently in the set.
- Data sets with 1, 2 or 3 modes are respectively called **unimodal**, **bimodal** and **trimodal**.

##### Skewed Data

- Positively skewed: $mode < median$

### Dispersion

How the data spread out.

#### Range

The difference between the largest and smallest values

#### Quantile

Data points that split the data into equal-size consecutive sets. e.g. percentage.

#### Quartile

4-quantile

##### Interquartile Range (IQR)

$$IQR = 3rdQuartile - 1stQuartile \triangleq Q_3 - Q_1$$

##### Outliers

Values falling at least $1.5\times$ IQR above $Q_3$ or below $Q_1$

#### Five-Number Summary

- Minimum
- $Q_1$
- Median
- $Q_3$
- Maximum

#### Variance and Standard Deviation

$$ \sigma^2 = \frac{1}{N}\sum_N (x_i - \bar{x}) = \left( \frac{1}{N}\sum_N x_i^2 \right) - \bar{x}^2 $$

- At least $(1 - 1/k^2) \times 100\%$ are no more than $k\sigma$ from mean. (By Chebyshev's Inequality)

#### Ohter

##### Mean Deviation

$$ \frac{\sum_n|x - \bar{x}|}{n} $$

##### Skewness

$$ \frac{\bar{x} - \textrm{mode}}{\sigma} $$

##### Coefficient of Variation

$$ \frac{\sigma}{\bar{x}} \times 100\% $$

## Graphic Displays

### Quantile Plot

1. Sort $x_i$ in increasing order
2. Compute $f_i = (i-0.5)/N$. $f_i$ indicates that approximately $f_i \times 100\%$ data are below $x_i$.
3. Plot $f_i$ against $x_i$.

### Quantile-Quantile Plot

- Plots the quantiles of one univariate distribution against the corresponding quantiles of another.
- Indicates if there is a shift from one distribution to another.

### Histogram

### Scatter plot

## Data Visualization Techniques

### Geometric Projection

> Visualizing high dimension data

- Direct visualization
- Scatter plot with various colors and markers
- Scatter plot matrices
  - Less effective when dimensions are high
- Parallel coordinates
  - $k$ equally spaced axes, one for each dimension
- Landscapes

### Pixel-Oriented Visualization

- For $m$ dimensions, create $m$ axes, one for each dimension
- $m$ values of one record are mapped to the corresponding pixels in the $m$ windows
- The values are organized in some global order, shared by all windows

### Hierarchical Visualization

- Dimensional stacking
- Worlds-within-worlds
- Tree-maps (e.g. Disk space usage)
- Tag cloud

## Measuring Similarity and Dissimilarity

- Data matrix $x_{ij}$
- Dissimilarity matrix $d_{ij} = d(i,j)$ where $d(i,j)$ is a measurement of distance between $x_i$ and $x_j$.

### Proximity Measures for Nominal Data

- $d(i,j) = (p-m) / p$ where $m$ is the number of matched values, and $p$ is the total number of attributes
