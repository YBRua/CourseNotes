# 值函数估计

## 模型无关的强化学习 Model-Free RL

> 在没有明确给出状态转移和奖励函数的现实问题，模型无关的强化学习直接从经验中学习值和策略，而无需构建MDP

- 关键步骤
  1. 估计值函数
  2. 优化策略

## 值函数估计

### 蒙特卡洛方法 Monte-Carlo

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
