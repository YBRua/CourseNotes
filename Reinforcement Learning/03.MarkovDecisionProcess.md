# 马尔可夫决策过程

## 随机过程

> 随机过程是一个或多个事件、随即系统或者随机现象随时间发生演变的过程。

### 马尔可夫过程

> 当前状态是未来的充分统计量

$$ \mathbb{P}[S_{t+1}|S_1,\dots,S_t] = \mathbb{P}[S_{t+1}|S_t] $$

## 马尔可夫决策过程

提供了一套为在结果部分随机、部分在决策者控制下的决策过程建模的数学框架

$$\mathbb{P}[S_{t+1}|S_t,A_t]$$

### 五元组

马尔可夫决策过程可以由一个五元组表示

$$ (S,A,\{P_{sa}\},\gamma,R) $$

- $S$ 是状态的集合
- $A$ 是动作的集合
- $P_{sa}$ 是状态转移概率：对每个状态 $s$ 和动作 $a$，$P_{sa}$ 是下一个状态在 $S$ 中的概率分布
- $\gamma \in [0, 1]$ 是对未来奖励的折扣因子
- $R:S\times A\mapsto \mathbb{R}$ 是奖励函数
  - 有时只和状态有关

### MDP的动态

- 从状态 $s_0$ 开始
- 智能体选择某个动作 $a_0$
- 得到奖励 $R(s_0,a_0)$
- 随机转移到下个状态 $s_1 \sim P_{s_0a_0}$
- 不断执行上述过程，直到出现终止状态（也可以无限执行）
- 总回报为 $\sum_t \gamma^t R(s_t,a_t)$

## 占用度量 Occupancy Measure

$$ \rho^{\pi}(s,a) = \mathbb{E}_{a\sim\pi(s),s'\sim p(s,a)}\left[ \sum_{t=0}^T\gamma^tp(s_t=s,a_t=a) \right] $$

### 归一化的占用度量

$$ \rho^{\pi}(s,a)' = (1-r)\rho^{\pi}(s,a) $$

- 归一化后占用度量的和为1
- 表示（动作，状态）被访问到的概率

定理1
: 和同一个动态环境交互的两个策略 $\pi_1$ 和 $\pi_2$ 得到的占用度量 $\rho^{\pi_1}$ 和 $\rho^{\pi_2}$ 满足

$$ \rho^{\pi_1} = \rho^{\pi_2} \Leftrightarrow \pi_1 = \pi_2 $$

定理2
: 给定一个占用度量 $\rho$，可生成该占用度量的唯一策略是

$$ \pi_p = \frac{\rho(s,a)}{\sum_{a'}\rho(s,a')} $$

## 基于动态规划的强化学习

- 选择能够最大化累计奖励期望的动作
$$ \mathbb{E}[R(s_0) + \gamma R(s_1) + \gamma^2R(s_2）+ \cdots] $$
  - $\gamma\in[0,1]$ 是未来奖励的折扣因子，使智能体更重视即时奖励
- 给定一个特定策略 $\pi(s):S \mapsto A$
  - 在状态 $s$ 采取策略 $a=\pi(s)$
- 给策略 $\pi$ 定义价值函数
$$ V^{\pi}(s) = \mathbb{E}[R(s_0) + \gamma R(s_1) + \gamma^2R(s_2）+ \cdots \mid s_0=s, \pi] $$

### 贝尔曼等式 Bellman Equation

$$\begin{aligned}
    V^{\pi}(s) &= \mathbb{E}[R(s_0) + \gamma R(s_1) + \gamma^2R(s_2）+ \cdots \mid s_0=s, \pi]\\
    &= \mathbb{E}[R(s_0) \mid s_0=s, \pi] + \gamma\mathbb{E}[R(s_1)+\gamma R(s_2) + \cdots \mid s_0=s, \pi]\\
    &= R(s) + \gamma\sum_{s'\in S}P_{s\pi(s)}(s')V(s')
\end{aligned}$$

### 最优价值函数

对状态 $s$ 来说的最优价值函数是所有策略可获得的最大可能折扣奖励的和

$$ V^*(s) = \max_{\pi}V^{\pi}(s) $$

#### 最优价值函数的Bellman等式

$$ V^*(s) = R(s) + \max_{a\in A}\gamma\sum_{s' \in S}P_{sa}(s')V^*(s') $$

#### 最优策略

$$ \pi^*(s) = \argmax_{a \in A}\sum_{s' \in S}P_{sa}(s')V^*(s') $$

- $ V^*(s) = V^{\pi^*}(s) \ge V^{\pi}(s) $

### 价值迭代 Value Iteration

```python
V = [0 for s in S]
while not converged():
    for s in S:
        V[s] = R[s] + maximize(gamma * sum([P[s][a](s_) * V[s_] for s_ in S]))
```

- 在计算中没有明确的策略

#### 同步迭代

- 存储两份值函数的拷贝
$$ V_{new}(s) \leftarrow \max_{a\in A}\left( R(s) + \gamma\sum_{s'\in S}P_{sa}(s')V_{old}(s') \right) $$

$$ V_{old}(s) \leftarrow V_{new}(s) $$

#### 异步迭代

$$ V_(s) \leftarrow \max_{a\in A}\left( R(s) + \gamma\sum_{s'\in S}P_{sa}(s')V(s') \right) $$

### 策略迭代 Policy Iteration

- 对于有限动作空间和状态空间的MDP
- $|S|<\infty, |A|<\infty$

```python
pi = random_init()
while not converged():
    V = compute_v_pi()  # computationally expensive
    for s in S:
        pi[s] = argmax(sum([P[s][a][s_] * V[s_] for s_ in S]))
```

## 基于模型的强化学习

- 在实际问题中，状态转移和奖励函数一般不是明确给出的
- 但是我们可以观测到一些 episodes

### 学习MDP模型

- 学习状态转移概率
$$ P_{sa}(s') = \frac{\#在状态s下采取策略a转移到s'}{\#在状态s下采取策略a} $$
- 学习奖励函数
$$ R(s) = \textrm{mean}_i(R(s)^{(i)}) $$

```python
pi = random_init()
while not converged():
    data = execute_and_collect_data(pi)
    P_sa, R = update(data)
    V = value_iteration()
    pi = greedy_update(V)
```
