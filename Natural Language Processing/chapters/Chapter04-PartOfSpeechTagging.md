# 词性标注与隐马尔可夫模型

## 词性标注

### 方法

- 基于规则
- 基于统计模型
  - 隐马尔可夫模型 HMM 和条件随机场 CRF
- 统计方法与规则方法结合
  - 使用规则方法对可疑的标注结果进行歧义消解
- 深度学习
  - LSTM + CRF 或 BiLSTM + CRF

## 隐马尔可夫模型

### 任务

给定一段句子单词 $v_1,\dots,v_N$，预测每个单词最可能的词性 $h_1,\dots,h_N$

$$ \argmax_{h}\mathbb{P}[h_1,\dots,h_N|v_1,\dots,v_N] = \argmax\frac{\mathbb{P}[v|h]\mathbb{P}[h]}{\mathbb{P}[v]} $$

即

$$ \argmax_h\mathbb{P}[v|h]\mathbb{P}[h] $$

- $h_i$ 为隐状态（词性）
- $v_i$ 为观测（实际的词）

#### $\mathbb{P}[h]$

- 当前隐层状态只与上一时刻的隐层状态有关

$$\begin{aligned}
    \mathbb{P}[h] &= \mathbb{P}[h_1,\dots,h_N]\\
    &= \mathbb{P}[h_1|h_2,\dots,h_N]\cdot\mathbb{P}[h_2|h_3,\dots,h_N]\cdot\cdots\\
    &= \mathbb{P}[h_1]\prod_{i=2}^N\mathbb{P}[h_i|h_{i-1}]
\end{aligned}$$

#### $\mathbb{P}[v|h]$

- 当前观测值只依赖于当前的隐层状态

$$\mathbb{P}[v|h] = \prod_{j=1}^N\mathbb{P}[v_j|h_j] $$

> 但是在数据集较大的情况下，直接计算所有概率的时间复杂度过高 $O(ns^n)$

## Viterbi 算法

- 是用动态规划相对高效地计算 $\mathbb{P}[v,h]$
- $O(ns^2)$
- 详见 AI2651 智能语音技术

## 前向-后向算法 Forward-Backward Algorithm

- $\alpha_t(j)=\mathbb{P}[v_1,\dots,v_t,h_t=j] $
  - $\alpha_{t+1}(j) = \sum_{i=1}^S\alpha_t(i)\cdot\mathbb{P}[h_{t+1}=j|h_t=i]\cdot\mathbb{P}[v_{t+1}|h_{t+1}=j]$
- $\beta_t(j) = \mathbb{P}[v_{t+1},\dots,v_N|h_t=j]$
  - $\beta_{t-1}(j) = \sum_{i=1}^S\beta_t(i)\cdot\mathbb{P}[h_t=i|t_{t-1}=j]\cdot\mathbb{P}[v_t|h_t=i]$

## 有监督参数估计

### 初始分布

$$ \hat{pi}_i = \mathbb{P}[h_1=i] = \frac{\#h_1=i}{\#Sentences} $$

### 状态转移

$$ \hat{a}_{ij} = \mathbb{P}[h_{i+1}=j|h_i=i] = \frac{\#Tags=(i,j)}{\#Tags=i} $$

### 状态输出

$$ \hat{b}_{ij} = \mathbb{P}[v_t=j|h_t=i] = \frac{\#Tags(word=i,tag=j)}{\#Tags(word=i)} $$

## 无监督参数估计 Baum-Welch
