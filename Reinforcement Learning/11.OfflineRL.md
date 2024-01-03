# Offline Reinforcement Learning

## Overview

- Training an RL agent in real environment can sometimes be costly or risky
- **Offline RL** is a method of training the agent only from a pre-collected offline dataset
- The agent only have access to an offline dataset and cannot interact with the environment during training

### Extrapolation Error

$$ Q(s,a) \leftarrow (1-\alpha)Q(s,a) + \alpha(r + \gamma\max_{a'}Q(s',a')) $$

- Extrapolation error is introduced by the mismatch between the dataset and true state-action vistation of the current policy
- The Q-function may encounter an unforeseen $(s',a')$

## Methods

### Batch-Constrained Q-Learning BCQ

Although the agents use the same training data, their behavior may vary greatly. Whenever the offline model deviates from the online model, even the same input data may lead to different training results

#### Constraining Batches

$$ Q(s,a) = (1-\alpha)Q(s,a) + \alpha(r + \gamma\max_{a'\in\mathcal{B}}Q(s',a')) $$

- Constraint $a'$ to be some action in current batch of input data

#### VAE-Based Action Generation

- Use a VAE to give the action that may occur in real environment with high probability

$$ \pi(s) = \arg\max_{a_i+\xi_\phi(s, a_i, \Phi)} Q_\theta(s,a_i+\xi_\phi(s, a_i, \Phi)) $$

- $\xi_\phi(s, a_i, \Phi)$ is a variational auto-encoder

### Conservative Q-Learning

- Learn a conservative, lower-bound Q function to avoid over-estimation
- Add penalty terms on a standard Bellman error objective

### Advantage-Weighted Regression AWR

Policy optimization objective

$$ J(\pi) = \mathbb{E}_{r\sim p_\pi} \left[ \sum_{t=0}^\infty \gamma^tr_t \right] = \mathbb{E}_s\mathbb{E}_a[r(s,a)] $$

#### Reward-Weighted Regression

$$ \pi = \arg\max_\pi \mathbb{E}s\mathbb{E}_a \left[ \log\pi(a|s)\exp\left( \frac{1}{\beta}R(s,a) \right) \right] $$

- Regarded as solving a maximum likelihood estimation which fits a new policy to samples collected under the current policy, where the likelihood is weighted by the exponential return
- In some sense, a behaviour cloning that only clones 'good' data
