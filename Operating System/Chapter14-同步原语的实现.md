# 同步原语的实现

!!!warning 锁
    在本节中，请始终记住：**一旦放锁，就可能发生很多事情。**

!!!info 有关原子操作
    本节提供的代码样例中，假设CPU对于地址对齐的64位写操作都是原子的，所以部分代码并没有用原子指令保证操作的原子性。在实际编程时，应该使用编程语言提供的原子操作，交给编译器决定是否需要生成额外的代码保障原子性。

## 互斥锁实现

### 单核硬件实现：关闭中断

- 对于单核设备，只要进入临界区前关闭中断，就意味着当前线程不会在临界区内被其他线程抢占
  - 保证了任意时刻至多一个线程在临界区内，实现了互斥访问
  - 在离开临界区前，需要重新开启中断，以保证空闲让进
- 但是对于多核设备，即使关闭所有核心的中断，也不能阻塞其他核心上正在执行的线程，它们仍可能进入临界区，因此只依靠关中断不能保证互斥访问

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
    flag[0] = false; // flag[1] = false for thread 1
}
```

从线程0的角度

- 如果 `flag[1] == false`
  - 线程1不在临界区，自己可以进入临界区
- 如果 `flag[1] == true && turn == 1`
  - 要么线程1在临界区，线程0需要等待
  - 要么线程1刚刚执行完 `flag[1] = true` 但尚未进入临界区，此时线程1马上将会把 `turn` 置零，此后线程0即可进入临界区
- 如果 `flag[1] == true && turn == 0`
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

#### 为什么需要原子指令

考虑一种直观但是错误的互斥锁实现

```cpp
/* a lock that does not work */
struct lock { int state; }

void acquire (lock *L) {
    while (L->state == LOCKED) {
    }  // busy loop
    L->state = LOCKED;
}

void release (lock *L) {
    L->state = UNLOCKED;
}
```

- 假设有两个线程 `A` 和 `B`
- `A` 先通过 `acquire` 尝试获得锁，但是在刚出 `while` 循环时被调度走了
- `B` 通过 `acquire` 获得锁
- `A` 被调度到，执行下一步 `L->state = LOCKED`，获得锁
- 于是两个线程可以同时进入临界区

根本原因在于检查锁的状态和上锁两步不是原子操作，而我们显然不能通过另一个锁来保证上锁过程的原子性

#### Test-and-Set

```cpp
int TestAndSet(int *old_ptr, int new_val) {
    int old = *old_ptr; // read old value
    *old_ptr = new_val; // set new value
    return old; // return old value
}
```

##### 基于 Test-and-Set 的自旋锁

```cpp
struct lock_t {
    int flag;
}

void lock(lock_t *lock) {
    while (TestAndSet(&lock->flag) == 1)
        ; // wait
}

