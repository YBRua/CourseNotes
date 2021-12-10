# Model-Based Deep Reinforcement Learning

## Q-Planning and Dyna

### Q-Planning

1. 从经验数据学习一个（环境）模型 $p(s', r|s,a)$
2. 从模型中采样以训练模型

Q-Planning同样产生一个四元组 $(s,a,r,s')$，但是其中 $s,a$ 是和真实环境交互的真实（历史）数据、$r,s'$ 是学习到的模型生成的虚假数据

```js
s = sample_state()
a = sample_action(s)

r, s_ = model(s, a)

/* One-step Q-function update */
```

### Dyna-Q

## Shooting Methods

1. “凭空产生”一组长度为 $T$ 的行动 $[a_0,\dots,a_T]$ （$a_0$是初始状态）
2. 用该行动序列和环境交互，得到一组轨迹 $[s_0,a_0,\hat{r}_0,\hat{s}_1,a_1,\hat{r}_0,\dots,\hat{s}_T,a_T,\hat{r}_T]$
3. 选择预期价值最高的动作序列 $\pi(s) = \arg\max_a \hat{Q}(s,a)$

### Random Shooting

- 纯随机采样动作序列
- 优势
  - 实现简单
  - 计算开销小
- 问题
  - 高方差
  - 可能采不到高回报的动作序列

### Cross Entropy Method CEM

- 根据已知的会产生较高回报的动作序列
- 在新采样时使用接近该高回报序列的分布

### Probabilistic Ensembles with Trajectory Sampling PETS

$$ loss_P(\theta) = -\sum_{n=1}^N \log\tilde{f}_{\theta}(s_{n+1}|s_n,a_n) $$

$$ \tilde{f} = P(s_{t+1}|s_t,a_t) = \mathcal{N}(\mu_\theta(s_t,a_t), \Sigma_\theta(s_t,a_t)) $$

- 假设 $P(s'|s,a)$ 是一个高斯过程，且使用神经网络拟合该过程
- 集成多个拟合的模型

## Branched Rollout Method

### Branched Rollout

- 从历史数据中，根据状态的分布采样一个历史起点
- 从历史起点跑 $k$ 步模拟
  - Dyna算法可以看作 $k=1$ 的 Rollout

### Model-Based Policy Optimization MBPO

## BMPO and AMPO

### Bidirectional Model BMPO

- 除了向后推演外，双向模型同时向前推演（TENET.jpg）
- 在同样长度的情况下，Compouding Error更小
- 但是需要额外的后向模型
  - 后向模型 $q_\theta'(s|s',a)$
  - 后向策略 $\tilde{\pi}_\phi(a|s')$

### AMPO

#### Distribution Mismatch in MBRL

- 环境的真实数据和模型模拟的数据之间的分布存在误差
- 这是 Compounding Model Error 的来源

##### Alleviations

- 学习过程中
  - 设计不同的损失函数和模型架构
  - 让rollout更拟真
- 使用模型时
  - 设计比较合理的rollout情景
  - 在误差造成问题之前停止rollout
- 但是问题仍然存在
