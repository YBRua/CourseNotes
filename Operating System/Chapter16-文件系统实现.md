# 文件系统的实现与崩溃一致性

## 文件系统API

文件系统提供多个API，应用程序通过系统调用使用这些API

### `open`

> 打开一个文件

- 检查用户权限
- 更新访问时间
- 返回一个号码，表示该文件（文件描述符 FD）
  - 后续操作均使用FD

#### 文件描述符 File Descriptor

- 每个进程启动时，有三个文件默认被打开
  - 标准输入 `fd:0` 标准输出 `fd:1` 和标准错误 `fd:2`
- FD还可以表示打开的设备
  - 键盘、屏幕、磁盘等
  - 程序员不需要考虑IO细节
  - 不同设备只需要定义不同的IO操作
- 每个进程有自己的FD命名空间

##### 文件描述符的作用

> 隔离用户和内核

- 安全性
  - 用户无法访问内核的数据结构
- 不可屏蔽性
  - 所有的文件操作都应该由内核执行

#### 文件游标 Cursor

- 文件游标
  - 记录了一个文件中下一次操作的位置
  - 可以由 `seek` 操作修改
- 共享游标
  - 父进程将FD传递给子进程
  - 允许父子进程共享同一个文件
- 非共享游标
  - 两个不同的进程打开同一个文件

#### `fd_table` 和 `file_table`

- 整个系统维护了一个 `file_table`
  - 记录了所有打开文件的信息
  - `inode` 号、文件游标、引用数（打开该文件的游标数，不同于 `inode` 的 `refcnt`）
  - 因此父子进程间可以共享文件游标
- 每个进程维护了一个 `fd_table`
  - 记录了该进程每个 `fd` 所对应文件在 `file_table` 中的索引
  - POSIX规范要求打开文件时返回的 `fd` 是表中可用的最小的 `fd`
    - 直接导致无优化时多核性能较差
    - 因为每个进程打开文件时必须锁住 `fd_table`、找到最小的 `fd` 并将其标为“在使用”

#### `OPEN` 的实现

```js
function open(finename, flags, mode) {
  inode_number = path_to_inode_number(filename, wd)
  if (inode_number == null and flags == CREATE) {
    inode_number = create(filename, mode)
  }
  if (inode_number == null) {
    return FAILURE
  }

  inode = inode_number_to_inode(inode_number)
  if (permitted(inode, flags)) { // check permissions
    file_index = insert(file_table, inode_number)
    fd = find_unused_descriptor(fd_table)
    fd_table[fd] = file_index
    return fd
  } else {
    return FAILURE
  }
}
```

#### `READ` 的实现

```js
function read(fd, buf, n) {
  file_index = fd_table[fd]
  cursor = file_table[file_index].cursor
  
  inode_number = file_table[file_index].inode_number
  inode = inode_number_to_inode(inode_number)
  
  m = min(inode.size - cursor, n)
  update_atime(inode, now())

  if (m == 0) {
    return EOF
  }
  for (i = 0; i < m; ++i) {
    b = inode_number_to_block(i, inode_number)
    copy(b, buf, min(m-i, BLOCK_SIZE))
    i = i + min(m-i, BLOCK_SIZE)
  }
  file_table[file_index].cursor = cursor + m
  return m
}
```

#### 一个简单文件系统的磁盘布局

```text
| S | i | d | - | - | - | D | D | D | D | ...
```

- 磁盘开头存放文件元数据
  - `S` 是超级块
    - inode个数
    - 数据块个数
    - inode表起始位置（例如磁盘块`3`）
    - ...
    - Magic Number，指示文件系统类型
  - `i` 空闲 inode 的 bitmap
  - `d` 空闲数据块的 bitmap

#### 删除一个打开的文件

- 假设一个进程打开了文件
- 另一个文件将文件删除
- 在POSIX系统中，文件的 `inode` 不会被释放和删除，直到打开文件的进程调用 `close`
  - 在WINDOWS上则禁止删除打开的文件

!!!warning
    请牢记 `inode` 的 `size` 不能先于数据更新，否则万一中途断电或出现问题，`size` 增加（而内容没有更新时）可能读到其他数据（随机/垃圾/未清零的已删除文件等）

### `sync`

#### Block Cache

- 缓存了最近被使用的磁盘块
  - 缓存缺失时才从磁盘中读取
- 推迟数据向磁盘的写入
  - 寻求机会批量写入，提升访问磁盘的性能
- 但是如果在缓存写回磁盘前发生故障，则可能导致不一致性
- `sync` 调用保证对文件的所有修改被写入设备

