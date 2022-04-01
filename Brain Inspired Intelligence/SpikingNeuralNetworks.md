# Spiking Neural Networks

## Overview

### Encoding-Decoding

#### Input

- Rates: Output amplitude related to input rate
- Latency: Output latency related to input rate
- Delta Modulation

#### Output

- Rates
- Latency

### Architecture

#### Neuron Model

- Activation
- Topology

#### Loss

- Rate-based
- Latency-based

### Training

- Error Propagation
- ANN to SNN Conversion
- STDP for Online Learning

## Encoding in SNN

!!! question What is a 'good' spike?

    - Sparsity: Easy to compress and process; Prevents overheating
    - Static Suppression: Only reacts to changes (events)

### Input Encoding

#### Rate Encoding

- Converts input intensity to spike couts

Let input $X \in \mathbb{R}^{m \times n}$, we convert $X$ into encoding $R \in \mathbb{R}^{m\times n\times t}$

Let

$$ R_{ijk} \sim B(n, p) $$

Then

$$ P[R_{ijk} = 1] = X_{ij} = 1 - P[R_{ijk} = 0] $$

#### Latency Encoding

Simulates the process of a charging RC circuit

$$ U(t) = I_{in}R(1 - e^{-t/\tau}) $$

Time to charge until target value $\theta$

### Output Encoding

#### Rate Encoding

- Converts output intensity to prediction confidence level (argmax)
  - Can be done by a softmax layer $\mathrm{Softmax}(N_C)$ whose input is the number of spikes in a time interval for each output neuron
  - Can also be done by a MSE error function
    - Less robust to noise, but only requires one output neuron so the network can be smaller

## Training Algorithm for SNN

### Leaky Integrate and Fire (LIF) Neuron

- The buiding block for an SNN (just like the linear mapping and nonlinear activation in ANNs)
- A trade-off between biological realism and utility

1. 接受信息的膜结构可以建模为 RC 电路
   a. 膜的离子通道可以建模为电阻
   b. 膜的绝缘部分可以建模为电容（不导电，但是可以存储电荷）

#### Mathematic Formulation

$$ I_{in} = I_R + I_C = \frac{U_{mem}(t)}{R} + C \frac{\mathrm{d}U_{mem}(t)}{\mathrm{d}t} $$

##### Lapicque Model

We use $\Delta t$ to approximate $\mathrm{d}t$

$$ U(t + \Delta t) = U(t) + \frac{\Delta t}{\tau}(-U(t) + RI_{in}(t)) $$

#### Spike Generation

If $U_{mem} \ge \vartheta$, then $V_{out}$ generates a voltage spike and emits it to the output layer

#### Reset Mechanism

Whenever a spike is generated, $U_{mem}$ is reset to 0. Can be implemented by diodes, but has to be done manually in simulations

#### Simplified LIF Model

Assume no input current, $I_{in}(t) = 0$ =>

$$ U(t + \Delta t) = (1 - \frac{\Delta t}{\tau})U(t) $$

Denote $1 - \Delta t /\tau$ by $\beta$,

$$ U(t + \Delta t) = \beta U(t) $$

Further consider $I_{in}$

$$ U[t+1] = \beta U[t] + WX[t+1] $$

Further consider resetting

$$ U[t+1] = \beta U[t] + WX[t+1] - S[t]U_{threshold} $$

Parameters are $\beta, W, S$

## How to Train Your SNN

### Methods

#### White-box Optimization

##### Back-Propagation

- Classic gradient-based optimization methods

#### Black-box Optimization

##### Weight Perturbation

- Add random perturbation to weights
- If the performance is higher, then we accept the perturbation
- Otherwise discard the perturbation

However, as dimensions go up, sampling can be inefficient

##### Bayes Optimization

### Challenge

#### Dead Neuron Problem

- 模型的输入 $X[t+1]$ 是一串二进制序列
- 信号突变导致对输入的导数要么是 0，要么是无穷大

##### 导数替代 Surrogate Gradient

- 用平滑信号代替突变的脉冲
- 理论上需要证明替代梯度和理论梯度更新的权重之间的差距足够小

##### Spkie-time Gradient

- 对 Spike 产生的时间求导，而不是对 spike 本身求导 (SpikeProp)

Spike response model

$$ U_j(t) = \sum_{i,k} W_{i,j} I_i^{(k)} (t) $$

$$ I_i^{(k)}(t) = \varepsilon(t - f_i^{(k)}) = \frac{t}{\tau}e^{1-t/\tau} \Theta(t) $$

- $t$ is time step
- $W_{ij}$ is the weight from neuron $i$ to $j$, which is to be updated
- $f_i^{(k)}$ is the firing time of the $k$-th spike
- $I_i^{(k)}$ is the input sequence of spikes
- $\Theta(t)$ is the Heaviside step function

$$ L = MSE(y_j, f_j) $$

Gradient w.r.t. $W$ involves $I_i^{(k)}$. If there exists signal, then everything will be fine, but if there is no input signal, then the gradient will be $0$

Instead, we compute gradient by

$$ \frac{\partial L}{\partial W_{ij}} = \frac{\partial L}{\partial f_j} \frac{\partial f_j}{\partial U_j} \frac{\partial U_j}{\partial w_{ij}} $$

- 第一项和第三项可以直接求导得到
- 第二项在 $U(f_j)$ 满足反函数求导定理的前提下可以用 $\partial U / \partial t$ 的倒数求得

##### Spike Timing Dependent Plasticity STDP

从神经元接受和发射脉冲的时间差出发