void unlock(lock_t *lock) {
    lock->flag = 0;
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

##### 基于 Comare-and-Swap 的自旋锁

```cpp
void lock(lock_t *lock) {
    while (CompareAndSwap(&lock->flag, 0, 1) == 1) {
        // spinning
    }
}
```

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

##### 基于 LL-SC 的自旋锁

基于LL-SC实现的自旋锁需要一个 `while` 循环

```cpp
void lock(lock_t *lock) {
    while (true) {
        while (LoadLinked(&lock->flag) == 1) {
            // spin
        }
        if (StoreConditional(&lock->flag, 1) == 1) {
            return; // successfully locked
        }
        // otherwise try it all over again
    }
}
```

### 自旋锁 Spin Lock

前文的互斥锁都是自旋锁，在加锁时，如果空闲则直接上锁，否则会不断循环重试

#### 自旋锁的问题

自旋锁是否满足解决临界区问题的三个必要条件？

- 互斥访问 :heavy_check_mark:
- 空闲让进 :heavy_check_mark:
- 有限等待 :x:
  - 空闲时，会让所有竞争者都同时尝试完成原子操作
  - 原子操作的成功与否完全取决于硬件特性
  - 某些情况下某些线程可能一直无法获得锁，破坏了公平性

### 排号自旋锁 Ticket Lock

> 餐厅排队取号就是说。

排号锁按照锁竞争者的申请顺序传递锁，所有竞争者形成一个先入先出的队列。

排号锁基于一个新的原子操作 `FetchAndAdd()`

#### Fetch-and-Add

```cpp
int FetchAndAdd(int *ptr) {
    int old = *ptr;
    *ptr = old + 1;
    return old;
}
```

#### 排号锁

- 互斥访问 :heavy_check_mark:
- 空闲让进 :heavy_check_mark:
- 有限等待 :heavy_check_mark:
  - 按照顺序，只要前序竞争者保证在有限时间释放，则可以实现有限等待

##### 基于 Fetch-and-Add 的排号锁

```cpp
struct lock_t {
    int ticket;
    int turn;
}

void lock_init(lock_t *lock) {
    lock->ticket = 0;
    lock->turn = 0;
}

void lock(lock_t *lock) {
    int myturn = FetchAndAdd(&lock->ticket);
    while (lock->turn != myturn) {
        // spin
    }
}

void unlock(lock_t *lock) {
    lock->turn = lock->turn + 1;
}
```

## 条件变量的实现

### 条件变量回顾

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

#### 条件变量的语义

```cpp
struct cond {
    struct thread *wait_list;
}

void cond_wait(struct cond* cond, struct lock *mutex) {
    list_append(cond->wait_list, thread_self());
    atomic_block_unlock(mutex); // must be atomic
    lock(mutex); // re-acquire mutex after receiving signals
}

void cond_signal(struct cond *cond) {
    if (!list_empty(cond->wait_list)) {
        wakeup(list_remove(cond->wait_list));
    }
}

void cond_broadcast(struct cond *cond) {
    while (!list_empty(cond->wait_list)) {
        wakeup(list_remove(cond->wait_list));
    }
}
```

- `cond_wait` 中，阻塞自己和放锁必须是原子的。
  - 如果先阻塞自己再放锁，则被阻塞的线程已经没法放锁了
  - 如果先放锁再阻塞自己，则线程 A 放锁之后、阻塞自己之前，可能被调度走，此时线程 B 一通操作执行了 `cond_signal`，但是线程 A 还没有阻塞自己，所以它不会被唤醒，而是在下一次调度到自己时才会挂起自己，从而错过 `signal`

### 条件变量的基础 `yield()`

- 进程调用 `yield()` 主动放弃CPU，进入可运行队列等待
  - 类似 `sleep()`

#### 具体步骤

1. 暂停当前运行的线程：保存上下文
2. 选择新的可运行线程
3. 恢复新选择的可运行线程

#### 数据结构

- `threads table` 记录所有线程的表
- `t_lock` 即 Threads Table Lock，用于保护 Threads Table
- `CPUs table` 记录每个CPU当前运行的线程，但是并没有锁保护

#### 参考实现

```js
function yield() {
    // acquire t_lock because we need to modify thread table
    acquire(t_lock)

    // hang current thread
    id = cpus[CPU].thread  // get current thread id
    threads[id].state = RUNNABLE  // set current thread to runnable
    threads[id].sp = SP  // stack pointer; save context

    // find the next runnable thread
    do {
        id = (id + 1) % N
    } while (threads[id].state != RUNNABLE)

    // recover context of new thread
    // Note that at least one thread is RUNNABLE
    // because current thread has just been paused
    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id

    // Note that the context has switched
    release(t_lock)
}
```

### 基于 `yield` 的 `wait` / `signal` 实现

#### 错误实现

考虑一个向共享缓存 `bb` 添加物品的 `send()` 函数，该函数调用 `wait`，但是该 `wait` 的实现有问题。

```js
// bb is a buffer, msg is the message
function send(bb, msg) {
    acquire(bb.lock)
    while (true) {
        if (bb.in - bb.out < N) {
            bb.buff[bb.in % N] = msg
            bb.in += 1
            release(bb.lock)
            signal(bb.not_empty)
            return
        }
        release(bb.lock)
        // A lot of things could happen here!
        wait(bb.not_full) // calls yield() inside
        acquire(bb.lock)
    }
}
```

注意到这个错误实现的 `wait` 函数只需要 `condition` 而不需要 `mutex`。

这个实现是错误的。如果sender刚刚释放锁，但是还没有执行到 `wait(bb.not_full)`。此时另一个CPU执行 `receive`，`receive` 趁机从 buffer 取走了所有 `msg` 并疯狂发送 `bb.not_full` 的信号。但是此时sender还没有等待 `not_full` 的信号，而当 sender 真的开始等待 `not_full` 时已经没有人会发送这个信号了，于是 sender 与世长辞。寄！

- 因此，必须要保证放锁和yield的原子性

#### WAIT 与 SIGNAL

首先看 `wait` 和 `signal` 的初版实现

```js
function wait(cv, lock) {
    acqure(t_lock)  // acquire thread table lock
    release(lock)
    threads[id].cv = cv  // current thread waiting for cv
    threads[id].state = WAITING  // block thread, not RUNNABLE
    yield_wait()  // not yield here
    release(t_lock)
    acquire(lock)
}
```

```js
function signal(cv) {
    acquire(t_lock)
    for (i = 0; i < N; ++i) {
        if (threads[i].cv == cv && threads[i].state == WAITING) {
            threads[i].state = RUNNABLE
        }
    }
    release(t_lock)
}
```

注意上述 `wait` 中，必须先获得 `t_lock` 再释放原本的 `lock`，否则在释放 `lock`、获取 `t_lock` 之前，仍然可能被调度走，然后另一个线程调用 `signal`，导致`wait` 的线程错过 `signal`

基于该 `wait` 和 `signal` 实现的 `send` 为

```js
function send(bb, msg) {
    acquire(bb.lock)
    while (true) {
        if (bb.in - bb.out < N) {
            bb.buff[bb.in % N] = msg
            bb.in += 1
            release(bb.lock)
            signal(bb.not_empty)
            return
        }
        wait(bb.not_full, bb.lock)
    }
}
```

#### `yield_wait`

上述实现中，使用了 `yield_wait` 函数，该函数的实现如下

```js
function yield_wait() {
    // no need to acquire t_lock here
    // it has been acquired in wait()

    // called by wait()
    id = cpus[CPU].thread
    // no need to set current thread to WAITING here
    // it has been done in wait()
    threads[id].sp = SP

    // NOTE HERE
    do {
        id = (id + 1) % N
    } while (threads[id].state != RUNNABLE)

    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id
}
```

##### 放锁再拿锁

- 注意到 `yield_wait` 中有一个 `do-while` 循环，该循环尝试寻找一个 `RUNNABLE` 的线程
- 那么如果没有 `RUNNABLE` 的线程怎么办？
  - 此时执行 `yield_wait` 的线程将拿着 `t_lock` 跑一个死循环！寄！
- 除非其他CPU执行 `signal`，将一些线程变成 `RUNNABLE`
  - 但是运行 `signal` 需要 `t_lock`，而拿着 `t_lock` 的线程正在跑一个死循环
    - 然后死锁了
    - 打破这个死锁的方法是不允许持有并等待：要求在该 `do-while` 循环中先放锁再拿锁，进而允许其他线程拿到 `t_lock`

该 `do-while` 循环需要做如下修改

```js
do {
    id = (id + 1) % N
    release(t_lock)
    acquire(t_lock)
} while (threads[id].state != RUNNABLE)
```

##### 保存栈信息

- 但是这仍然有问题：一旦释放 `t_lock`，另一个CPU可能恰好运行 `signal` 将当前线程改为 `RUNNABLE`，然后又一个CPU可能恰好运行 `wait`，该 `wait` 找到了阴差阳错变成 `RUNNABLE` 的本线程，然后尝试运行本线程，于是此时两个CPU的 `SP` 指向了同一个位置
  - 本线程的运行时栈被破坏！
- 解决方案是为每一个CPU设置一个专门的栈，这个栈只是临时使用，专门用来做 `yield`，且不同CPU之间不共享，SP马上会指向新线程的栈

```js
function yield_wait() {
    id = cpus[CPU].thread
    threads[id].sp = SP

    // use temporary CPU stack
    SP = cpus[CPU].stack

    do {
        id = (id + 1) % N
        release(t_lock)
        acquire(t_lock)
    } while (threads[id].state != RUNNABLE)

    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id
}
```

### 处理时钟中断

- 当一个线程的时间片到了，将会触发时钟中断，由中断处理函数调用 `yield()`。但是万一CPU在中断时正在 `yield` 或 `yield_wait` 中，处于拿着 `t_lock` 但没放下的状态，则会卡在 `yield` 尝试拿 `t_lock` 的步骤，于是开始自己等自己。
- 因此，在 `wait` 和 `yield_wait` 中拿 `t_lock` 前需要关中断、在放 `t_lock` 后需要重开中断。
- 但是这种实现仍然有问题，考虑修改后的 `yield_wait`

```js
// in yield_wait
do {
    id = (id + 1) % N
    release(t_lock)
    enable_interrupt()
    // assume yield() happens here
    disable_interrupt()
    acquire(t_lock)
} while (threads[id].state != RUNNABLE)
```

如果 `yield` 发生在开中断、关中断之间，则进入 `yield` 后会把当前线程状态改为   `RUNNABLE`。可是在 `yield_wait` 外面的 `wait` 里我们刚刚把线程状态改到 `WAITING`！

- 那我的 `WAITING` 不就没了吗！

于是需要修改 `yield_wait`，把当前CPU的 `thread` 设为空，并在 `yield` 中增加判空检查。

### `yield` `yield_wait` 的完整实现

```js
function yield_wait() {
    id = cpus[CPU].thread

    // nullify current CPU thread
    cpus[CPU].thread = null

    threads[id].sp = SP

    // use temporary CPU stack
    SP = cpus[CPU].stack

    do {
        id = (id + 1) % N
        release(t_lock)
        enable_interrupt()
        disable_interrupt()
        acquire(t_lock)
    } while (threads[id].state != RUNNABLE)

    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id
}

function yield() {
    // acquire t_lock because we need to modify thread table
    acquire(t_lock)

    // hang current thread
    id = cpus[CPU].thread  // get current thread id
    
    if (id == null) {
        // do nothing if no thread is running on current CPU
        return
    }
    
    threads[id].state = RUNNABLE  // set current thread to runnable
    threads[id].sp = SP  // stack pointer; save context

    // find the next runnable thread
    do {
        id = (id + 1) % N
    } while (threads[id].state != RUNNABLE)

    // run next thread
    SP = threads[id].sp
    threads[id].state = RUNNING
    cpus[CPU].thread = id

    release(t_lock)
}
```

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

两个等待中的线程可能同时以为自己拿到了资源，先后离开 `while` 循环，先后执行 `atomic_add(&S, -1)`，然后信号量变成了 `-1`。寄！

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
    while (S->value < 0) {
        do {
            cond_wait(S->sem_cond, S->sem_lock);
        } while (S->wakeup == 0)
        S->wakeup--;
    }
    unlock(S->sem_lock)
}

void signal(struct sem *S) {
    lock(S->sem_lock);
    S->value++;
    if (S->value <= 0) {
        // people are waiting
        S->wakeup++;
        cond_signal(S->sem_cond);
    }
    unlock(S->sem_lock);
}
```

注意这里需要使用一个 `do-while` 循环保障有限等待和公平性。否则一个线程调用完 `signal` 之后立刻调用 `wait`，然后立刻重新获得刚刚释放的资源。
