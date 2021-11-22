# 近似逼近方法

## 参数化价值函数

之前所有模型都是创建一个查询表，在表中维护状态价值函数 $V[s]$ 或动作价值函数 $Q[s,a]$。

- 处理大规模强化学习问题时
  - 状态空间或状态-动作空间可能非常大
  - 状态空间可能连续
- 解决方法
  - 离散化或分桶
  - 构建参数化的函数估计

## 离散化状态动作

- 对状态空间离散化
- 优点
  - 简洁直观
  - 高效
  - 在一些问题上能达到较好的效果
- 缺点
  - 过于简单
  - 一个桶只用一个常数，难以精确拟合连续函数
  - 维度灾难

## 参数化价值函数

构建可学习的函数来近似价值函数

$$ V_\theta(s) \approx V^{\pi}(s) \quad Q_\theta(s,a) \approx Q^{\pi}(s,a) $$

- 如果只关注参数化函数，那么绝大部分机器学习模型都可以使用
  - 线性模型、决策树等（需要特征工程）
    - 但是模型需要适合在非稳态、非独立同分布的数据上训练
    - 因此参数化模型比树模型更合适
      - 学出树模型后很难更改树的结构
  - 神经网络

### 随机梯度下降

#### 目标

找到参数向量 $\theta$ 最小化值函数近似值与真实值之间的均方误差

$$ J(\theta) = \mathbb{E}_\pi[\frac{1}{2}(V^\pi(s)-V_\theta(s))^2] $$

#### 梯度下降参数更新

$$ \theta = \theta - \alpha \frac{\partial J}{\partial \theta} = \theta + \alpha (V^\pi(s)-V_\theta(s))\frac{\partial V_\theta}{\partial \theta} $$

### 特征化状态

用一个特征向量表示状态

$$ x(s) = \begin{bmatrix}
    x_1(s)\\
    x_2(s)\\
    \vdots\\
    x_k(s)
\end{bmatrix} $$

## 价值函数近似算法

### 状态值函数近似

用特征的线性组合表示价值函数（也可以不用线性模型而用其他函数）

$$ V_\theta(s) = \theta^Tx(s) $$

$$ \theta = \theta + \alpha (V^\pi(s)-V_\theta(s))x(s) $$

#### 蒙特卡洛状态值函数近似

- 使用训练数据对价值函数进行预测

$$ (s_1,G_1), (s_2,G_2),\dots,(s_T,G_T) $$

- 对每个数据样本，使用梯度下降进行参数更新

$$ \theta = \theta + \alpha(G_t - V_\theta(s_t))x(s_t) $$

- 蒙特卡洛预测至少能收敛到一个局部最优解
  - 在价值函数为线性的情况下可以收敛到全局最优

#### 时序差分状态值函数近似

$$ (s_1,r_2 + \gamma V_\theta(s_2)), (s_2, r_3+\gamma V_\theta(s_3)), \dots $$

$$ \theta = \theta + \alpha (r_{t+1} + \gamma V_\theta(s_{t+1}) - V_\theta(s_t))x(s_t) $$

- 注意不需要对 $V_\theta(s_{t+1})$ 求梯度，因为它只是作为已知值，用于近似 $V^\pi(s)$

### 状态-动作函数近似

和 $V(s)$ 的近似类似，使用一个特征向量 $x(s,a)$ 表示特征，并对特征建立线性模型

$$ Q_\theta(s,a) = \theta^Tx(s,a) $$

#### 蒙特卡洛方法

#### 时序差分方法

## 策略梯度

### 参数化策略

- 可以将策略参数化

策略可以是确定性的

$$ a = \pi_\theta(s) $$

也可以是随机的

$$ \pi_\theta(a|s) = \mathbb{P}[a|s;\theta] $$

- $\theta$ 是参数
- 将可见的已知状态泛化到未知上

### 基于策略的强化学习

- 优点
  - 具有良好的收敛性
  - 在高维度或连续动作空间中更有效
    - 基于值函数的方法通常需要取最大值
  - 能够学习出随机策略
- 缺点
  - 通常会收敛到局部最优，而非全局最优
  - 评估一个策略通常不够高效，且有较大方差

### 策略梯度

#### 随机策略更新方法

- 直觉上
  - 降低带来较低价值的动作出现的概率
  - 提升带来较高价值的动作出现的概率

#### 单步马尔可夫决策过程的策略梯度

- 起始状态 $s\sim d(s)$
- 决策过程在一步后结束，奖励为 $r_{sa}$
- 策略的价值期望为

$$ J(\theta) = \mathbb{E}_{\pi_\theta}[r] = \sum_{s\in S}d(s)\sum_{a\in A}\pi_\theta(a|s)r_{sa} $$

如果对 $\theta$ 求导数

$$ \frac{\partial J}{\partial \theta} = \sum_{s\in S}d(s)\sum_{a \in A}\frac{\partial \pi_\theta}{\partial \theta} r_{sa} $$

#### 似然比 Likelihood Ratio

注意到

