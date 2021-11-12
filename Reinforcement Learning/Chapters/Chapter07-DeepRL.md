# 深度强化学习

## 深度Q网络 DQN

- 直观想法
  - 使用神经网络拟合 $Q_\theta(s,a)$
  - 不work
    - 连续采样的 $s_t,a_t,s_{t+1},r_t$ 不满足独立同分布
    - $Q_\theta(s,a)$ 频繁更新
- 解决方法
  - 经验回放
  - 双网络结构
    - 评估网络 Evaluation Network
    - 目标网络 Target Network

### 经验回放

- 存储训练过程中的每一步 $e_t = (s_t,a_t,s_{t+1},r_t)$
  - 从训练数据中采样，采样时服从均匀分布

#### 优先经验回放

以 Q 函数的值与目标值的差异来衡量学习的价值

$$ p_t = |r_t + \gamma\max_{a'}Q_\theta(s_{t+1},a')-Q_\theta(s_t,a_t)| $$

- 为了保证每个样本都有机会被采样，存储时使用 $p_t + \varepsilon$

选择样本的概率

$$ P(t) = \frac{p_t^\alpha}{\sum_kp_k^\alpha} $$

- 重要性采样
  - $\omega_t = \frac{(N\times P(t))^{-\beta}}{\max_i \omega_i}$

#### 目标网络

- 使用较旧的参数 $\theta_-$，每隔 $C$ 步和训练网络的参数同步一次
- 让目标网络的更新慢一些，防止新数据的偏差导致训练不稳定

$$L_i(\theta_i) = \mathbb{E}[\frac{1}{2}\omega_t(r_t + \gamma\max_{a'}Q_{\theta_-}(s_{t+1}, a') - Q_{\theta_i}(s_t,a_t))^2]$$