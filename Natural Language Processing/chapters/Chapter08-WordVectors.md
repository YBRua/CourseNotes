# 词向量

## 词的表示

### 单热点词向量 One-hot

- 对 $N$ 个词的词库构建 $N$ 维的向量，其中第 $i$ 个词对应的向量第 $i$ 位为 $1$ 其余均为 $0$
- 简单直观
- 天然适合词袋模型

#### 词袋模型

- 对语句和短语的建模方式之一
- 只记录词的出现次数，忽略词的顺序
- 将语句中出现的每个词的词向量相加
  - 词袋模型中每一维度都是该词在该语句中出现的次数

#### 问题

- 维度爆炸
  - 有多少词就有多少维度
- 不能反应词与词之间的联系
  - 任意两个词的内积都是零，欧氏距离全部相等，不能反映词与词的语义关系

### 分布式词向量

- 具有聚类特性，能够根据距离反应词与词的关系
  - 可能是欧氏距离，也可能是余弦距离
- 每个维度代表了某种不同范畴的语义

## 词向量

### 基于共现频度的词向量