# 值函数估计

## 模型无关的强化学习 Model-Free RL

> 在没有明确给出状态转移和奖励函数的现实问题，模型无关的强化学习直接从经验中学习值和策略，而无需构建MDP

- 关键步骤
  1. 估计值函数
  2. 优化策略

## 值函数估计

### 蒙特卡洛方法 Monte-Carlo Method

- 无偏估计、高方差
- 总折扣奖励
$$ G_t =R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{T-1}R_T $$
- 值函数估计值
$$\begin{aligned}
    V^{\pi}(s) &= \mathbb{E}[R(s_0)+\gamma R(s_1) + \cdots\mid s_0=s, \pi]\\
    &= \mathbb{E}[G_t\mid s_t=s,\pi]\\
    &\approx \frac{1}{N}\sum_{i=1}^N G_t^{(i)}
\end{aligned}$$
  - 其中 $G_t^{(i)}$ 是一次观测到状态 $s_t=s$ 起始的总折扣奖励

#### 实现

- 给定一段 episode，其中的每个时刻 $t$ 的状态 $s$ 都被访问
  1. 计数器增量 $N(s) \leftarrow N(s)+1$
  2. 累计奖励增量 $S(s) \leftarrow S(s) + G_t$
  3. 估计价值函数 $V(s) \leftarrow S(s)/N(s)$
  4. 更新策略 $\pi$

### 重要性采样 Importance Sampling

- 估计一个不同分布的期望
$$\begin{aligned}
  \mathbb{E}_{x\sim p}[f(x)] &= \int_x p(x)f(x)\mathrm{d}x\\
  &= \int_x q(x)\frac{p(x)}{q(x)}f(x)\mathrm{d}x\\
  &= \mathbb{E}_{x\sim q}\left[ \frac{p(x)}{q(x)}f(x) \right]
\end{aligned}$$
- 使用从一个分布中采到的样本估计另一个分布上的期望
- 将每个实例的权重重新分配为 $\beta(x)=p(x)/q(x)$
- 但是 $p(x)$ 和 $q(x)$ 都是概率，因此 $\beta$ 有时候会很大，有时候会很小
  - 导致权重小的数据点被权重大的数据点支配

#### 重要性采样的值函数估计

- 从独立同分布的原则出发，在完成一次策略更新后，之前所有依据旧策略得到的数据都不再能运用到后续训练中
- 因此可以根据两个策略之间的重要性比率对累计奖励进行加权
- 使用策略 $\mu$ 产生的累计奖励评估策略 $\pi$

$$ G_t^{\pi/\mu} = \frac{\pi(a_t|s_t)}{\mu(a_t|s_t)}\frac{pi(a_{t+1}|s_{t+1})}{\mu(a_{t+1}|s_{t+1})}\cdot\cdots G_t $$

- 方差可能非常大

#### 时序差分

- 根据重要性采样对时序差分目标 $r + \gamma V(s')$ 加权

$$ V(s_t)\leftarrow V(s_t) + \alpha\left( \frac{\pi(a_t|s_t)}{\mu(a_t|s_t)}\left( r_{t+1} + \gamma V(s_{t+1}) - V(s_t) \right) \right) $$

- 相比蒙特卡洛方法，方差更小

### 时序差分学习

- 模型无关学习
- 低方差、有偏估计
- 能够通过 bootstrap 从不完整的片段中学习

$$ V(S_t) \leftarrow V(S_t) + \alpha(R_{t+1} + \gamma V(S_{t+1})- V(S_t)) $$

#### 多步时序差分学习

- $n$ 步累计奖励 $G_t^{(n)} = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{n-1}R_{t+n} + \gamma^n V(S_{t+n})$