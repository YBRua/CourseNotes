# 知识存储与检索

## 知识图谱的存储

- 按存储方式可以分为
  - 基于表结构的存储
  - 基于图结构的存储

### 基于表的存储

#### 三元组表

|   S   |   P   |   O   |
| :---: | :---: | :---: |
|  xxx  |  yyy  |  zzz  |

- 简单直接、易于理解
- 整个知识图谱存储在一张表中，规模太大，增删改查开销大
- 复杂查询需要拆分成若干简单查询的符合操作，开销大

#### 类型表

- 为每种类型构建一张表，同一类型的实例放在同一张表中
- 每一列表示该实体的一个属性，每一行存储该类型的一个实例

~~relational database~~ 但是它不是

- 数据字段的存储有冗余
  - 同属于两个类型的实例会被重复存储，且相同的字段会有两份

##### 考虑层级关系的类型表

~~类的继承~~

- 每个类型的表只记录属于该类型的特有属性
- 类型之间的共有属性保存在上一级类型中

#### 关系型数据库

- 二维表结构，每一行是一个 **元组**，每一列是一个 **属性**

### 基于图的存储

- 实体看作节点，关系看作带有标签的边
- 基于有向图
  - 节点用于表示实体、事件等对象。
  - 边用于表示对象之间的关系
  - 属性用于描述节点或边的特性

## 知识图谱的查询

### 关系型数据库-SQL

Structured Query Language SQL 介于关系代数和元组演算之间的语言。主要提供对数据的插入、删除、修改、查询四种操作。

#### 插入

```sql
insert
into TAB /* [(col1, col2, ...)] */
values tuple1 /* [, tuple2, ...] */
```

#### 更新

```sql
update TAB
set col1=val1, col2=val2
where condition
```

#### 删除

```sql
delete
from TAB
where condition
```

#### 查询

```sql
select
from TAB
where condition
```

### 图数据库-SPARQL

Simple Protocol And RDF Query Language

#### 插入

```sql
insert data { tuple }
```

- 可以是多条三元组，通过 `.` 分隔
- 如果待插入的三元组已经存在，则会被忽略

#### 删除

```sql
delete data { tuple }
```

#### 更新

- 通过 `delete` 后 `insert` 实现

#### 查询

##### select

```sql
select var1, var2, ...
where graph_pattern
/* [descriptors] */
```

##### ask

用于测试数据库中是否存在满足给定图模式 `graph_pattern` 的解，返回 `yes` 或 `no`

```sql
ask graph_pattern
```

##### describe

用于获取和给定资源相关的数据

```sql
describe var
where graph_pattern
```

##### construct

用于生成满足某种模式 `graph_pattern` 的 RDF 图

```sql
construct template
where graph_pattern
```
