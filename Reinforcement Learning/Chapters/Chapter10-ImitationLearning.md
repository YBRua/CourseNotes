# .模仿学习

## 绪论

- 通常，提供专家数据比定义合理的汇报函数更容易一些

### What is Imitation Learning

- Train models when the reward funtion is not defined
  - Learning from Demostration LfD
  - Try to imitate from the expert demonstrations

#### Problem Setting

- Can obtain pre-collected trajectories ($(s,a)$-pairs) from experts
- Can (or sometimes cannot) interact with the environment
- Cannot access direct reward signals

### Basics

#### Trajectory Distribution

$P(\tau|\pi)$: distribution of trajectories induced by a policy

1. Sample $s_0$ from initial distribution over states $\rho_0$
2. Sample action $a_t$ from $\pi$
3. Sample next state $s_{t+1}$ from environment

#### Occupancy Measure

Distribution of state-action paris induced by a policy

$$ \rho_\pi(s,a) = \rho_\pi(s)\pi(a|s) $$

where

$$ \rho_pi(s) = (1-\gamma)\sum_{t=0}^\infty \gamma^tP(s_t=s|\pi) $$

## Methods

### General Imitation Learning

#### Objective

$$ \pi^\ast = \arg\min_\pi \mathbb{E}_{s\sim \rho_\pi^s}[l(\pi(\cdot|s), \pi_E(\cdot|s))] $$

### Behaviour Cloning

$$ \pi^\ast = \arg\min_\pi \mathbb{E}_{s\sim \rho_{\pi_E}^s}[l(\pi_E(\cdot|s), \pi(\cdot|s))] $$

- Essentially an MLE on each single step

#### Limiatations

- Distributional Shift
  - When $\pi_\theta$ takes a wrong action and starts to diverge from the expert, the distribution will be different from that of the expert
  - The agent cannot recover from errors so the problem becomes worse
- No long term planning

#### Advantages

- Simple
- Efficient

##### Can be Used For

- When 1-step deviations are not very bad
- When learning reactive behaviours
- When expert trajectories covers the entire space

### Inverse Reinforcement Learning

### Generative Adversarial Imitation Learning
