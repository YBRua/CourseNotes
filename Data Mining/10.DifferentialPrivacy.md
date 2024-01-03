# Privacy Preserving Data Mining

## Definition and Properties

> Participation of a person does not change the outcome too much

- Randomness
- Closeness

### Terminology

- Two parties are involved
  - A curator
  - A data analyst
    - Data analyst can be adversary

#### Curator

- A trustworthy **curator** holds data of individuals in database $D$
  - Each row corresponds to an individual
  - Each column corresponds to an attribute
- Goal is to protect ever individual row while permitting statistical analysis of $D$
- Can have two types depending on permission to interact
  - Non-interactive
    - Curator releases summary statistics, or "sanitized database", once and for all
  - Interactive
    - Permit queries adaptively to the database

#### Privacy

- Data analysis knows no more about an individual after analysis is completed than before the analysis had begun
- Adversary's **prior view** and **posterior views** about an individual should not be too different

##### Plausible Deniability

- Privacy comes from **plausible deniability**

### Randomized Algorithm

#### Probability Simplex

- Given a discrete set $B$, the **probability simplex** over $B$, denoted by $\Delta(B)$, is defined to be

$$ \Delta(B) = \left\{ x\in\mathbb{R}^{|B|}\mid \forall i x_i\ge 0, \sum_{i=1}^{|B|} x_i = 1 \right\} $$

A randomized algorithm $M$ with domain $A$ and discrete range $B$

#### Differentially Private Algorithms

##### $\epsilon$-Differential Privacy

An algorithm $A$ is called $\epsilon$-differentially private randomized algorithm if for all $D$, $D'$ that differ in one person's value

$$ \sup_t \left| \log\frac{p(A(D)=t)}{p(A(D')=t)} \right| \le \epsilon $$

i.e. The max-divergence of the two distributions is $\epsilon$

##### $(\epsilon,\delta)$-Differential Privacy

A randomized algorithm $M$ with domain $X$ is $(\epsilon,\delta)$-differentially private if for all $O\subseteq Range(M)$ and for all $x,y \in X$ s.t. $\|x - y\|_1 \le 1$

#### Properties

##### Post-Processing

Let $M$ be a $(\epsilon,\delta)$-differentially private algorithm
, and let $f$ be an arbitrary randomized mapping. Then $f\circ M$ is also $(\epsilon,\delta)$-differentially private

##### Composition

The composition of $k$ $(\epsilon_i,\delta_i)$-differentially private mechanizsms is $(\sum_i\epsilon_i,\sum_i\delta_i)$-differentially private

## Basic Mechanisms

### Randomized Response

> Flip a coin
