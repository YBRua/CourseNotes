# 同步原语的实现

!!!warning 锁
    在本节中，请始终记住：**一旦放锁，就可能发生很多事情。**

## 互斥锁实现

### 皮特森算法

> 互斥锁的软件实现

#### 问题设定

- 假设有两个线程，一个临界区
  - 同一时刻只有一个线程能进临界区
- 两个数据结构
  - 每个线程一个 `flag`： `flag[0]` 和 `flag[1]`
  - 一个 `turn`，可以是 `0` 或 `1`，表示轮到谁

#### 算法实现

```cpp
// thread 0
while (true) {
    flag[0] = true; // flag[1] = true for thread 1
    turn = 1; // turn = 0 for thread 1
    while (flag[1] == true && turn == 1)
    {
        // wait
    }
    /* critical zone */
    flag[0] = false;
}
```

从线程0的角度

- 如果 `flag[1] == 0`
  - 线程1不在临界区，自己可以进入临界区
- 如果 `flag[1] == 1 && turn == 1`
  - 要么线程1在临界区，线程0需要等待
  - 要么线程1刚刚执行完 `flag[1] = true` 但尚未进入临界区，此时线程1马上将会把 `turn` 置零，此后线程0即可进入临界区
- 如果 `flag[1] == 1 && turn == 0`
  - 线程1正在等待，线程0可以进入

#### 问题

皮特森算法可能并不能在现代CPU上正常运行

- 算法假设
  - `flag[i]` 必须在 `turn` 被设置前设置，否则两个线程可能同时进入临界区
  - 要求访存操作顺序执行
  - 但是许多现代CPU的内存一致性模型并不能满足上述假设
    - 访存操作可能是乱序执行的

### 原子指令

由硬件提供。原子指令是不可被打断的一个或一系列操作。一个原子指令要么被完整执行，要么完全不执行。

#### Test-and-Set

```cpp
int TestAndSet(int *old_ptr, int new_val) {
    int old = *old_ptr; // read old value
    *old_ptr = new_val; // set new value
    return old; // return old value
}
```

基于 Test-And-Set 可以实现自旋锁

```cpp
void lock(lock_t *lock) {
    while (TestAndSet(&lock->flag) == 1)
        ; // wait
}
```

#### Compare-and-Swap

```cpp
int CompareAndSwap(int *ptr, int expected, int new_val) {
    int actual = *ptr; // read current value in ptr
    if (actual == expected)
        *ptr = new_val; // set new value
    return actual; // return value read from ptr
}
```

##### Intel对CAS的实现

#### Load-Linked 与 Store-Conditional

ARM体系结构提供的新原子指令

```cpp
int LoadLinked(int *ptr) {
    return *ptr;
}

int StoreConditional(int *ptr, int value) {
    /* If no one has updated *ptr since the LoadLinked to this addr */
    if (NoOneUpdatedPTRSinceLoadLinkedToThisAddr()) {
        *ptr = value;
        return 1; // success
    } else {
        return 0; // failure
    }
}
```

基于LL-SC实现的自旋锁需要一个 `while` 循环

#### Fetch-and-Add

```cpp
int FetchAndAdd(int *ptr) {
    int old = *ptr;
    *ptr = old + 1;
    return old;
}
```

> 餐厅排队取号就是说。

基于Fetch-and-Add可以实现 Ticket Lock

### 各种互斥锁

#### 自旋锁 Spin Lock

```cpp
```

#### 排号锁 Ticket Lock

- [x] 互斥访问
- [x] 有限等待
  - 按照顺序，只要前序竞争者保证在有限时间释放，则可以实现有限等待
- [x] 空闲让进

## 信号量实现

### 信号量回顾

条件变量有两个接口

```c
void wait(struct cond *cond, struct lock *mutex)
  // call system call yield() to release CPU occupation
```

1. 放入条件变量的等待队列
2. 阻塞自己、释放锁（这两步是原子的）
3. 被唤醒后重新获取锁

```c
void signal(struct cond *cond)
```

1. 检查等待队列
2. 如果有等待者则移除队列并唤醒等待着

### `yield()`

- 进程调用 `yield()` 主动放弃CPU，进入可运行队列等待
  - 类似 `sleep()`

#### 具体步骤

1. 暂停当前运行的线程
2. 选择新的可运行线程
3. 恢复新选择的可运行线程

