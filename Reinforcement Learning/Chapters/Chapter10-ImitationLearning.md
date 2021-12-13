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

#### Limitations

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

#### Dataset Aggregation DAgger

- Agent can interact with the environment using its learned policy
- Experts then label the generated trajectory to provide partial dataset
  - 'Partial' means that if the agent deviates from the trajectory, the data cannot be used since the agent is in a different state

### Inverse Reinforcement Learning

Learn a reward function $r^\ast$ from expert datasets.

Once $r^\ast$ is learned, a model can be trained with the reward function

$$ \pi^\ast = \arg\max_\pi \mathbb{E}){(s,a)\sim\rho_pi}[r^\ast(s,a)] $$

#### Learning Reward Function

The pricinple is that the expert should be optimal. i.e. the expert trajectory should achieve the highest value in the leared reward function

$$ r^\ast = \arg\max_r \mathbb{E}\left[ \sum_{t=0}^\infty \gamma^tr(s,a)|\pi^\ast \right] - \mathbb{E}\left[ \sum_{t=0}^\infty \gamma^tr(s,a)|\pi \right] $$

- Want the reward of the expert to be high, and the reward of others to be low

The training process is usually implemented in a nested loop

- Outer loop: find $r$
  - Inner loop: train policy $\pi$ with $r$
  - Check if $V(\pi^\ast) - V(\pi)$ is minimized

However, this formulation is ambiguous. The solution $r$ may not be unique.

#### Max-Entropy RL Formulation

- Learns a more diversed strategy
  - More chances to explore the environment
  - More robust
- Resolves ambiguity in IRL

### Generative Adversarial Imitation Learning

> Idea: Expert and policy occupancy measure can be formulated as the discriminator and generator in GAN
> Also proved that the duality of IRL with MaxEnt setting is equivalent to GAIL

$$ \min_\pi\max_D \mathbb{E}_{\pi_E}[\log D(s,a)] + \mathbb{E}_\pi[\log(1-D(s,a))] - \lambda H(\pi) $$

- Uses a discriminator $D$ to determine whether the current policy is from the expert or from the agent
