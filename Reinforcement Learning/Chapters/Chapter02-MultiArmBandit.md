# 多 臂 老 虎 机

## 序列决策任务的基本问题

“基于目前策略获取已知最优收益，或者尝试不同的决策”

## 多臂老虎机

### 形式化表述

- 动作 $\mathcal{A} = \{ a_1, a_2, \dots, a_K \} $
- 收益分布 $\mathcal{R}(r_t|a_i) = \mathbb{P}(r_t|a_i)$
- 目标是最大化累计时间的收益 $\max\sum_{t=1}^T r_t$

### 算法框架

```python
# init
for i in range(K):
    Q[a[i]] = c[i]
    N[a[i]] = 0  # counter

# main loop
for t in range(T):
    action = select_action(pi)  # choose action by policy pi
    r[t] = bandit(action)       # get reward
    N[a[i]] = N[a[i]] + 1       # update counter
    update(Q[a[i]])             # update reward estimation
```

- $Q(a_i)$ 是执行动作 $a_i$ 能带来的收益的估计值
- $N_t(a_i) = \sum_{j=1}^t \mathbb{I}[A_j=a_i]$ 是 $t$ 时刻前选择动作 $a_i$ 的次数
- 要解决的问题
  - 估计期望收益
  - 选择策略 $\pi$

### 期望收益估计

- 动作的价值的真实值是选择这个动作的期望收益 $q_*(a)=\mathbb{E}[r|A_t=a]$
- 该期望可以使用均值估计
- 令 $Q_n(a_i)$ 表示动作$a_i$在被选择了 $n$ 次之后的估计收益，$R_j(a_i)$ 表示第 $j$ 次选择动作 $a_i$ 时获得的收益。

$$ Q_n(a_i) = \frac{\sum_{j=1}^{n-1}R_{j}(a_i)}{n-1} $$

### 贪心策略

#### 贪心法

在每一步估计收益，并选择当前最优（带来收益最大）的动作。

$$ Q_t(a) = \frac{\sum_{i=1}^{t-1}R_i \mathbb{I}[A_i=a]}{\sum_{i=1}^{t-1}\mathbb{I}[A_i=a]} $$

$$ a^* = \argmax_a Q_t(a) $$

#### $\epsilon$-贪心策略

#### 衰减贪心策略

### 乐观初始化