## 文件系统崩溃一致性

文件系统中保存了多种数据结构，不同数据结构间存在依赖关系和一致性要求，如果遭遇突发状况，可能导致这些数据结构之间的一致性被打破

### 例子：追加文件数据 APPEND

涉及三次磁盘写入。假设单次磁盘写入能保证原子性。

1. 将数据写入磁盘数据块
2. 将 `inode` 写入磁盘的 `inode_table`
3. 更新 `inode` 和 `data` 在磁盘上的bitmap

崩溃时

- 只有1.成功，则没有太大问题
  - 白 写 了
- 只有2.成功，则会造成安全性问题
  - `inode` 的 `size` 和 `pointer` 都被更新了，但是数据没有更新
- 只有3.成功，则会浪费一个磁盘块
  - 虽然问题不是很大但是还是有问题
- 12成功，但是bitmap未更新
  - 可能导致另一个文件误认为当前块未被使用，导致两个 `inode` 指向同一个块
  - 安全性问题
- 23成功，则可能读到垃圾数据
  - 安全性问题
- 13成功，则会浪费一个磁盘块

### 用户期望

在从崩溃恢复后，用户期望

1. 维护文件系统的数据结构仍然可靠
2. 仅最近的一些操作没有被保存到磁盘
3. 没有顺序的异常

### 同步元数据写+FSCK

若非正常重启，则运行FSCK检查磁盘

1. 检查Superblock
   - 保证文件系统大小大于已分配磁盘块总和
   - 否则尝试使用Superblock的物理备份
2. 检查空闲的Block
   - 扫描所有 `inode` 包含的磁盘块
   - 用扫描结果修正对应的 bitmap
   - 对 `inode_bitmap` 也执行类似操作
3. 检查 `inode` 状态
   - 检查类型：普通文件、目录、符号文件
   - 若类型错误，则清除掉 `inode` 和对应 bitmap
4. 检查 `inode` 链接
   - 扫描整个文件系统书，核对文件连接数量
   - 如果某一个 `inode` 存在（bitmap为1），但是不存在于任何一个目录，则存放到 `/lost+found`
5. 检查重复磁盘块
   - 例如两个 `inode` 指向同一个磁盘块
   - 如果其中一个 `inode` 明显有问题，则删除
   - 否则复制磁盘块，每个 `inode` 使用一个
6. 检查坏的磁盘块ID
   - 例如指向超出磁盘空间的ID
   - 但是FSCK并不能修复这类问题
7. 检查目录
   - 保证 `.` 和 `..` 是位于头部的目录项
   - 保证目录的链接数只能是一个
   - 目录中不能有相同的文件名

#### 问题

- 慢
  - 每 `70GB` 大约需要10分钟
  - 对 `4TB` 硬盘，大约需要十小时
- 同步元数据写导致创建文件等操作很慢

> “所以大家对FSCheck非常痛恨。可以买到专门的FSCK的衣服”

### 基于日志的一致性

> “容错的本质是冗余”

- 在进行修改，先将修改记录到日志 Journal 中
- 所有要进行的修改都记录完毕后，提交日志
  - 写完日志后，写 `commit` 表示该日志是完整的
- 然后再进行修改
- 修改之后，删除日志

#### Ext4的日志实现

作为例子，Ext4 提供了三种不同的日志配置

- Data Mode
  - 数据和元数据都写入日志区域
  - 严格的 All-or-nothing
  - 但是所有磁盘读写需要的空间全部翻倍
  - “我搞了部蓝光电影，40G” `<-There goes 80GB disk space`
- Ordered mode
  - 先将数据写入原本的文件位置，再将元数据写入日志
  - 作为文件系统的默认配置
- Writeback mode
  - 仅将元数据写入日志，新数据写入原本的文件位置，但是不保证两者顺序
  - 即写完数据后不会强制flush

##### Ordered Mode 两次 Flush

1. 写入数据（写入原数据所在位置）和更新后的元数据（写入日志）
2. 调用flush确保数据确实写入磁盘
3. 在日志区写入 `commit`，再次调用flush
4. 在数据段写入元数据

- 如果在 `commit` 中加入数据和元数据的哈希或校验和，则 `commit` 可以和数据、元数据一起写入磁盘，而无需额外调用flush

#### 基于日志的恢复

- 启动后检查日志区域
  - 若没有日志，则无需恢复
- 扫描所有已经commit的事务
  - 如果没有commit，则无需恢复
  - 否则需要将元数据从日志区写到原本的位置
- 完成后清空日志
