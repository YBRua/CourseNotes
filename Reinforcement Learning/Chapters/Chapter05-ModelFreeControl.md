# 无模型控制方法

> 估计 $Q(s,a)$

## 在线策略 On-Policy 与 离线策略 Off-Policy

- 在线策略
  - 得到策略后可以直接开始使用
  - 学习时使用当前策略采集到的数据
    - 不需要采样
    - 使用的数据也全是符合自己采用的策略的
  - 但是需要耗费大量资源
    - 因为数据全是自己采样的
  - 例如 $\epsilon$-Greedy
- 离线策略
  - 使用一个行为策略收集数据
  - 使用另一个目标策略估计动作价值函数
  - 例如 Q-Learning

### 为什么使用离线策略学习

- 平衡探索和利用
- 重用旧策略产生的经验
- 探索策略时学习最优策略

## SARSA

### 策略评估

- 对当前策略执行的每个 $(S,A,R,S',A')$ 五元组

$$ Q(s,a) \leftarrow Q(s,a) + \alpha (r + \gamma Q(s',a') - Q(s,a)) $$

### 策略改进

- $\epsilon$-Greedy 策略改进

## Q-Learning

- 根据行为策略选择动作 $a_t \sim \mu(a|s_t)$
- 根据目标策略选择后续动作 $a_{t+1}' \sim \pi(a|s_t)$

$$ Q(s,a) \leftarrow Q(s_t,a_t) + \alpha (r_t + \gamma Q(s_{t+1},a_{t+1}') - Q(s_t,a_t)) $$

- 允许行为策略和目标策略都进行改进
- 目标策略 $\pi$ 是关于 $Q(s,a)$ 的贪心策略
- 行为策略 $\mu$ 是关于 $Q(s,a)$ 的 $\epsilon$-贪心策略

Q-Learning 的目标函数可以简化为

$$ r_{t+1} + \gamma Q(s_{t+1},a_{t+1}') = r_{t+1} + \gamma\max_{a_{t+1}'}Q(s_{t+1},a_{t+1}') $$
