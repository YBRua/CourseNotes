# 中文分词与条件随机场

## 概述

### 中文分词的规范

#### 合并原则

- 语义上无法由组合成分直接相加而得到的字串应该合并为一个分词单位
  - 不管三七二十一、十三点、超级加倍
- 语类无法由组合成分直接得到的字串应该合并为一个分词单位
  - 字串的语法功能不符合组合规律
    - 好吃、好喝
  - 字串的内部结构不符合语法规律
    - 端游、手游
- 附着性语素和前后词合并为一个单位
  - 邮递员、快递员
  - 现代化、合理化
- 使用频率高或共同出现频率高的字串尽量合并为一个分词单位
- 双音节加单音节的偏正式名词
  - 国际线、分数线、贫困线
- 双音节结构的偏正动词
  - 紧随其后

#### 切分原则

- 有明显分隔符标记的
- 内部结构复杂、合并起来过于冗长

### 切分歧义

- 交集型歧义
  - 为人民工作：为人、人民、民工
- 组合型歧义
  - 门把手弄坏了：门把手、门-把手、门-把-手

### 未登录词识别

> 即 `unk`，在训练集中没有出现过的词

- 人名、地名、组织机构名
- 新出现的词汇、术语、个别俗语

## 基本算法

### 最大匹配法

- 优点
  - 简单
  - 仅需要很少的语言资源（一个词表）
- 缺点
  - 歧义消解能力差
  - 没有优化机制

#### 正向最大匹配

- 假设词表中最长词长度为 $N$，最短词长度为 $1$
- 从 $N$ 到 $1$、从前往后在词典中进行匹配
  - 隐含假设是长的词比短的词优先级高

#### 逆向最大匹配

- 从 $N$ 到 $1$、从后往前在词典中进行匹配
- 实验结果通常是逆向匹配比正向匹配效果略好

### 最短路径法

- 输入一句句子，根据词典建立图
- 在图上用最短路径算法分词
- 假设一句话的分词结果应尽量少
- 优点
  - 切分原则明确、符合规律
  - 需要的语言资源也比较少
- 缺点
  - 歧义消解能力差
    - 在有多条最短路径时，难以划定区分标准
  - 字串长度增加时，等长的最短路径数量也会急剧增加

### 语言模型法

- 设句子 $S = \{s_1,\dots,s_N\}$ 可以切分为 $K$ 个词 $W= \{w_1,\dots,w_K\}$
- 找到最优的 $W^*$

$$ W^* = \argmax_W \mathbb{P}[W|S] = \argmax \mathbb{P}[W]\cdot\mathbb{P}[S|W] $$

其中 $\mathbb{P}[S|W]=1$ （因为词序列给定后拼成的句子一定是确定的），故

$$W^* = \argmax \mathbb{P}[W]$$

- 可以根据一个预先给定的语言模型计算
- 穷举所有的 $W$，找到最优的 $W^*$

#### 束搜索 Beam Search

- 从左到右计算，只保留可能性最大的前 $N$ 条路径
  - 不能保证结果是最优的
  - 但是这个近似结果不会太差

#### 优缺点

- 优点
  - 在语料充分的前提下，可以获得较好的切分准确率
- 缺点
  - 需要训练语料有较大规模、覆盖领域正确
  - 计算量较大

### 条件随机场

#### 问题设定

- 将分词看作序列标注问题，依次对序列中每个字赋予一个标签，再根据标签合并同一个单词的字符

#### 标签

- 四类标签
  - `B`：词首，一个词的开头
  - `M`：词中
  - `E`：词尾，一个词到此结束
  - `S`：单独成词
  - 要求配对使用；但是模型的输出不一定符合配对规范
- 两类标签
  - `I` 断字：词的最后一个字
  - `B` 非断字

> 可以用隐马尔可夫模型建模，但是也可以直接对条件概率 $\mathbb{P}[h|v]$ 进行拟合

#### CRF 概念

$$ \argmax_h \mathbb{P}[h|v] = \argmax_h \frac{score(h,v)}{\sum_h score(h,v)} $$

其中

$$ score(h,v) = \exp\left( \sum_{k=1}^K w_kF_k(h,v) \right) $$

$$ F_k(h,v) = \sum_{i=1}^N f_k(h_i, h_{i-1},v,i) $$

## 附录：概率图模型

### 概述

- 由图表示的联合概率分布 $\mathbb{P}[Y]$
- 节点 $v\in V$ 表示一个随机变量 $Y_v$
- 边表示随机变量之间的依赖关系

### 概率图模型的马尔可夫性

在建模概率图模型时，通常假设以下三种马尔可夫性质

#### 成对马尔可夫性

- 令 $v$, $u$ 是两个任意不直接相连的节点
- $O$ 是其他节点的集合

$$ \mathbb{P}[Y_v,Y_u|Y_O] = \mathbb{P}[Y_u|Y_O]\mathbb{P}[Y_v|Y_O] $$

#### 局部马尔可夫性

- 令 $v$ 是一个节点，$W$ 是与 $v$ 相邻的节点，$O$ 是其他节点

$$ \mathbb{P}[Y_v,Y_O|Y_W] = \mathbb{P}[Y_v|Y_W]\cdot\mathbb{P}[Y_O|Y_W] $$

#### 全局马尔可夫性

- 令 $A$、$B$ 是被节点集合 $C$ 隔开的两个节点集合

$$ \mathbb{P}[Y_A,Y_B|Y_C] = \mathbb{P}[Y_A|Y_C]\cdot\mathbb{P}[Y_B|Y_C] $$

### 定义

概率图模型
: 设有联合概率分布 $\mathbb{P}[Y]$，由无向图 $G=(V,E)$ 表示，节点表示随机变量，边表示变量的依赖关系。若 $\mathbb{P}[Y]$ 满足成对、局部或全局马尔可夫性，则称该联合分布为**概率（无向）图模型**，或**马尔可夫随机场**

最大团
: 无向图 $G=(V,E)$ 中任意两个节点间均有边连接的节点子集称为**团**。若 $C$ 是一个团，且不能再加入任何一个节点使 $C$ 成为一个更大的团，则 $C$ 称为 **最大团**

#### Hammersley-Clifford 定理

概率图模型的联合概率分布 $\mathbb{P}[Y]$ 可以表示成

$$ \mathbb{P}[Y] = \frac{1}{Z}\prod_C \Psi_C(Y_C) $$

其中

- $C$ 是图的最大团
- $\Psi_C(Y_C)$ 是 $C$ 上定义的严格正函数
  - 通常是指数函数

条件随机场
: 设 $X$、$Y$ 是随机变量。若 $\mathbb{P}[Y|X]$ 符合马尔可夫性，则称 $\mathbb{P}[Y|X]$ 是一个条件随机场。