#### 数据结构

- `threads table` 记录所有线程的表
- `t_lock` 即 Threads Table Lock，用于保护 Threads Table
- `CPUs table` 记录每个CPU当前运行的线程，但是并没有锁保护

#### 参考实现

```python
def yield():
    """acquire t_lock because we need to modify thread table"""
    acquire(t_lock)

    """hang current thread"""
    id = cpus[CPU].thread  # get current thread id
    if thread is None:
        return
    threads[id].state = RUNNABLE  # set current thread to runnable
    threads[id].sp = SP  # stack pointer; save context

    """find the next runnable thread"""
    do:
        id = (id + 1) % N
    while threads[id].state != RUNNABLE

    """recover context of new thread
       Note that at least one thread is RUNNABLE
       because current thread has just been paused
    """
    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id

    """Note that the context has switched"""
    release(t_lock)
```

### WAIT/SIGNAL 实现

#### 错误实现

```python
def send(bb, msg):
    acquire(bb.lock)
    while True:
        if bb.in - bb.out < N:
            bb.buff[bb.in & N] = msg
            bb.in += 1
            release(bb.lock)
            signal(bb.not_empty)
            return
        release(bb.lock)
        """A lot of things could happen here!"""
        wait(bb.not_full) # calls yield() here
        acquire(bb.lock)
```

这个实现是错误的。如果sender刚刚释放锁，但是还没有执行到 `wait(bb.not_full)`。此时另一个CPU执行 `receive`，`receive` 疯狂操作清空了 buffer并发送 `bb.not_full` 的信号。但是此时sender还没有等待 `not_full` 的信号，而当 sender 真的开始等待 `not_full` 时已经没有人会发送这个信号了，于是 sender 与世长辞。寄！

- 因此，必须要把 `release`、`wait`、`acquire` 打包成一个函数 `wait(bb.not_full, bb.lock)`

#### WAIT

```python
def wait(cv, lock):
    disable_interrupt()
    acquire(t_lock)
    release(lock)
    threads[id].cv = cv
    threads[id].state = WAITING  # not RUNNABLE
    yield_wait()
    release(t_lock)
    enable_interrupt()
    acquire(lock)
```

#### SIGNAL

```py
def signal(cv):
    acquire(t_lock)
    for i in range(N):
        if threads[i].cv == cv and threads[i].state == WAITING:
            # thread i is waiting for signal cv
            threads[i].state = RUNNABLE
```

#### YIELD_WAIT

```py
def yield_wait():
    id = cpus[CPU].thread
    cpus[CPU].thread = None
    threads[id].sp = SP
    SP = cpus[CPU].stack  # notice here

    do:
        id = (id + 1) % N
        release(t_lock)  # notice here
        enable_interrupt()
        disable_interrupt()
        acquire(t_lock)  # notice here
    while threads[id].state != RUNNABLE

    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id
```

#### 处理时钟中断

当一个线程的时间片到了，将会触发时钟中断，由中断处理函数调用 `yield()`。万一CPU在

## 信号量的实现

### 信号量的语义实现

这个实现是不对的。

```cpp
void wait(int S) {
    while (S <=0)
        /* waiting */;
    atomic_add(&S, -1); // problematic here
}

void signal(int S) {
    atomic_add(&S, 1);
}
```

两个等待中的线程可能同时以为自己拿到了资源，同时执行 `atomic_add(&S, -1)`，然后信号量变成了 `-1`。寄！

因此需要对信号量本身加锁

```cpp
void wait(sem_t *S) {
    lock(S->lock);
    while (S->value <=0) {
        unlock(S->lock);
        lock(S->lock);
    }
    S->value--;
    unlock(S->lock);
}

void signal(sem_t *S) {
    lock(S->lock);
    S->value++;
    unlock(S->lock);
}
```

> “我们这里都是假设程序员无比地智慧。写代码都没有bug。”

信号量的最终实现使用了条件变量、互斥锁和一个计数器

- `value`
  - 正数为信号量
  - 负数为有人等待
- `wakeup`
  - 等待时可以唤醒的数量
- 某一时刻真实的信号量是 `value >= 0 ? value : wakeup`

```cpp
void wait(sem_t *S) {
    lock(S->sem_lock);
    S->value--;
    if ()
}
```