$$ \frac{\partial\pi_\theta}{\partial\theta} = \pi_\theta \frac{1}{\pi_\theta}\frac{\partial\pi_\theta}{\partial_\theta} = \pi_\theta \frac{\partial\log\pi_\theta}{\partial\theta} $$

将其带入并一通操作后

$$ \frac{\partial J}{\partial\theta} = \mathbb{E}_{\pi_\theta}\left[ \frac{\partial \log\pi_\theta}{\partial\theta}r_{sa} \right] $$

#### 策略梯度定理

- 把似然比推导过程泛化到了多步马尔可夫决策过程
  - 用长期价值函数 $Q_{\pi_\theta}(s,a)$ 代替瞬时奖励 $r_{sa}$
- 涉及起始状态目标函数 $J_1$，平均奖励目标函数 $J_{avR}$ 和平均价值目标函数 $J_{avV}$

对于任何可微的策略 $\pi_\theta(a|s)$，对上述三个目标函数中的任意一个，其策略梯度是

$$ \nabla J(\theta) = \mathbb{E}_{\pi_\theta}\left[ \frac{\partial\log\pi_\theta(a|s)}{\partial\theta}Q_{\pi_\theta}(s,a) \right] $$

### 蒙特卡洛策略梯度 REINFORCE

- 随机梯度上升更新策略最大化目标函数
- 利用策略梯度定理
- 利用累计奖励值 $G_t$ 作为 $Q_{\pi_\theta}(s,a)$ 的无偏估计

$$ \Delta\theta_t = \alpha \frac{\partial\log\pi_\theta}{\partial\theta} G_t $$

$$ \theta = \theta + \Delta\theta $$

```python
theta = random_init()
for s, a, r in get_episode(pi):
    for t in range(T):
        theta = theta + delta_theta()
```

- 简单
- 但是每次采样方差可能较大
  - 可以通过多次roll-out的 $G_t$ 平均值 $\bar{G}_t = \frac{1}{N}\sum_{i=1}^N G_t^{(i)}$ 来减小误差
  - 但是通常可能需要很多sample

#### Softmax 随机策略

$$ \pi_\theta(a|s) = \frac{\exp(f_\theta(s,a))}{\sum_{a'}\exp(f_\theta(s,a'))} $$

- 其中 $f_\theta(s,a)$ 是预先定义的状态-动作得分函数

该函数的对数似然的梯度是

$$ \frac{\partial\log\pi_\theta}{\partial\theta} = \frac{\partial f_\theta(s,a)}{\partial\theta} - \mathbb{E}_{a'\sim\pi_\theta(a'|s)}\left[ \frac{\partial f_\theta(s,a')}{\partial\theta} \right] $$

- 一步的梯度减去期望的梯度

## Actor-Critic

### REINFORCE 的问题

- 基于片段式数据的任务
  - 通常情况下需要终止状态
- 低数据利用率
  - 需要大量的训练数据
- 高方差

### Actor-Critic 基本思想

- 不使用样本直接对值函数进行估计
- 而是使用可训练的值函数 $Q_{\Phi}$ 来完成估计过程
- Actor $\pi_\theta(a|s)$
- Critic $Q_\Phi(s,a)$

### 训练

#### Critic

- 学习准确估计当前 actor policy 的动作价值

$$ Q_\Phi(s,a) \simeq r(s,a) + \gamma\mathbb{E}_{s'\sim p(s'|s,a), a'\sim\pi_\theta(a'|s')}[Q_\Phi(s',a')]$$

#### Actor

- 学习采取让 Critic 满意的动作

$$ J(\theta) = \mathbb{E}_{s\sim p,\pi_\theta}[\pi_\theta(a|s)Q_\Phi(s,a)] $$

$$ \nabla J = \mathbb{E}_{\pi_\theta}\left[ \nabla_\theta\log\pi_\theta(a|s) Q_\Phi(s,a) \right] $$

### Advantageous Actor-Critic A2C

- 减去一个基线函数来标准化 Critic 的打分
  - 引入更多信息指导，降低较差动作的概率，提高较优动作的概率
  - 进一步降低方差

#### 优势函数

$$ A_\pi(s,a) = Q_\pi(s,a) - V_\pi(s) $$

- Baseline 函数可以有很多选择

由于

$$Q_\pi(s,a) = r(s,a) + \gamma\mathbb{E}_{s'\sim p,a\sim\pi_\theta}[Q_\Phi(s',a')] $$

上式中，期望里的 $Q_\Phi$ 可以用 $V_\pi$ 代替

$$ Q_\pi(s,a) = r(s,a) + \gamma\mathbb{E}_{s'\sim p(s'|s,a)}[V_\pi(s)] $$

因此只需要拟合状态值函数就可以拟合优势函数

$$ A(s,a) = r(s,a) +\gamma\mathbb{E}[V_\pi(s')-V_\pi(s)] \simeq r(s,a) + \gamma(V_\pi(s')-V_\pi(s)) $$

- 采样一步状态进行估计
