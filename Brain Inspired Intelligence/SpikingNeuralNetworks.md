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

$$ I_{in} = I_R + I_C = \frac{U_{mean}(t)}{R} + C \frac{\mathrm{d}U_{mean}(t)}{\mathrm{d}t} $$

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
